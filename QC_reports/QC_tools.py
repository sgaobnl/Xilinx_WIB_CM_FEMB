import matplotlib.pyplot as plt
import numpy as np

class QC_tools:
#    def __init__(self):


    def FEMB_SUB_PLOT(self, ax, x, y, title, xlabel, ylabel, color='b', marker='.', atwinx=False, ylabel_twx = "", e=None):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        if (atwinx):
            ax.errorbar(x,y,e, marker=marker, color=color)
            y_min = int(np.min(y))-1000
            y_max = int(np.max(y))+1000
            ax.set_ylim([y_min, y_max])
            ax2 = ax.twinx()
            ax2.set_ylabel(ylabel_twx)
            ax2.set_ylim([int((y_min/16384.0)*2048), int((y_max/16384.0)*2048)])
        else:
            ax.plot(x,y, marker=marker, color=color)

    def FEMB_CHK_PLOT(self, chn_rmss,chn_peds, chn_pkps, chn_pkns, chn_onewfs, chn_avgwfs, title):
    #    import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(10,6))
        ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
        ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
        ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
        ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
        chns = range(128)
        self.FEMB_SUB_PLOT(ax1, chns, chn_rmss, title="RMS Noise", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
        self.FEMB_SUB_PLOT(ax2, chns, chn_peds, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
        self.FEMB_SUB_PLOT(ax2, chns, chn_pkps, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='b', marker='.')
        self.FEMB_SUB_PLOT(ax2, chns, chn_pkns, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='g', marker='.')
        for chni in chns:
            ts = 100
            x = (np.arange(ts)) * 0.5
            y3 = chn_onewfs[chni][25:ts+25]
            y4 = chn_avgwfs[chni][25:ts+25]
            self.FEMB_SUB_PLOT(ax3, x, y3, title="Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))
            self.FEMB_SUB_PLOT(ax4, x, y4, title="Averaging(100 Cycles) Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))

        fig.suptitle(title)
        plt.tight_layout( rect=[0.05, 0.05, 0.95, 0.95])
        return fig

    def Config_Plot(self, xx, yy, xlabels, var, title):
        fig_V1,axes_V1 = plt.subplots(3,2,figsize=(20,10))
        fig_V2,axes_V2 = plt.subplots(3,2,figsize=(20,10))
        fig_V3,axes_V3 = plt.subplots(3,2,figsize=(20,10))

        cm = plt.get_cmap('tab20')

        for i in range(8):  # per chip
            for j in range(16):
                ch = 16*i+j

                if i<3:
                   axes_V1[i,0].plot(xx,yy[0][i][j],label='ch{}'.format(j),color=cm(j/16))
                   axes_V1[i,1].plot(xx,yy[1][i][j],label='ch{}'.format(j),color=cm(j/16))
                if i>=3 and i<6:
                   axes_V2[i-3,0].plot(xx,yy[0][i][j],label='ch{}'.format(j),color=cm(j/16))
                   axes_V2[i-3,1].plot(xx,yy[1][i][j],label='ch{}'.format(j),color=cm(j/16))
                if i>=6:
                   axes_V3[i-6,0].plot(xx,yy[0][i][j],label='ch{}'.format(j),color=cm(j/16))
                   axes_V3[i-6,1].plot(xx,yy[1][i][j],label='ch{}'.format(j),color=cm(j/16))

            if i<3:
               axes_V1[i,0].text(.2,.9,'chip {} @900mV BL'.format(i),transform=axes_V1[i,0].transAxes)
               axes_V1[i,1].text(.2,.9,'chip {} @200mv BL'.format(i),transform=axes_V1[i,1].transAxes)
            if i>=3 and i<6:
               axes_V2[i-3,0].text(.2,.9,'chip {} @900mV BL'.format(i),transform=axes_V2[i-3,0].transAxes)
               axes_V2[i-3,1].text(.2,.9,'chip {} @200mV BL'.format(i),transform=axes_V2[i-3,1].transAxes)
            if i>=6:
               axes_V3[i-6,0].text(.2,.9,'chip {} @900mV BL'.format(i),transform=axes_V3[i-6,0].transAxes)
               axes_V3[i-6,1].text(.2,.9,'chip {} @200mV BL'.format(i),transform=axes_V3[i-6,1].transAxes)

        axes_V3[2,0].axis('off')
        axes_V3[2,1].axis('off')
        axes_V1[0,0].legend(ncol=8, bbox_to_anchor=(0.05, 1.2), loc='upper left', borderaxespad=0.)
        axes_V2[0,0].legend(ncol=8, bbox_to_anchor=(0.05, 1.2), loc='upper left', borderaxespad=0.)
        axes_V3[0,0].legend(ncol=8, bbox_to_anchor=(0.05, 1.2), loc='upper left', borderaxespad=0.)
        fig_V1.suptitle('{} vs. configurations'.format(var), fontsize=16)
        fig_V2.suptitle('{} vs. configurations'.format(var), fontsize=16)
        fig_V3.suptitle('{} vs. configurations'.format(var), fontsize=16)

        plt.setp(axes_V1, xticks=xx, xticklabels=xlabels)
        plt.setp(axes_V2, xticks=xx, xticklabels=xlabels)
        plt.setp(axes_V3, xticks=xx, xticklabels=xlabels)
        fig_V1.subplots_adjust(hspace = 0.2,wspace=0.05)
        fig_V2.subplots_adjust(hspace = 0.2,wspace=0.05)
        fig_V3.subplots_adjust(hspace = 0.2,wspace=0.05)
        fig_V1.savefig('{}_V1_{}.png'.format(title,var))
        fig_V2.savefig('{}_V2_{}.png'.format(title,var))
        fig_V3.savefig('{}_V3_{}.png'.format(title,var))

    def Current_Plot(self,xx, yy, xlabels, var):
        fig,axes = plt.subplots(3,3,figsize=(10,12))
        cm = plt.get_cmap('tab20')

        for i in range(8):  # per chip
            for j in range(16):
                ch = 16*i+j
                axes[i//3,i%3].plot(xx,yy[i][j],label='ch{}'.format(j),color=cm(j/16))

            axes[i//3,i%3].text(.2,.9,'chip {}'.format(i),transform=axes[i//3,i%3].transAxes)

        axes[2,2].axis('off')
        axes[2,1].legend(ncol=3, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        fig.suptitle('{} vs. current'.format(var), fontsize=16)
        plt.setp(axes, xticks=xx, xticklabels=xlabels)
        fig.savefig('CHK_current_{}.png'.format(var))

