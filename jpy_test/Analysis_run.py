#*****************************************************************
#   Author: Rado
#   email: radofana@gmail.com
#   last modification: September 26, 2022
#****************************************************************
from operator import index
import Analysis_FEMB_QC

if __name__ == '__main__':
    # correct csv files for RMS by removing femb 24, 55, 07 and 27
    femb_list = [75, 24, 55, 7, 27]
    temperatures = ['LN', 'RT']
    for T in temperatures:
        path_to_csvfiles = 'D:/IO-1865-1C/QC/analysis/' + T
        output_path = 'D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV'
        Analysis_FEMB_QC.saveCorrectedCSV(path_to_csv=path_to_csvfiles, femb_list=femb_list, output_path=output_path, datanames=['Pedestal', 'RMS'])
    datanames = ['Pedestal', 'RMS']
    for T in temperatures:
        for dataname in datanames:
            Analysis_FEMB_QC.save_gaussianInfo(sourceMainDir='D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV',
                                             dataType=dataname, outputDir='D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV/plots/'+ dataname,
                                          nstd=3, nbins=60, skewed=True)
        
            Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV/plots/'+dataname+'/gaussian_'+dataname+'.csv',
                                                     BL='200mV',
                                                     outputDir='D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV/plots/'+dataname,
                                                     ylabel=dataname,
                                                     addToTitle='', skewed=True)
            Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV/plots/'+ dataname + '/gaussian_'+ dataname +'.csv',
                                                     BL='900mV',
                                                     outputDir='D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV/plots/' + dataname,
                                                     ylabel=dataname,
                                                     addToTitle='', skewed=True)
    # asicdac = Analysis_FEMB_QC.ASICDAC_CALI(inputdir='../data/data_OK')
    # asicdac._plot()
    #Analysis_FEMB_QC.plot_stdDIVmean_vs_shapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv')
