import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

class CALI_FEMB:

    def __init__(self, folder):
        self.folder=folder
        self.dac_du_ratio={}
        self.du={}    
        self.adc={}
        self.rms={}
        self.gains={}
        self.ENC={}

    def DAC_DU_Ratio(self,makeplot=False):
        fp = self.folder + "logs_tm008.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        if "LN" not in logs["Env"]:
            sgs = ["14_0mVfC" ]
        else:
            sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]

        dac_set=np.array([0,32,63])
        colors = [plt.cm.tab20(ii) for ii in range(8)]

        results={}

        for sgi in sgs:
            results[sgi]=[]

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
                results[sgi].append((-slope, vref-intercept))

                if makeplot:
                    plt.scatter(dac_set,dac_mea,color=colors[asic], label="asic{}: {:.2f}*x+{:.2f}".format(asic,slope,intercept))
                    plt.plot(dac_set,slope*dac_set+intercept,color=colors[asic])


            if makeplot:
                plt.legend()
                plt.title('{} DAC vs. DU'.format(sgi))
                plt.show()
        
        self.dac_du_ratio=results

    def ADC_DU(self,makeplot=False): 
        fp = self.folder + "logs_tm007.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)
        
        if "LN" not in logs["Env"] :
            sncs = ["900mVBL", "200mVBL"]
            sgs = ["14_0mVfC" ]
            sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]
        else:
            sncs = ["900mVBL", "200mVBL"]
            sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
            sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]

        du_dict={}
        adc_dict={}
        rms_dict={}
        
        for i in range(len(sncs)):
            snc = i
            if i == 0:
               vmaxdac = 0x20
            else:
               vmaxdac = 0x40
        
            for j in range(len(sgs)):
                sg0 = j%2
                sg1 = j//2
                if j == 0: #14mV/fC
                    ks = [0,1,2,3]
                else:
                    ks = [3] #only 2.0us
        
                for k in ks: 
                    st0 = k%2
                    st1 = k//2
       
                    wave_peak = []
                    dac_value = []
                    rms_value = []
        
                    for asicdac in range(0, vmaxdac, 4):
                        cali_fp = self.folder + "ASICDAC_CALI/CALI_{}_{}_{}_ASICDAC0x{:02x}.h5".format(sncs[i], sgs[j], sts[k], asicdac)
                       
                        asic_log = logs[cali_fp]
        
                        wave_peak.append(asic_log[2])
                        rms_value.append(asic_log[0])
                        dac_value.append(asicdac)
                        
                    
                    du_dict["{}_{}_{}".format(sncs[i],sgs[j],sts[k])]=np.array(dac_value)
                    adc_dict["{}_{}_{}".format(sncs[i],sgs[j],sts[k])]=wave_peak
                    rms_dict["{}_{}_{}".format(sncs[i],sgs[j],sts[k])]=rms_value

        self.du=du_dict
        self.adc=adc_dict
        self.rms=rms_dict

    def Get_Gain_ENC(self, makeplot=False, linearplot=False):
       
        CC=1.85*pow(10,-13)
        e=1.602*pow(10,-19)

        QQ={} 
        for ikey,dac_set in self.du.items():
            QQ[ikey] = []     # a list of chips

            for sgi in self.dac_du_ratio.keys():
                if sgi in ikey:
                    for asic in range(8):
                        slope=self.dac_du_ratio[sgi][asic][0]
                        intercept=self.dac_du_ratio[sgi][asic][1]
                        chip_Q=(slope*dac_set+intercept)*CC/e/1000.0  # a list of voltages for set DACs, convert mV to V
                        QQ[ikey].append(chip_Q) 

        gains={}
        ENC={}

        for ikey in QQ.keys():
            gains[ikey]=[]
            ENC[ikey]=[]

            for ichan in range(128):
                nchip=ichan//16
                dac_value=QQ[ikey][nchip]
                adc_value=[]
                for ix in range(len(self.adc[ikey])):
                    tmpadc=self.adc[ikey][ix][ichan]
                    adc_value.append(tmpadc)

                adc_value=np.array(adc_value)
                slope,intercept=np.polyfit(adc_value,dac_value,1)

                gains[ikey].append(slope)

                rms_ch=self.rms[ikey][0][ichan]  # RMS at DAC=0
                tmpENC=slope*rms_ch
                ENC[ikey].append(tmpENC)

                if linearplot:
                    plt.plot(adc_value,dac_value,marker=".",label=ichan)
                    plt.title(ikey)
                    plt.ylabel("DAC voltage")
                    plt.xlabel("ADC")
                    plt.legend()
                    plt.show()
        
        self.gains=gains
        self.ENC=ENC

        chan=range(128)
        if makeplot:
            save_dir = self.folder+"CALI/"

            if not (os.path.exists(save_dir)):
                try:
                    os.makedirs(save_dir)
                except OSError:
                    print("Error to create folder %s"%save_dir)
                    input("hit any button and then 'Enter' to exit")
                    sys.exit()    

            for ikey in gains.keys():
                plt.plot(chan, gains[ikey],marker=".")
                plt.title(ikey)
                plt.xlabel("chan")
                plt.ylabel("gain")
                plt.savefig(save_dir+"{}_gain.png".format(ikey))
                plt.close()

        if makeplot:
            for ikey in ENC.keys():
                plt.plot(chan, ENC[ikey],marker=".")
                plt.title(ikey)
                plt.xlabel("chan")
                plt.ylabel("ENC")
                plt.savefig(save_dir+"{}_ENC.png".format(ikey))
                plt.close()

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

    f="D:/IO_1826_1B/QC/FEMB209_LN_150pF/"
    femb=CALI_FEMB(f)
    femb.ADC_DU()
    femb.DAC_DU_Ratio(makeplot=False)
    femb.Get_Gain_ENC(makeplot=False)
    femb.Avg_Gain_ENC()
   
