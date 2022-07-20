import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from fpdf import FPDF
from PyPDF2 import PdfMerger
import QC_tools
#from matplotlib.backends.backend_pdf import PdfPages



class CHECK_PWR:

    def __init__(self, folder, runNo): 
        self.folder = folder
        self.runNo = runNo
        self.tools = QC_tools.QC_tools()

    def pwr_config(self):
        fp = self.folder + "logs_tm003.bin"

        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        dic={}
        dic['SDC_off_vfe']=logs["power_meas1_vfe_meas"]
        dic['SDC_off_vadc']=logs["power_meas1_vadc_meas"]
        dic['SDC_off_vcd']=logs["power_meas1_vcd_meas"]
        dic['SDC_off_bias']=logs["power_meas1_bias_meas"]

        dic['SDC_on_vfe']=logs["power_meas2_vfe_meas"]
        dic['SDC_on_vadc']=logs["power_meas2_vadc_meas"]
        dic['SDC_on_vcd']=logs["power_meas2_vcd_meas"]
        dic['SDC_on_bias']=logs["power_meas2_bias_meas"]

        dic['SEDC_on_vfe']=logs["power_meas3_vfe_meas"]
        dic['SEDC_on_vadc']=logs["power_meas3_vadc_meas"]
        dic['SEDC_on_vcd']=logs["power_meas3_vcd_meas"]
        dic['SEDC_on_bias']=logs["power_meas3_bias_meas"]

        pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
        pdf.add_page()
        pdf.set_font('Times', 'B', 20)

        pdf.cell(80, 10, 'Power Measurement', 0, 1, 'C')
        pdf.ln(2)

        pdf.set_font('Times', '', 12)
        pdf.cell(80, 5, '14mV/fC, 900mV BL, 2.0us, 500pA, ASICDAC=0x00, Cali_disable', 0, 1)

        pdf.ln(2)
        pdf.cell(100, 5, 'Single Ended, SDC off', 1, 1)
        pdf.cell(25, 5, 'Power Rail', 1)
        pdf.cell(25, 5, 'Voltage (V)', 1)
        pdf.cell(25, 5, 'Current (A)', 1)
        pdf.cell(25, 5, 'Power (W)', 1,1)
        
        pdf.cell(25, 5, 'FEMB', 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_off_vfe'][0]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_off_vfe'][1]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_off_vfe'][0]*dic['SDC_off_vfe'][1]), 1,1)

        pdf.ln(2)
        pdf.cell(100, 5, 'Single Ended, SDC on', 1, 1)
        pdf.cell(25, 5, 'Power Rail', 1)
        pdf.cell(25, 5, 'Voltage (V)', 1)
        pdf.cell(25, 5, 'Current (A)', 1)
        pdf.cell(25, 5, 'Power (W)', 1,1)
        
        pdf.cell(25, 5, 'FEMB', 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_on_vfe'][0]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_on_vfe'][1]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SDC_on_vfe'][0]*dic['SDC_on_vfe'][1]), 1,1)

        pdf.ln(2)
        pdf.cell(100, 5, 'Single Ended, SEDC on', 1, 1)
        pdf.cell(25, 5, 'Power Rail', 1)
        pdf.cell(25, 5, 'Voltage (V)', 1)
        pdf.cell(25, 5, 'Current (A)', 1)
        pdf.cell(25, 5, 'Power (W)', 1,1)
        
        pdf.cell(25, 5, 'FEMB', 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SEDC_on_vfe'][0]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SEDC_on_vfe'][1]), 1)
        pdf.cell(25, 5, "{:0.3f}".format(dic['SEDC_on_vfe'][0]*dic['SEDC_on_vfe'][1]), 1,1)

        pdf.output('pwr1.pdf', 'F')
        pdf.close()

    def pwr_cycles(self):

        # voltage, current, power after each power cycle
        fp = self.folder + "logs_tm004.bin"
        with open(fp, 'rb') as fp:
            logs = pickle.load(fp)

        vfe=[]
        ife=[]
        pfe=[]
        for i in range(5):
            key_name = "power_cycle{}_on_vfe_meas".format(i)
            a_v = logs[key_name][0]
            a_i = logs[key_name][1]
            a_p = a_v*a_i
            vfe.append(a_v)
            ife.append(a_i)
            pfe.append(a_p)

        vadc=[]
        iadc=[]
        padc=[]
        for i in range(5):
            key_name = "power_cycle{}_on_vadc_meas".format(i)
            a_v = logs[key_name][0]
            a_i = logs[key_name][1]
            a_p = a_v*a_i
            vadc.append(a_v)
            iadc.append(a_i)
            padc.append(a_p)

        vcd=[]
        icd=[]
        pcd=[]
        for i in range(5):
            key_name = "power_cycle{}_on_vcd_meas".format(i)
            a_v = logs[key_name][0]
            a_i = logs[key_name][1]
            a_p = a_v*a_i
            vcd.append(a_v)
            icd.append(a_i)
            pcd.append(a_p)

# not available due a bug in the QC_runs.py
#        vbias=[]
#        ibias=[]
#        pbias=[]
#        for i in range(5):
#            key_name = "power_cycle{}_on_vbias_meas".format(i)
#            a_v = logs[key_name][0]
#            a_i = logs[key_name][1]
#            a_p = a_v*a_i
#            vbias.append(a_v)
#            ibias.append(a_i)
#            pbias.append(a_p)
#

        xx = range(5)

        vfe=np.array(vfe)
        ife=np.array(ife)
        pfe=np.array(pfe)
        fig_fe,axes_fe=plt.subplots(1,3,figsize=(12,2))
        mean = np.mean(vfe)
        axes_fe[0].plot(xx,vfe,marker='.',label="mean={:03f}".format(mean))
        axes_fe[0].set_title("FEMB voltage(V)")
        axes_fe[0].set_xlabel("cycles")
        axes_fe[0].set_ylabel("V")
        axes_fe[0].set_ylim([mean*0.99,mean*1.01])
        axes_fe[0].legend()

        mean = np.mean(ife)
        axes_fe[1].plot(xx,ife,marker='.',label="mean={:03f}".format(mean))
        axes_fe[1].set_title("FEMB current (A)")
        axes_fe[1].set_xlabel("cycles")
        axes_fe[1].set_ylabel("I")
        axes_fe[1].set_ylim([mean*0.99,mean*1.01])
        axes_fe[1].legend()

        mean = np.mean(pfe)
        axes_fe[2].plot(xx,pfe,marker='.',label="mean={:03f}".format(mean))
        axes_fe[2].set_title("FEMB power(W)")
        axes_fe[2].set_xlabel("cycles")
        axes_fe[2].set_ylabel("P")
        axes_fe[2].set_ylim([mean*0.99,mean*1.01])
        axes_fe[2].legend()

        fig_fe.savefig("fe_pwr.png")

        vadc=np.array(vadc)
        iadc=np.array(iadc)
        padc=np.array(padc)
        fig_adc,axes_adc=plt.subplots(1,3,figsize=(12,2))
        mean = np.mean(vadc)
        axes_adc[0].plot(xx,vadc,marker='.',label="mean={:03f}".format(mean))
        axes_adc[0].set_title("ColdADC voltage(V)")
        axes_adc[0].set_xlabel("cycles")
        axes_adc[0].set_ylabel("V")
        axes_adc[0].set_ylim([mean*0.99,mean*1.01])
        axes_adc[0].legend()

        mean = np.mean(iadc)
        axes_adc[1].plot(xx,iadc,marker='.',label="mean={:03f}".format(mean))
        axes_adc[1].set_title("ColdADC current (A)")
        axes_adc[1].set_xlabel("cycles")
        axes_adc[1].set_ylabel("I")
        axes_adc[1].set_ylim([mean*0.99,mean*1.01])
        axes_adc[1].legend()

        mean = np.mean(padc)
        axes_adc[2].plot(xx,padc,marker='.',label="mean={:03f}".format(mean))
        axes_adc[2].set_title("ColdADC power(W)")
        axes_adc[2].set_xlabel("cycles")
        axes_adc[2].set_ylabel("P")
        axes_adc[2].set_ylim([mean*0.99,mean*1.01])
        axes_adc[2].legend()

        fig_adc.savefig("adc_pwr.png")

        vcd=np.array(vcd)
        icd=np.array(icd)
        pcd=np.array(pcd)
        fig_cd,axes_cd=plt.subplots(1,3,figsize=(12,2))
        mean = np.mean(vcd)
        axes_cd[0].plot(xx,vcd,marker='.',label="mean={:03f}".format(mean))
        axes_cd[0].set_title("ColdDATA voltage(V)")
        axes_cd[0].set_xlabel("cycles")
        axes_cd[0].set_ylabel("V")
        axes_cd[0].set_ylim([mean*0.99,mean*1.01])
        axes_cd[0].legend()

        mean = np.mean(icd)
        axes_cd[1].plot(xx,icd,marker='.',label="mean={:03f}".format(mean))
        axes_cd[1].set_title("ColdDATA current (A)")
        axes_cd[1].set_xlabel("cycles")
        axes_cd[1].set_ylabel("I")
        axes_cd[1].set_ylim([mean*0.99,mean*1.01])
        axes_cd[1].legend()

        mean = np.mean(pcd)
        axes_cd[2].plot(xx,pcd,marker='.',label="mean={:03f}".format(mean))
        axes_cd[2].set_title("ColdDATA power(W)")
        axes_cd[2].set_xlabel("cycles")
        axes_cd[2].set_ylabel("P")
        axes_cd[2].set_ylim([mean*0.99,mean*1.01])
        axes_cd[2].legend()

        fig_cd.savefig("cd_pwr.png")


        # RMS and pulse response per cycle
        rms=np.empty(0)
        ped=np.empty(0)
        pkp=np.empty(0)
        pkn=np.empty(0)
        onewf=np.empty(0)
        avgwf=np.empty(0)

        for i in range(5):
            fp = 'D:/IO_1826_1B/QC/FEMB{}_LN_150pF/PWR/power_cycle{}_CHK_response_SE.h5'.format(self.runNo, i)

            pwr_log = logs[fp]
            a_rms = np.array(pwr_log[0])
            a_ped = np.array(pwr_log[1])
            a_pkp = np.array(pwr_log[2])
            a_pkn = np.array(pwr_log[3])
            a_onewf = np.array(pwr_log[4])
            a_avgwf = np.array(pwr_log[5])
            if i==0:
                rms = a_rms
                ped = a_ped
                pkp = a_pkp
                pkn = a_pkn
                onewf = a_onewf
                avgwf = a_avgwf
            else:
                rms = rms+a_rms
                ped = ped+a_ped
                pkp = pkp+a_pkp
                pkn = pkn+a_pkn
                onewf = onewf+a_onewf
                avgwf = avgwf+a_avgwf

        rms = rms/5
        ped = ped/5
        pkp = pkp/5
        pkn = pkn/5
        onewf = onewf/5
        avgwf = avgwf/5

        fig_chk = self.tools.FEMB_CHK_PLOT(rms, ped, pkp, pkn, onewf, avgwf, "average all cycles")

        fig_chk.savefig("chk_pwr.png")
        plt.close()

        pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
        pdf.add_page()
        pdf.set_font('Times', 'B', 20)

        pdf.cell(80, 10, 'Power Cycles Measurement', 0, 1, 'C')
        pdf.ln(2)

        pdf.image("fe_pwr.png",10, 20, 200)
        pdf.image("adc_pwr.png",10, 65, 200)
        pdf.image("cd_pwr.png",10, 110, 200)
        pdf.image("chk_pwr.png",10, 160, 200)

        pdf.output('pwr2.pdf', 'F')
        pdf.close()

        



    def MergePDF(self):
        # merge pdfs
        pdfName = self.folder+'QC_report.pdf'
#        if not (os.path.exists(pdfName)):


if __name__=='__main__':

    runNo = 352
    folder = '/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/FEMB_QC_data/FEMB{}_LN_150pF/'.format(runNo)
    pwr = CHECK_PWR(folder, runNo)
#    pwr.pwr_config()
    pwr.pwr_cycles()
