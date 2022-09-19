from operator import index
import Analysis_FEMB_QC

if __name__ == '__main__':
    # Analysis_FEMB_QC.save_gaussianInfo(sourceMainDir='distributionPNG/csv',
    #                                 dataType='pedestal', outputDir='norm_skewed_fit/pedestal_test_skewed',
    #                                 nstd=3, nbins=50, skewed=True)
    
    # Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv',
    #                                         BL='200mV',
    #                                         outputDir='norm_skewed_fit/pedestal_test_skewed',
    #                                         ylabel='pedestal',
    #                                         addToTitle='', skewed=True)
    # Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv',
    #                                         BL='900mV',
    #                                         outputDir='norm_skewed_fit/pedestal_test_skewed',
    #                                         ylabel='pedestal',
    #                                         addToTitle='', skewed=True)
    # asicdac = Analysis_FEMB_QC.ASICDAC_CALI(inputdir='../data/data_OK')
    # asicdac._plot()
    Analysis_FEMB_QC.plot_stdDIVmean_vs_shapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv')