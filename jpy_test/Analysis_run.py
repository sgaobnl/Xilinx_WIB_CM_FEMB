#*****************************************************************
#   Author: Rado
#   email: radofana@gmail.com
#   last modification: October 24, 2022
#****************************************************************
from operator import index
import Analysis_FEMB_QC

if __name__ == '__main__':
    # correct csv files for RMS by removing femb 24, 55, 07 and 27
    # femb_list = [75, 24, 55, 7, 27]
    # temperatures = ['LN', 'RT']
    # for T in temperatures:
    #     path_to_csvfiles = 'D:/IO-1865-1C/QC/analysis/' + T
    #     output_path = 'D:/IO-1865-1C/QC/analysis/'+ T +'/correctedCSV'
    #     Analysis_FEMB_QC.saveCorrectedCSV(path_to_csv=path_to_csvfiles, femb_list=femb_list, output_path=output_path, datanames=['Pedestal', 'RMS'])
    # datanames = ['Pedestal', 'RMS']
    # for T in temperatures:
    #     for dataname in datanames:
    #         # Analysis_FEMB_QC.save_gaussianInfo(sourceMainDir='../../../WIB_SW_BNL/data/analysis/'+T+'/correctedCSV_rms_pedestal',
    #         #                                  dataType=dataname, outputDir='../../../WIB_SW_BNL/data/analysis/'+ T +'/correctedCSV_rms_pedestal/plots/'+ dataname,
    #         #                               nstd=3, nbins=60, skewed=True)
    #         ylim200, ylim900 = [], []
    #         if dataname=='Pedestal':
    #             ylim200 = [500, 1650]
    #             ylim900 = [7750, 9500]
    #         elif dataname=='RMS':
    #             ylim200 = [0, 55]
    #             ylim900 = [0, 55]

    #         Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='../../../WIB_SW_BNL/data/analysis/'+ T +'/correctedCSV_rms_pedestal/plots/'+dataname+'/gaussian_'+dataname+'.csv',
    #                                                  BL='200mV',
    #                                                  outputDir='../../../WIB_SW_BNL/data/analysis/'+ T +'/correctedCSV_rms_pedestal/plots/'+dataname,
    #                                                  ylabel=dataname,
    #                                                  addToTitle='', skewed=True, ylim=ylim200)
    #         Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='../../../WIB_SW_BNL/data/analysis/'+ T +'/correctedCSV_rms_pedestal/plots/'+ dataname + '/gaussian_'+ dataname +'.csv',
    #                                                  BL='900mV',
    #                                                  outputDir='../../../WIB_SW_BNL/data/analysis/'+ T +'/correctedCSV_rms_pedestal/plots/' + dataname,
    #                                                  ylabel=dataname,
    #                                                  addToTitle='', skewed=True, ylim=ylim900)
    #
    #
    # Analysis_FEMB_QC.save_gaussianInfo(sourceMainDir='distributionPNG/csv',
    #                                 dataType='pedestal', outputDir='norm_skewed_fit/pedestal_test_skewed',
    #                                 nstd=3, nbins=50, skewed=True)
    
    # Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='norm_skewed_fit/RMS_test_skewed/gaussian_RMS.csv',
    #                                         BL='200mV',
    #                                         outputDir='norm_skewed_fit/RMS_test_skewed',
    #                                         ylabel='RMS',
    #                                         addToTitle='', skewed=True,
    #                                         ylim=[0, 25])
    # Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='norm_skewed_fit/RMS_test_skewed/gaussian_RMS.csv',
    #                                         BL='900mV',
    #                                         outputDir='norm_skewed_fit/RMS_test_skewed',
    #                                         ylabel='RMS',
    #                                         addToTitle='', skewed=True, ylim=[0, 25])

    # asicdac = Analysis_FEMB_QC.ASICDAC_CALI(inputdir='../data/data_OK')
    # asicdac._plot()
    #Analysis_FEMB_QC.plot_stdDIVmean_vs_shapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv')
    Analysis_FEMB_QC.separateCSV_foreachFEMB(path_to_csv='../../../WIB_SW_BNL/WIB_SW_BNL/results/PWR_RMS_Pedestal/LN/correctedCSV_rms_pedestal',
                                            output_path='../../../WIB_SW_BNL/WIB_SW_BNL/results/LN', datanames=['Pedestal', 'RMS'])