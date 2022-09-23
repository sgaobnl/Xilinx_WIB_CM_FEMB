from binascii import hexlify
from codecs import readbuffer_encode
from operator import index
import os
from string import hexdigits
from symbol import continue_stmt
from sys import path_hooks
from turtle import ondrag
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy.stats import norm
from scipy.optimize import curve_fit
import scipy.stats as stats
# progress bar
import time
from tqdm import tqdm
# for ASICDAC_CALI data analysis
import pickle

# function for one file
def get_pathToFile(sourceMainDir='', dataType='pedestal', indexFile=0):
    path_to_file = '/'.join([sourceMainDir, dataType, os.listdir(os.path.join(sourceMainDir, dataType))[indexFile]])
    return path_to_file

def read_csv(path_to_file: str):
    # path_to_file = get_pathToFile(sourceMainDir=sourceMainDir, dataType=dataType, indexFile=indexFile)
    data_df = pd.read_csv(path_to_file)
    return data_df

def get_temperature_pF(data_df: pd.DataFrame):
    '''
    This function should return:
        *   'LN' for liquid Nitrogen or 'RT' for Room Temperature.
        *   the input capacitance of a board that plugged into the FEMBs : '0pF' or '150pF'
        in an tuple (temperature, pF)
    '''
    # temperature
    temperature = 'RT'
    folderName = data_df['folderName']
    folderName_temp = pd.Series([k.split('_')[1] for k in folderName])
    if (folderName_temp == 'LN').sum() == len(folderName_temp):
        temperature = 'LN'
    # pF
    pF = '0pF'
    folderName_pF = pd.Series([k.split('_')[-1] for k in folderName])
    if (folderName_pF == '150pF').sum() == len(folderName_pF):
        pF = '150pF'
    return (temperature, pF)

def get_titleFromFileName(path_to_file='', temperature='LN', pF='0pF'):
    tmp_title = path_to_file.split('/')[-1].split('.')[0]
    tmp_title = tmp_title.split('_')[2:]
    tmp_title.append(temperature)
    tmp_title.append(pF)
    title = '_'.join(tmp_title)
    return title

def hist(plt, dataVec: pd.Series, xlabel='', ylabel='', title='', legend='', nbins=100, inLog=False, inDensity=False):
    d = plt.hist(dataVec, color='b', log=inLog, bins=nbins, density=inDensity, label=legend)
    plt.xlabel(xlabel, fontsize='13')
    plt.ylabel(ylabel, fontsize='13')
    plt.title(title)

def get_gaussPdf(dataVec: pd.Series, nstd=3, skewed=False):
    '''
    This function returns (dataSelected, mean, std, x, pdf) where mean and std are mean and std of the data selected;
    x is a list of number between the range xmin to xmax;
    pdf is the probability density function
    '''
    # select data in the range (mean - std * nstd) and (mean + std * nstd)
    old_mean = np.mean(dataVec)
    old_std = np.std(dataVec)
    old_xmin = old_mean - nstd * old_std
    old_xmax = old_mean + nstd * old_std
    dataSelected = dataVec[(dataVec >= old_xmin) & (dataVec <= old_xmax)]
    # get new mean and new std from the selected data
    new_mean = np.mean(dataSelected)
    new_std = np.std(dataSelected)
    # mean and std are properties of the fitting distribution
    mean, std, xmin, xmax = 0.0, 0.0, 0.0, 0.0
    ae = 0.0
    x = []
    pdf = []
    if not skewed:
        # fit the dataSelected with gaussian distribution
        mean, std = norm.fit(dataSelected)
        xmin = mean - nstd * std
        xmax = mean + nstd * std
        x = np.linspace(xmin, xmax, 100)
        pdf = norm.pdf(x, mean, std)
    else:
        # fit the dataSelected with a skewed gaussian distribution
        ae, loc, scale = stats.skewnorm.fit(dataSelected)
        # xmin = mean - nstd * std
        # xmax = mean + nstd * std
        xmin = old_xmin
        xmax = old_xmax
        x = np.linspace(xmin, xmax, 1000)
        pdf = stats.skewnorm.pdf(x, ae, loc, scale)
        ## now can return loc and scale of the distribution
        return (dataSelected, new_mean, new_std, loc, scale, x, pdf)
    return (dataSelected, new_mean, new_std, x, pdf)

def fit_withGaussian(sourceMainDir='', dataType='pedestal', outputDir='', indexFile=0, nstd=3, nbins=100, skewed=False):
    '''
    This function fits the data with a gaussian distribution
    '''
    path_to_file = get_pathToFile(sourceMainDir=sourceMainDir, dataType=dataType, indexFile=indexFile)
    data_df = read_csv(path_to_file=path_to_file)
    temperature, pF = get_temperature_pF(data_df=data_df)
    histTitle = get_titleFromFileName(path_to_file=path_to_file, temperature=temperature, pF=pF) #
    # separate BL, Gain, Shaping Time, temperature, inputCapacitance
    tmp_histTitle = histTitle.split('_')
    BL = tmp_histTitle[0]
    Gain = '_'.join([tmp_histTitle[1], tmp_histTitle[2]])
    ShapingTime = '_'.join([tmp_histTitle[3], tmp_histTitle[4]])
    ## temperature and inputCapacitance=pF are already found
    # Gaussian parameters
    out_dist = get_gaussPdf(data_df[dataType], nstd=nstd, skewed=skewed)
    # get dataSelected and informations of the fitting distribution
    dataSelected, mean, std, x, pdf = out_dist[0], out_dist[1], out_dist[2], out_dist[-2], out_dist[-1]
    # if the distribution is skewed, need the loc and scale parameters
    loc = -2022
    scale = -2022
    if skewed:
        loc = out_dist[3]
        scale = out_dist[4]
    #
    # plot the distribution with the fitting curve
    plt.figure(figsize=(12,7))
    plt.rcParams.update({'figure.max_open_warning': 0}) # get rid of the warning
    plt.plot(x, pdf, color='r', label='Gaussian fit')
    hist(plt=plt, dataVec=dataSelected, xlabel=dataType, ylabel='#',
        title=histTitle, legend='data_selected: mean_data = {:.4f}; std_data = {:.4f}'.format(mean, std), nbins=nbins, inDensity=True, inLog=False)
    plt.legend()
    plt.savefig(os.path.join(outputDir, histTitle + '_.png'))
    if (loc >= 0) & (scale >= 0):
        return (BL,Gain, ShapingTime, temperature, pF, mean, std, loc, scale)
    return (BL,Gain, ShapingTime, temperature, pF, mean, std)

def save_gaussianInfo(sourceMainDir: str, dataType: str, outputDir: str, nstd=3, nbins=100, Nfiles=32, skewed=False):
    '''
    This function saves the configuration along with the mean and std in a csv file
    '''
    BL, Gain, ShapingTime, temperature, inputCapacitance, mean, std = [], [], [], [], [], [], []
    loc, scale = [], []
    for i in tqdm(range(Nfiles)):
        out_fit = fit_withGaussian(sourceMainDir=sourceMainDir, dataType=dataType,
                                                            outputDir=outputDir, indexFile=i, nstd=nstd,
                                                            nbins=nbins, skewed=skewed)
        if len(out_fit) == 9:
            loc.append(out_fit[-2])
            scale.append(out_fit[-1])
        # (tbl, tgain, tst, ttemp, ticap, tmean, tstd) = fit_withGaussian(sourceMainDir=sourceMainDir, dataType=dataType,
        #                                                     outputDir=outputDir, indexFile=i, nstd=nstd,
        #                                                     nbins=nbins, skewed=skewed)
        BL.append(out_fit[0])
        Gain.append(out_fit[1])
        ShapingTime.append(out_fit[2])
        temperature.append(out_fit[3])
        inputCapacitance.append(out_fit[4])
        mean.append(out_fit[5])
        std.append(out_fit[6])
        time.sleep(0.001)
    filename = '_'.join(['gaussian', dataType + '.csv'])
    # save info in a dataframe
    gaussFit_df = pd.DataFrame()
    if (len(loc) != 0) & (len(scale) != 0):
        gaussFit_df = pd.DataFrame({
            'BL': BL,
            'Gain': Gain,
            'ShapingTime': ShapingTime,
            'Temperature': temperature,
            'inputCapacitance': inputCapacitance,
            'mean': mean,
            'std': std,
            'loc': loc,
            'scale': scale
        })
    else:
        gaussFit_df = pd.DataFrame({
            'BL': BL,
            'Gain': Gain,
            'ShapingTime': ShapingTime,
            'Temperature': temperature,
            'inputCapacitance': inputCapacitance,
            'mean': mean,
            'std': std
        })
    t = '-'*20
    print('{} Saving the fitting information {}\n'.format(t, t))
    try:
        gaussFit_df.to_csv(os.path.join(outputDir, filename), index=False)
        print('{} Information saved {}\n'.format(t, t))
    except:
        print('{} Error occured {}'.format(t, t))

# plot mean vs shaping time
def convert_Gain_to_float(df):
    df['Gain'] = df['Gain'].apply(lambda x: x.split('_')[0] + '.' + x.split('_')[1].split('m')[0])
    df['Gain'] = df['Gain'].apply(lambda x: float(x))
    return df

def convert_Timing_to_float(df):
    df['ShapingTime'] = df['ShapingTime'].apply(lambda x: float(x.split('_')[0] + '.' + x.split('_')[1].split('u')[0]))
    # df['ShapingTime'] = df['ShapingTime'].apply(lambda x: float(x))
    return df

def plot_mean_vs_ShapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv',
                            BL='200mV', outputDir='', ylabel='pedestal', addToTitle='', skewed=False):
    dataFrame = pd.read_csv(path_to_csv)
    dataFrame['BL'] = dataFrame['BL'].apply(lambda x: x[:-2])
    # condition to get the corresponding BL
    condition = (dataFrame['BL']==BL)
    dataFrame = convert_Gain_to_float(dataFrame)
    Gain = dataFrame[condition]['Gain'].unique()
    #-> dataFrame for BL==200mV
    df = dataFrame[condition]
    # -> shaping time to float
    df = convert_Timing_to_float(df)
    # plot baseline vs shapingTime
    plt.figure(figsize=(12,12))
    for gain in tqdm(Gain):
        plt.errorbar(x=df[df['Gain']==gain]['ShapingTime'], y=df[df['Gain']==gain]['mean'],
                     yerr=df[df['Gain']==gain]['std'],
                     label= '_'.join([BL, str(gain) + 'mV/fC']))
        time.sleep(0.001)
    plt.xlabel('Shaping time');plt.ylabel(' '.join([ylabel, 'mean']))
    plt.xticks(ticks=df['ShapingTime'].unique(), labels=df['ShapingTime'].unique())
    plt.legend()
    plt.title('_'.join([addToTitle, 'shapingTime_vs_' + ylabel + 'Mean', BL]))
    plt.savefig(os.path.join(outputDir, '_'.join(['shapingTime_vs_' + ylabel + 'Mean', BL]) + '.png'))
    #
    # save another fig if the distribution is skewed
    if skewed:
        plt.figure(figsize=(12,12))
        for gain in tqdm(Gain):
            plt.errorbar(x=df[df['Gain']==gain]['ShapingTime'], y=df[df['Gain']==gain]['loc'],
                        yerr=df[df['Gain']==gain]['scale'],
                        label= '_'.join([BL, str(gain) + 'mV/fC']))
            time.sleep(0.001)
        plt.xlabel('Shaping time');plt.ylabel(' '.join([ylabel, 'locMax']))
        plt.xticks(ticks=df['ShapingTime'].unique(), labels=df['ShapingTime'].unique())
        plt.legend()
        plt.title('_'.join([addToTitle, 'shapingTime_vs_' + ylabel + 'locMax', BL]))
        plt.savefig(os.path.join(outputDir, '_'.join(['shapingTime_vs_' + ylabel + 'locMax', BL]) + '.png'))

# plot std/mean vs shaping time
def plot_stdDIVmean_vs_shapingTime(path_to_csv='', BL='200mV', outputDir='',
                                    ylabel='pedestal'):
    dataFrame = pd.read_csv(path_to_csv)
    dataFrame['BL'] = dataFrame['BL'].apply(lambda x : x[:-2])
    condition = (dataFrame['BL']==BL)
    dataFrame = convert_Gain_to_float(dataFrame)
    Gain = dataFrame[condition]['Gain'].unique()
    #-> dataFrame for BL==200mV
    df = dataFrame[condition]
    # -> shaping time to float
    df = convert_Timing_to_float(df)
    df['ratio_std_mean'] = df['std'] / df['mean']
    plt.figure(figsize=(12, 7))
    for gain in Gain:
        plt.errorbar(x=df[df['Gain']==gain]['ShapingTime'],# y=df[df['Gain']==gain]['mean'],
                    y=df[df['Gain']==gain]['ratio_std_mean'],
                    label= '_'.join([BL, str(gain) + 'mV/fC']))
    plt.xticks(ticks=df['ShapingTime'].unique(), labels=df['ShapingTime'].unique())
    plt.legend()
    plt.show()
#
#
#
def onedigit_hex_below16(onedigit='a'):
    h1 = 0
    if onedigit == 'a':
        h1 = 10
    elif onedigit == 'b':
        h1 = 11
    elif onedigit == 'c':
        h1 = 12
    elif onedigit == 'd':
        h1 = 13
    elif onedigit == 'e':
        h1 = 14
    elif onedigit == 'f':
        h1 = 15
    else:
        h1 = int(onedigit)
    return h1

def hex2dec(hexvalue='00'):
        '''
        Convert hex number to decimal number
        '''
        h1 = onedigit_hex_below16(onedigit=hexvalue[0])
        h2 = onedigit_hex_below16(onedigit=hexvalue[1])
        decvalue = h1 * 16 + h2 * 1
        return decvalue

# if decvalue < 16, right_digit is returned by the function below and left_digit is zero
def dec_is_lessthan16(decvalue=0):
    hexvalue = ''
    if decvalue < 10:
        hexvalue = str(decvalue)
    elif decvalue==10:
        hexvalue = 'a'
    elif decvalue==11:
        hexvalue = 'b'
    elif decvalue==12:
        hexvalue = 'c'
    elif decvalue==13:
        hexvalue = 'd'
    elif decvalue==14:
        hexvalue = 'e'
    elif decvalue==15:
        hexvalue = 'f'
    return hexvalue

def dec2hex(decvalue=0):
    hexvalue = ''
    if decvalue < 16:
        hexvalue = '0' + dec_is_lessthan16(decvalue=decvalue)
    else:
        leftdigit = decvalue // 16
        rightdigit = decvalue % 16
        hex_left = dec_is_lessthan16(decvalue=leftdigit)
        hex_right = dec_is_lessthan16(decvalue=rightdigit)
        hexvalue = hex_left + hex_right
    return hexvalue

# ASICDAC_CALI analysis
class ASICDAC_CALI:
    def __init__(self, inputdir):
        self.inputdir = inputdir
        self.usefuldir = []
        self.alldata = []
        self.filename = ''
        self.listh5_filenames = [] # to verify that all bin files have the same h5 files
        # need to set self.data to list when dealing with all the data folders
        # self.data = dict()
        # self.h5keys = []
        # self.keyswithconfig = []
        # self.filename = 'logs_tm007.bin'
        
    def select_usefuldir(self, tm=7, temperature='LN'):
        '''
        Select folders having tm==7
        '''
        listdir = os.listdir(self.inputdir)
        self.filename = 'logs_tm00' + str(tm) + '.bin'
        print('Select only the directories meeting our requirements.............')
        for DIR in tqdm(listdir):
            if temperature in DIR:
                path_to_dir = os.path.join(self.inputdir, DIR)
                if self.filename in os.listdir(path_to_dir):
                    self.usefuldir.append(path_to_dir)
                # time.sleep(0.0001)

    def listallh5files(self, DACvalue='00'):
        '''
        List all h5 files to be used.
        '''
        for f in os.listdir(os.path.join(self.usefuldir[0], 'ASICDAC_CALI')):
            if ('.h5' in f) & ('_CD0x' not in f) & (('0x'+DACvalue) in f):
                self.listh5_filenames.append(f)

    def read_bin(self, indexDir=0):
        '''Reads the bin file'''
        path_to_file = os.path.join(self.usefuldir[indexDir], self.filename)
        with open(path_to_file, 'rb') as fp:
            return pickle.load(fp)
    
    def geth5keys(self, dataDict: dict, withCD=False):
        print('Getting all the h5 keys..................')
        h5keys = []
        for key in tqdm(dataDict.keys()):
            if '.h5' in key:
                if withCD & ('_CD0x' in key):
                        h5keys.append(key)
                else:
                    if '_CD0x' not in key:
                        h5keys.append(key)
                # time.sleep(0.00005)
        return h5keys
        
    def geth5keys_forDAC(self, h5keys=[], DACvalue='00'):
        '''
        Knowing the DACvalue (hex number), this function returns the corresponding h5 keys from self.h5keys
        '''
        print('DAC value (decimal) = {}\n'.format(hex2dec(hexvalue=DACvalue)))
        DAC_str = 'ASICDAC0x' + DACvalue
        listKeys = []
        print('Selecting h5 keys corresponding to the DACvalue.....')
        for key in tqdm(h5keys):
            if DAC_str in key:
                listKeys.append(key)
            # time.sleep(0.0001)
        return listKeys

    def getData_forh5Key(self, data_dict: dict, h5key: str, dataType='pedestal'):
        '''
        Get data from the dictionary self.data using a h5key.
        '''
        indexData = -1
        if dataType=='RMS':
            # 0
            indexData = 0
        elif dataType=='pedestal':
            # 1
            indexData = 1
        elif dataType=='pospeak':
            # 2
            indexData = 2
        elif dataType=='negpeak':
            # 3
            indexData = 3
        elif dataType=='onewaveform':
            # 4
            indexData = 4
        elif dataType=='avgwaveform':
            # 5
            indexData = 5
        if indexData != -1:
            # print('data = ', data_dict[h5key][indexData])
            return data_dict[h5key][indexData]
        else:
            return 'no corresponding data'

    def getAllDataFromFolders(self, dataType='pedestal', list_pathToFolders=[],
                             oneh5file='', DACvalue='00'):
        '''
        Given the list of the path_to_folders, concatenate data of the same types.
        '''
        print('Getting all data................')
        tmp_alldata = []
        for indexDir, DIR in tqdm(enumerate(list_pathToFolders)):
            currData_dict = self.read_bin(indexDir=indexDir)
            h5keys = self.geth5keys(dataDict=currData_dict, withCD=False)
            h5keys_DAC = self.geth5keys_forDAC(h5keys=h5keys, DACvalue=DACvalue)
            for key in h5keys_DAC:
                if oneh5file in key:
                    # continue
                    oneData = self.getData_forh5Key(data_dict=currData_dict, h5key=key, dataType=dataType)
                    tmp_alldata += oneData
        self.alldata = tmp_alldata
            # time.sleep(0.00005)
    
    def filename_forDec(self, config='', dec_dacval=0):
                hex_dac = dec2hex(decvalue=dec_dacval)
                config += ('_ASICDAC0x' + hex_dac + '.h5')
                return config

    def _plot(self):
        outputdir = 'asicdac_pospeak'
        # indexh5 = 0
        DACvalue = '00'
        self.select_usefuldir(tm=7, temperature='LN')
        self.listallh5files(DACvalue=DACvalue)
        configs = [f.split('_ASICDAC')[0] for f in self.listh5_filenames]
        for config in configs:
            all_dacValues = [i for i in range(60) if i%4==0]
            plt.figure(figsize=(12, 7))
            for dacval in all_dacValues:
                filename = self.filename_forDec(config=config, dec_dacval=dacval)
                hex_dac = dec2hex(decvalue=dacval)
                self.getAllDataFromFolders(dataType='pospeak', list_pathToFolders=self.usefuldir,
                                            oneh5file=filename, DACvalue=hex_dac)
                plt.plot(self.alldata, label='{}'.format(dacval))
            plt.title(config)
            plt.legend()
            plt.savefig(os.path.join(outputdir, config + '.png'))
