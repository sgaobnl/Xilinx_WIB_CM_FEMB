import pickle
import matplotlib.pyplot as plt
import numpy as np

class CALI_FEMB:

    def __init__(self, folder):
        self.folder=folder
        self.dac_du_ratio={}
        self.du={}    
        self.adc={}
        self.rms={}
        self.gains={}

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
                for vdac in (0x00, 0x20, 0x3f):
                    tmp_dac=logs["Mon_LArASIC{}_{}_DAC{:02x}".format(asic, sgi, vdac)][0]
                    dac_mea.append(tmp_dac)
                dac_mea=np.array(dac_mea)
                slope,intercept=np.polyfit(dac_set,dac_mea,1)
                results[sgi].append((slope, intercept))

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

    def Get_Gain(self, makeplot=False, linearplot=False):
       
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
                        chip_Q=(slope*dac_set+intercept)*CC/e  # a list of voltages for set DACs      
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

        chan=range(128)
        if makeplot:
            for ikey in gains.keys():
                plt.plot(chan, gains[ikey],marker=".")
                plt.title(ikey)
                plt.xlabel("chan")
                plt.ylabel("gain")
                plt.show()

        if makeplot:
            for ikey in ENC.keys():
                plt.plot(chan, ENC[ikey],marker=".")
                plt.title(ikey)
                plt.xlabel("chan")
                plt.ylabel("ENC")
                plt.show()

if __name__=='__main__':

    f="D:/IO_1826_1B/QC/FEMB209_LN_150pF/"
    femb=CALI_FEMB(f)
    femb.ADC_DU()
    femb.DAC_DU_Ratio(makeplot=False)
    femb.Get_Gain(makeplot=True)
   
