import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from fpdf import FPDF
from PyPDF2 import PdfMerger
import QC_tools

class LArASIC_check:
    def __init__(self, folder,runNo,temp):
        self.folder=folder
        self.runNo=runNo
        self.temp=temp

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

    def Config_Plot(self, xx, yy, xlabels, var):
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

        plt.setp(axes_V1, xticks=range(16), xticklabels=xlabels)
        plt.setp(axes_V2, xticks=range(16), xticklabels=xlabels)
        plt.setp(axes_V3, xticks=range(16), xticklabels=xlabels)
        fig_V1.subplots_adjust(hspace = 0.2,wspace=0.05)
        fig_V2.subplots_adjust(hspace = 0.2,wspace=0.05)
        fig_V3.subplots_adjust(hspace = 0.2,wspace=0.05)
        fig_V1.savefig('CHK_V1_{}.png'.format(var))
        fig_V2.savefig('CHK_V2_{}.png'.format(var))
        fig_V3.savefig('CHK_V3_{}.png'.format(var))
        

    def Config_check(self):

        fp = self.folder + "logs_tm005.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        #########################################
        lkc = ["100pA", "500pA", "1nA",  "5nA"]
        I_rms = []
        I_pkp = []
        I_pkn = []
        I_ped = []
        for i in range(4):
            I_rms.append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}.h5'.format(self.runNo,self.temp,lkc[i])][0])
            I_ped.append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}.h5'.format(self.runNo,self.temp,lkc[i])][1])
            I_pkp.append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}.h5'.format(self.runNo,self.temp,lkc[i])][2])
            I_pkn.append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}.h5'.format(self.runNo,self.temp,lkc[i])][3])

        xx=range(4)

        rms_list = []
        pkp_list = []
        pkn_list = []
        ped_list = []

        for i in range(8):  # per chip
            rms_list.append([])
            ped_list.append([])
            pkp_list.append([])
            pkn_list.append([])
            for j in range(16):
                ch = 16*i+j
                tmp_list = [I_rms[0][ch],I_rms[1][ch],I_rms[2][ch],I_rms[3][ch]]
                rms_list[i].append(tmp_list)

                tmp_list = [I_ped[0][ch],I_ped[1][ch],I_ped[2][ch],I_ped[3][ch]]
                ped_list[i].append(tmp_list)

                tmp_list = [I_pkp[0][ch],I_pkp[1][ch],I_pkp[2][ch],I_pkp[3][ch]]
                pkp_list[i].append(tmp_list)

                tmp_list = [I_pkn[0][ch],I_pkn[1][ch],I_pkn[2][ch],I_pkn[3][ch]]
                pkn_list[i].append(tmp_list)

        self.Current_Plot(xx, rms_list, lkc, 'RMS')
        self.Current_Plot(xx, ped_list, lkc, 'Ped')
        self.Current_Plot(xx, pkp_list, lkc, 'Peak_P')
        self.Current_Plot(xx, pkn_list, lkc, 'Peak_N')

        #######################################################
        sncs = ["900mVBL", "200mVBL"]
        sgs = ["4_7mVfC", "7_8mVfC", "14_0mVfC", "25_0mVfC" ]
        sgs_x = ["4.7mVfC", "7.8mVfC", "14.0mVfC", "25.0mVfC" ]
        sts = ["0_5us", "1_0us",  "2_0us", "3_0us"]
        sts_x = ["0.5", "1",  "2", "3"]

        V_rms = []
        V_ped = []
        V_pkp = []
        V_pkn = []

        for i in range(2):
            V_rms.append([])
            V_ped.append([])
            V_pkp.append([])
            V_pkn.append([])
            for j in range(4):
                V_rms[i].append([])
                V_ped[i].append([])
                V_pkp[i].append([])
                V_pkn[i].append([])
                for k in range(4):
                    V_rms[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][0])
                    V_ped[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][1])
                    V_pkp[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][2])
                    V_pkn[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][3])

        V_rms_list=[[],[]]
        V_ped_list=[[],[]]
        V_pkp_list=[[],[]]
        V_pkn_list=[]

        for i in range(8):  # per chip
            V_rms_list[0].append([])
            V_rms_list[1].append([])

            V_ped_list[0].append([])
            V_ped_list[1].append([])
            
            V_pkp_list[0].append([])
            V_pkp_list[1].append([])

            V_pkn_list.append([])
            for j in range(16):
                ch = 16*i+j
                xx=range(16)
                V_rms_list[0][i].append([])
                V_rms_list[1][i].append([])
                
                V_ped_list[0][i].append([])
                V_ped_list[1][i].append([])
                
                V_pkp_list[0][i].append([])
                V_pkp_list[1][i].append([])
                
                V_pkn_list[i].append([])

                for ix in range(4):
                    for iy in range(4):
                        V_rms_list[0][i][j].append(V_rms[0][ix][iy][ch])
                        V_rms_list[1][i][j].append(V_rms[1][ix][iy][ch])

                        V_ped_list[0][i][j].append(V_ped[0][ix][iy][ch])
                        V_ped_list[1][i][j].append(V_ped[1][ix][iy][ch])

                        V_pkp_list[0][i][j].append(V_pkp[0][ix][iy][ch])
                        V_pkp_list[1][i][j].append(V_pkp[1][ix][iy][ch])

                        V_pkn_list[i][j].append(V_pkn[0][ix][iy][ch])

        xlabels=[]
        for ix in range(4):
            xlabels.append('{}\n{}'.format(sgs_x[ix],sts_x[0]))
            for iy in range(1,4):
                xlabels.append('\n{}'.format(sts_x[iy]))

        xlabels[15]='{}us'.format(xlabels[15])

        self.Config_Plot(range(16), V_rms_list, xlabels, 'RMS')
        self.Config_Plot(range(16), V_ped_list, xlabels, 'Ped')
        self.Config_Plot(range(16), V_pkp_list, xlabels, 'Peak_P')

        fig,axes = plt.subplots(3,3,figsize=(15,12))
        cm = plt.get_cmap('tab20')

        for i in range(8):  # per chip
            for j in range(16):
                ch = 16*i+j
                axes[i//3,i%3].plot(range(16),V_pkn_list[i][j],label='ch{}'.format(j),color=cm(j/16))

            axes[i//3,i%3].text(.2,.9,'chip {}'.format(i),transform=axes[i//3,i%3].transAxes)

        axes[2,2].axis('off')
        axes[2,1].legend(ncol=2, bbox_to_anchor=(1.1, 1), loc='upper left', borderaxespad=0.)
        fig.suptitle('Peak_N vs. configurations @900mVBL', fontsize=16)
        plt.setp(axes, xticks=range(16), xticklabels=xlabels)
        fig.savefig('CHK_Peak_N.png')

    def RMS_check(self):
        fp = self.folder + "logs_tm005.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        sncs = ["900mVBL", "200mVBL"]
        sgs = ["4_7mVfC", "7_8mVfC", "14_0mVfC", "25_0mVfC" ]
        sgs_x = ["4.7mVfC", "7.8mVfC", "14.0mVfC", "25.0mVfC" ]
        sts = ["0_5us", "1_0us",  "2_0us", "3_0us"]
        sts_x = ["0.5", "1",  "2", "3"]

        V_rms = []
        V_ped = []
        V_pkp = []
        V_pkn = []

        for i in range(2):
            V_rms.append([])
            V_ped.append([])
            V_pkp.append([])
            V_pkn.append([])
            for j in range(4):
                V_rms[i].append([])
                V_ped[i].append([])
                V_pkp[i].append([])
                V_pkn[i].append([])
                for k in range(4):
                    V_rms[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][0])
                    V_ped[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][1])
                    V_pkp[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][2])
                    V_pkn[i][j].append(logs['D:/IO_1826_1B/QC/FEMB{}_{}_150pF/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.runNo,self.temp,sncs[i], sgs[j], sts[k])][3])



if __name__=='__main__':

    runNo = 352
    temp='LN'
    folder = '/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/FEMB_QC_data/FEMB{}_LN_150pF/'.format(runNo)
    femb = LArASIC_check(folder, runNo, temp)
    femb.Config_check()

