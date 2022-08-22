#-----------------------------------------------------------
# 	Author: Rado
#	email: radofana@gmail.com
#	Last modification: August 22, 2022
#-----------------------------------------------------------
'''
	STRUCTURE OF THE DATA data_log[keys_data[0]]:
		0: RMS
		1: Pedestal value
		2: Positive peak
		3: Negative Peak
		4: One waveform
		5: Average waveform
	INPUT:
		Default input should be in a folder named data
	OUTPUT:
		The output of this code will be .png files stored in a folder named distributionPNG
'''

import pickle
import os
import matplotlib.pyplot as plt

def getFEMB_dir(mainDir):
    # get a list of the FEMB directories
    return [os.path.join(mainDir, f) for f in os.listdir(mainDir)]

def get_bin_list(source_DIR):
    '''
    This function gets the list of files having the extension '.bin'
    in the source_DIR which is a path to a FEMB data
    '''
    files = []
    for f in os.listdir(source_DIR):
        if '.bin' in f:
            files.append(f)
    return files

def read_bin(file_path):
    '''
    This function reads file_path which has the extension '.bin'
    '''
    with open(file_path, 'rb') as fp:
        return pickle.load(fp)

def get_keys(data_pickle, h5='h5'):
    '''
    This function returns the keys in the dictionary as a list
    '''
    keys = []
    ish5 = (h5=='h5')
    if ish5:
        for l in list(data_pickle.keys()):
            if '.h5' in l:
                keys.append(l)
    else:
        keys = list(data_pickle.keys())
    return keys

def get_h5filenames(mainDir='../data', indexBin=5):
    femb = getFEMB_dir(mainDir)[0]
    oneBin = get_bin_list(femb)[indexBin]
    binDataLog = read_bin(os.path.join(femb, oneBin))
    keys = get_keys(binDataLog,'h5')
    # keys has to be a list to be able to use this function
    filenames = []
    for f in keys:
        f_split = f.split('/')
        # normally the filename is at the end of the list generated
        # let's use the index -1 to get the element located at the end of the list
        filenames.append(f_split[-1])
    return filenames


def printInfo(label, info):
    print('*' * 100)
    print('*', label, ' : ')
    if type(info)==list:
        for f in info:
            print('*\t', f,'\n')
    else:
        print('*\t', info, '\n')
    print('*' * 100)

def exploreFEMBData(mainDir, indexFEMB):
    # FEMBs
    fembs = getFEMB_dir(mainDir)
    printInfo('FEMB directories', fembs)
    # list of bin files for the first FEMB folder
    bin_list = get_bin_list(fembs[0])
    printInfo('List of bin files', bin_list)
    # get keys from the one bin data
    data_log = read_bin(os.path.join(fembs[0], bin_list[5]))
    data_keys = get_keys(data_log, 'h5')
    printInfo('Keys corresponding to the femb', data_keys)
    #-> we can get data by writing: data_log[data_keys[indexKey]][indexData]
    #print(bin_list[5], ' - logs_tm006.bin')
    
def getDistribution(mainDir='../data', outputDir='distributionPNG', indexh5=0, indexBin=5, indexData=0, histBin=100):
    dataName = {0: 'RMS',
               1: 'pedestal',
               2: 'positive_peak',
               3: 'negative_peak',
               4: 'one_waveform',
               5: 'average_waveform'}
    printInfo('dataname', dataName[indexData])
    ## try to create a folder named dataName[indexData]
    try:
        os.mkdir(os.path.join(outputDir, dataName[indexData]))
    except:
        pass
    # get h5 key corresponding to indexh5
    h5_filename = get_h5filenames()[indexh5]
    printInfo('Name of the h5 file', h5_filename)
    
    # set variable to store the data
    dataVar = []
    
    ## get FEMBs dir
    fembs = getFEMB_dir(mainDir)
    
    for femb in fembs:
        # get list of bin files
        bin_list = get_bin_list(femb)

        if 'logs_tm006.bin' in bin_list:
        	printInfo('FEMB folder', femb)
	        printInfo('Name of the bin file', bin_list[indexBin])
	        # read the data corresponding to indexBin
	        data_log = read_bin(os.path.join(femb, bin_list[indexBin]))
	        dataKey = get_keys(data_log, 'h5')[indexh5] # get one key corresponding to indexh5
	        # printInfo('dataKey', dataKey)
	        # append data corresponding to indexData to the list dataVar
	        dataVar += data_log[dataKey][indexData]

    h5Name_split = h5_filename.split('.')[0].split('_')
    h5Name_split[0] = dataName[indexData]
    title = '_'.join(h5Name_split)

    plt.figure(figsize=(15, 7))
    plt.hist(dataVar, bins=histBin)
    plt.xlabel(dataName[indexData], fontsize='14'); plt.ylabel('#')
    plt.title(title, fontsize='14')
    plt.savefig(os.path.join(outputDir, dataName[indexData], dataName[indexData]+
                                        '_'+
                                         h5_filename.split('.')[0]+
                                         '.png'))

## MAIN FUNCTION
if __name__ == '__main__':
	## try to create a folder named distributionPNG
	# try:
	# 	os.mkdir('distributionPNG')
	# except:
	# 	pass

	dataIndices = [0, 1]

	# path to the data source
	mainDir = 'D:/IO_1826_1B/QC'

	# path to the output png files
	outputDir = 'I:/IO-1826-1B_QC/QC_general'

	printInfo('mainDir', mainDir)
	printInfo('outputDir', outputDir)

	h5_list = get_h5filenames(mainDir=mainDir, indexBin=5)
	for indexData in dataIndices:
	    for indexh5, h5 in enumerate(h5_list):
	        getDistribution(mainDir=mainDir, outputDir=outputDir, indexh5=indexh5, indexData=indexData, indexBin=5, histBin=50)