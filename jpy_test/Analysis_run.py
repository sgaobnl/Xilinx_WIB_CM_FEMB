from operator import index
import Analysis_FEMB_QC

if __name__ == '__main__':
    Analysis_FEMB_QC.save_gaussianInfo(sourceMainDir='D:/IO-1865-1C/QC/analysis/LN',
                                     dataType='Pedestal', outputDir='D:/IO-1865-1C/QC/analysis/LN/plots/Pedestal',
                                     nstd=3, nbins=50, skewed=True)
    
    Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='D:/IO-1865-1C/QC/analysis/LN/plots/Pedestal/gaussian_Pedestal.csv',
                                             BL='200mV',
                                             outputDir='D:/IO-1865-1C/QC/analysis/LN/plots/Pedestal',
                                             ylabel='Pedestal',
                                             addToTitle='', skewed=True)
    Analysis_FEMB_QC.plot_mean_vs_ShapingTime(path_to_csv='D:/IO-1865-1C/QC/analysis/LN/plots/Pedestal/gaussian_Pedestal.csv',
                                             BL='900mV',
                                             outputDir='D:/IO-1865-1C/QC/analysis/LN/plots/Pedestal',
                                             ylabel='Pedestal',
                                             addToTitle='', skewed=True)
    # asicdac = Analysis_FEMB_QC.ASICDAC_CALI(inputdir='../data/data_OK')
    # asicdac._plot()
    #Analysis_FEMB_QC.plot_stdDIVmean_vs_shapingTime(path_to_csv='norm_skewed_fit/pedestal_test_skewed/gaussian_pedestal.csv')
