import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import QC_tools

class CALI_FEMB:

    def __init__(self, folder, runNo,temp,adir):
        self.folder=folder
        self.runNo=runNo
        self.temp=temp
        self.adir=adir
        self.tools = QC_tools.QC_tools()

        self.dac_du_ratio=[]
        self.du=[]
        self.adc=[]
        self.rms=[]
        self.gains=[]
        self.ENC=[]

        self.sncs = ["900mVBL", "200mVBL"]
        self.sts = ["0_5us", "1_0us",  "2_0us", "3_0us"]
        self.sts_x=[0.5,1,2,3]
        if self.temp=='RT' :
            self.sgs = ["14_0mVfC" ]
            self.sgs_x=['14mV/fC']
        else:
            self.sgs = ["4_7mVfC", "7_8mVfC", "14_0mVfC", "25_0mVfC" ]
            self.sgs_x=['4.7mV/fC','7.8mV/fC','14mV/fC','25mV/fC',]

        self.xlabels=[]

    def ADC_ref(self):
        fp = self.folder + "logs_tm008.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
        pdf.add_page()
        pdf.set_font('Times', 'B', 20)

        pdf.cell(80, 10, 'LArASIC Monitoring Measurement', 0, 1, 'C')
        pdf.ln(2)

        pdf.set_font('Times', '', 12)
        pdf.cell(80, 5, '14mV/fC, 900mV BL, 2.0us, 500pA, ASICDAC=0x00, Cali_disable, SDC off', 0, 1)

        pdf.ln(2)
        pdf.cell(100, 5, 'ADC reference calibration', 0, 1)
        pdf.ln(2)
        pdf.cell(25, 5, '', 1)
        pdf.cell(25, 5, 'Set Reference', 1)
        pdf.cell(25, 5, 'Measured Reference', 1)
        pdf.cell(25, 5, 'BGR', 1)
        pdf.cell(25, 5, 'Temperature', 1,1)

        pdf.cell(25, 5, 'ASIC 0 ', 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_off_vfe'][0]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_off_vfe'][1]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_off_vfe'][0]*dic['SDC_off_vfe'][1]), 1,1)


    def DAC_DU_Ratio(self):
        fp = self.folder + "logs_tm008.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        if "LN" not in logs["Env"]:
            fig,axes=plt.subplots(1,2,figsize=(10,5))
        else:
            fig,axes=plt.subplots(4,2, figsize=(8,15))

        dac_set=np.array([0,32,63])
        colors = [plt.cm.tab20(ii) for ii in range(8)]

        results=[]

        for i in range(len(self.sgs)):
            sgi=self.sgs[i]
            results.append([])

            for asic in range(8):
                dac_mea=[]
                vref=0
                for vdac in (0x00, 0x20, 0x3f):
                    tmp_dac=logs["Mon_LArASIC{}_{}_DAC{:02x}".format(asic, sgi, vdac)][0]
                    if vdac==0:
                        vref=tmp_dac
                    dac_mea.append(tmp_dac)
                dac_mea=np.array(dac_mea)
                slope,intercept=np.polyfit(dac_set,dac_mea,1)
                results[i].append((-slope, vref-intercept))
                
                if len(self.sgs)==1:
                    axes[0].scatter(dac_set,dac_mea,color=colors[asic], label="asic{}: {:.2f}*x+{:.2f}".format(asic,slope,intercept))
                    axes[0].plot(dac_set,slope*dac_set+intercept,color=colors[asic])
                else:
                    axes[i,0].scatter(dac_set,dac_mea,color=colors[asic], label="asic{}: {:.2f}*x+{:.2f}".format(asic,slope,intercept))
                    axes[i,0].plot(dac_set,slope*dac_set+intercept,color=colors[asic])
            
            if len(self.sgs)==1:
                axes[1].axis('off')
                axes[0].legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', borderaxespad=0.)
                axes[0].set_title('{} DAC vs. DU'.format(sgi))
            else:
                axes[i,1].axis('off')
                axes[i,0].legend(bbox_to_anchor=(1.1, 1.0), loc='upper left', borderaxespad=0.)
                axes[i,0].set_title('{} DAC vs. DU'.format(sgi))

       
        fig.savefig('DAC_DU.png')
        self.dac_du_ratio=results

    def ADC_DU(self): 
        fp = self.folder + "logs_tm007.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)
        

        du_list=[]
        adc_list=[]
        rms_list=[]
        
        for i in range(2):
            snc = i
            if i == 0:
               vmaxdac = 0x20
            else:
               vmaxdac = 0x40

            du_list.append([])
            adc_list.append([])
            rms_list.append([])
       
            for j in range(len(self.sgs)):
                if self.sgs[j] == '14_0mVfC': #14mV/fC
                    ks = [0,1,2,3]
                else:
                    ks = [2] #only 2.0us

                du_list[i].append([])
                adc_list[i].append([])
                rms_list[i].append([])
              
                first = True
                for k in ks: 
                    wave_peak = []
                    dac_value = []
                    rms_value = []
        
                    for asicdac in range(0, vmaxdac, 4):
                        cali_fp = "D:/IO_1826_1B/QC/{}/ASICDAC_CALI/CALI_{}_{}_{}_ASICDAC0x{:02x}.h5".format(self.adir,self.sncs[i], self.sgs[j], self.sts[k], asicdac)
                        asic_log = logs[cali_fp]
        
                        wave_peak.append(asic_log[2])
                        rms_value.append(asic_log[0])
                        dac_value.append(asicdac)
                    
                    du_list[i][j].append(dac_value)
                    adc_list[i][j].append(wave_peak)
                    rms_list[i][j].append(rms_value)
 
                    if i==0:
                        if first:
                           self.xlabels.append('{}\n{}'.format(self.sgs_x[j],self.sts_x[k]))
                           first=False
                        else:
                           self.xlabels.append('\n{}'.format(self.sts_x[k]))

        self.du=du_list
        self.adc=adc_list
        self.rms=rms_list

    def Get_Gain_ENC(self):
       
        CC=1.85*pow(10,-13)
        e=1.602*pow(10,-19)

        gains=[[],[]]
        ENC=[[],[]]

        for i in range(8):
            gains[0].append([])
            gains[1].append([])
            ENC[0].append([])
            ENC[1].append([])

            for j in range(16):
                chan = i*16+j

                gains[0][i].append([])
                gains[1][i].append([])

                ENC[0][i].append([])
                ENC[1][i].append([])

                for ix in range(len(self.sgs)):
                    q_s = self.dac_du_ratio[ix][i][0]
                    q_b = self.dac_du_ratio[ix][i][1]
                    dac_value = self.du[0][0][0]
                    dac_value = np.array(dac_value)
                    Q_value = (q_s*dac_value+q_b)*CC/e/1000.0 

                    for iy in range(len(self.adc[0][ix])):
                        adc_value_1=[]
                        adc_value_2=[]
                        for idac in range(len(dac_value)):
                            adc_value_1.append(self.adc[0][ix][iy][idac][chan])
                            adc_value_2.append(self.adc[1][ix][iy][idac][chan])
                        adc_value_1=np.array(adc_value_1)
                        adc_value_2=np.array(adc_value_2)
                        s1,int1=np.polyfit(adc_value_1,Q_value,1)
                        s2,int2=np.polyfit(adc_value_2,Q_value,1)
                        gains[0][i][j].append(s1)
                        gains[1][i][j].append(s2)
                        ENC[0][i][j].append(s1*self.rms[0][ix][iy][0][chan])
                        ENC[1][i][j].append(s2*self.rms[1][ix][iy][0][chan])

        self.gains=gains
        self.ENC=ENC

        if self.temp=='LN':
            xx=range(7)
        else:
            xx=range(4)

        title='Gain'
        self.tools.Config_Plot(xx, gains, self.xlabels, 'Gain', title)
        title='ENC'
        self.tools.Config_Plot(xx, ENC, self.xlabels, 'ENC', title)


    def Avg_Gain_ENC(self, makeplot=False):

        sncs = ["900mVBL", "200mVBL"]
        sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
        sts = ["0_5us", "1_0us",  "2_0us", "3_0us"]

        avg_gain={}
        avg_ENC={}
        for ikey,gains in self.gains.items():
            gains=np.array(gains)

            tmp_mean = np.mean(gains)
            tmp_std = np.std(gains)

            avg_gain[ikey]=(tmp_mean,tmp_std)

        for ikey,ENC in self.ENC.items():
            ENC=np.array(ENC)

            tmp_mean = np.mean(ENC)
            tmp_std = np.std(ENC)

            avg_ENC[ikey]=(tmp_mean,tmp_std)

        save_dir = self.folder+"CALI/"

        if not (os.path.exists(save_dir)):
            try:
               os.makedirs(save_dir)
            except OSError:
               print("Error to create folder %s"%save_dir)
               input("hit any button and then 'Enter' to exit")
               sys.exit()    

        sgi="14_0mVfC"
        for snc in sncs:
            thisgain_mean=[]
            thisgain_std=[]
 
            for sti in sts:
                ikey = "{}_{}_{}".format(snc,sgi,sti)
                if ikey in avg_gain.keys():
                    thisgain_mean.append(avg_gain[ikey][0])
                    thisgain_std.append(avg_gain[ikey][1])

            plt.errorbar(sts,thisgain_mean, yerr=thisgain_std, marker=".")
            plt.title("Gain mean at {}".format(snc))

            plt.savefig(save_dir+snc+"_gain_avg.png")
            plt.close()

        for snc in sncs:
            thisENC_mean=[]
            thisENC_std=[]
 
            for sti in sts:
                ikey = "{}_{}_{}".format(snc,sgi,sti)
                if ikey in avg_ENC.keys():
                    thisENC_mean.append(avg_ENC[ikey][0])
                    thisENC_std.append(avg_ENC[ikey][1])

            plt.errorbar(sts,thisENC_mean, yerr=thisENC_std, marker=".")
            plt.title("ENC mean at {}".format(snc))

            plt.savefig(save_dir+snc+"_ENC_avg.png")
            plt.close()

if __name__=='__main__':

    runNo = 352
    temp = 'LN'
    adir = 'FEMB{}_{}_150pF'.format(runNo,temp)
    folder = '/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/FEMB_QC_data/{}/'.format(adir)
    femb = CALI_FEMB(folder, runNo, temp, adir)

    femb.ADC_DU()
    femb.DAC_DU_Ratio()
    femb.Get_Gain_ENC()
    #femb.Avg_Gain_ENC()
   
