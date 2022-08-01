import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from fpdf import FPDF
from PyPDF2 import PdfMerger
import QC_tools

class LArASIC_check:
    def __init__(self, folder,runNo,temp,adir):
        self.folder=folder
        self.runNo=runNo
        self.temp=temp
        self.adir=adir
        self.tools = QC_tools.QC_tools()

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
            I_rms.append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}.h5'.format(self.adir,lkc[i])][0])
            I_ped.append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}.h5'.format(self.adir,lkc[i])][1])
            I_pkp.append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}.h5'.format(self.adir,lkc[i])][2])
            I_pkn.append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}.h5'.format(self.adir,lkc[i])][3])

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

        self.tools.Current_Plot(xx, rms_list, lkc, 'RMS')
        self.tools.Current_Plot(xx, ped_list, lkc, 'Ped')
        self.tools.Current_Plot(xx, pkp_list, lkc, 'Peak_P')
        self.tools.Current_Plot(xx, pkn_list, lkc, 'Peak_N')

        #######################################################
        sncs = ["900mVBL", "200mVBL"]
        sgs = ["4_7mVfC", "7_8mVfC", "14_0mVfC", "25_0mVfC" ]
        sgs_x = ["4.7mVfC", "7.8mVfC", "14mVfC", "25mVfC" ]
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
                    V_rms[i][j].append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.adir,sncs[i], sgs[j], sts[k])][0])
                    V_ped[i][j].append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.adir,sncs[i], sgs[j], sts[k])][1])
                    V_pkp[i][j].append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.adir,sncs[i], sgs[j], sts[k])][2])
                    V_pkn[i][j].append(logs['D:/IO_1826_1B/QC/{}/CHK/CHK_response_SE_{}_{}_{}.h5'.format(self.adir,sncs[i], sgs[j], sts[k])][3])

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
        title='CHK'
        self.tools.Config_Plot(range(16), V_rms_list, xlabels, 'RMS', title)
        self.tools.Config_Plot(range(16), V_ped_list, xlabels, 'Ped', title)
        self.tools.Config_Plot(range(16), V_pkp_list, xlabels, 'Peak_P', title)

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
        fp = self.folder + "logs_tm006.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)


        sncs = ["900mVBL", "200mVBL"]
        sts = ["0_5us", "1_0us",  "2_0us", "3_0us"]
        sts_x = ["0.5", "1",  "2", "3"]

        if self.temp=='RT':
            sgs = ["14_0mVfC"]
            sgs_x = ["14mVfC"]
        else:
            sgs = ["4_7mVfC", "7_8mVfC", "14_0mVfC", "25_0mVfC" ]
            sgs_x = ["4.7mVfC", "7.8mVfC", "14mVfC", "25mVfC" ]

        rms = []

        for i in range(2):
            rms.append([])
            for j in range(len(sgs)):
                rms[i].append([])
                for k in range(4):
                    rms[i][j].append(logs['D:/IO_1826_1B/QC/{}/RMS/RMS_{}_{}_{}.h5'.format(self.adir,sncs[i], sgs[j], sts[k])][0])

        rms_list=[[],[]]

        for i in range(8):  # per chip
            rms_list[0].append([])
            rms_list[1].append([])

            for j in range(16):
                ch = 16*i+j
                xx=range(16)
                rms_list[0][i].append([])
                rms_list[1][i].append([])

                for ix in range(len(sgs)):
                    for iy in range(4):
                        rms_list[0][i][j].append(rms[0][ix][iy][ch])
                        rms_list[1][i][j].append(rms[1][ix][iy][ch])

        xlabels=[]
        if self.temp=='LN':
            for ix in range(4):
                xlabels.append('{}\n{}'.format(sgs_x[ix],sts_x[0]))
                for iy in range(1,4):
                    xlabels.append('\n{}'.format(sts_x[iy]))
            xlabels[15]='{}us'.format(xlabels[15])
        else:
            for ix in range(4):
                xlabels.append('{}us'.format(sts_x[ix]))

        xx=range(len(sgs)*len(sts))
        title='RMS'
        self.tools.Config_Plot(xx, rms_list, xlabels, 'RMS', title)


if __name__=='__main__':

    runNo = 352
    temp = 'LN'
    adir = 'FEMB{}_{}_150pF'.format(runNo,temp)
    folder = '/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/FEMB_QC_data/{}/'.format(adir)
    femb = LArASIC_check(folder, runNo, temp, adir)
    femb.Config_check()
    femb.RMS_check()

