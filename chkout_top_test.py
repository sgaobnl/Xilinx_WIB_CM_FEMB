# -*- coding: utf-8 -*-
"""
File Name: cls_femb_config.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:50:34 PM
Last modified: 5/25/2022 9:11:15 PM
"""

import numpy as np
import sys
import os
import string
import time
from datetime import datetime
from cls_udp import CLS_UDP
from tcp_cfg import TCP_CFG
import struct
from raw_convertor import RAW_CONV
import matplotlib.pyplot as plt
import h5py
import datetime

def Check_monitor_data(data, temp):

    V_1 = data[1][1]
    TEMP_1 = data[1][2]
    VCMI_1 = data[1][3]
    VCMO_1 = data[1][4]
    VREFP_1 = data[1][5]
    VREFN_1 = data[1][6]

    if V_1>1300 or V_1<1100:
        return False

    if temp=='RT':
        if TEMP_1<900 or TEMP_1>1000:
            return False
    
    if temp=='LN':
        if TEMP_1<200 or TEMP_1>300:
            return False

    if VCMI_1<900 or VCMI_1>1000:
        return False

    if VCMO_1<1100 or VCMO_1>1300:
        return False

    if VREFP_1<1800 or VREFP_1>2100:
        return False

    if VREFN_1<460 or VREFN_1>500:
        return False

    V_2 = data[2][1]
    TEMP_2 = data[2][2]
    VCMI_2 = data[2][3]
    VCMO_2 = data[2][4]
    VREFP_2 = data[2][5]
    VREFN_2 = data[2][6]

    if V_2>1300 or V_2<1100:
        return False

    if temp=='RT':
        if TEMP_2<900 or TEMP_2>1000:
            return False
    
    if temp=='LN':
        if TEMP_2<200 or TEMP_2>300:
            return False

    if VCMI_2<900 or VCMI_2>1000:
        return False

    if VCMO_2<1100 or VCMO_2>1300:
        return False

    if VREFP_2<1800 or VREFP_2>2100:
        return False

    if VREFN_2<460 or VREFN_2>500:
        return False

    return True

def Check_power_data(data):

    fe_Vref = data[1][1]
    fe_Vmea = data[1][2]
    fe_cur = data[1][3]
    fe_pwr = data[1][4]
    
    if (fe_Vref-fe_Vmea)<0 or (fe_Vref-fe_Vmea)>0.2:
        return False

    if fe_cur<0.4 or fe_cur>0.6:
        return False

    if fe_pwr<1.0 or fe_pwr>1.4:
        return False

    adc_Vref = data[2][1]
    adc_Vmea = data[2][2]
    adc_cur = data[2][3]
    adc_pwr = data[2][4]

    if (adc_Vref-adc_Vmea)<0 or (adc_Vref-adc_Vmea)>0.2:
        return False

    if adc_cur<1.2 or adc_cur>1.5:
        return False

    if adc_pwr<4.5 or adc_pwr>4.8:
        return False

    cd_Vref = data[3][1]
    cd_Vmea = data[3][2]
    cd_cur = data[3][3]
    cd_pwr = data[3][4]

    if (cd_Vref-cd_Vmea)<0 or (cd_Vref-cd_Vmea)>0.2:
        return False

    if cd_cur<0.1 or cd_cur>0.35:
        return False

    if cd_pwr<0.5 or cd_pwr>0.8:
        return False

    bias_Vref = data[4][1]
    bias_Vmea = data[4][2]
    bias_cur = data[4][3]
    bias_pwr = data[4][4]

    if (bias_Vref-bias_Vmea)<0 or (bias_Vref-bias_Vmea)>0.2:
        return False

    if bias_cur>0.1:
        return False

    if bias_pwr>0.04:
        return False
    
    return True

def generate_report(result_dict):
    print ("Generator the test report...")
    from fpdf import FPDF
    import pickle
    pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
    pdf.alias_nb_pages()
    print ("##### FEMB Checkout Test Report #####")
    pdf.add_page()
    pdf.set_font('Times', 'B', 20)
    pdf.cell(85)
    print (pdf.l_margin)
    pdf.l_margin = pdf.l_margin*2
    pdf.cell(30, 5, 'FEMB#{:04d} Checkout Test Report'.format(result_dict["FEMB_SN"]), 0, 1, 'C')
    pdf.ln(2)

    pdf.set_font('Times', '', 12)
    pdf.cell(30, 5, 'FEMB ID = {:04d},  SLOT={}'.format(result_dict["FEMB_SN"],result_dict["Slot"]), 0, 1)
   
    pdf.set_font('Times', '', 12)
    pdf.cell(30, 5, 'Date&Time: %s'%result_dict["datetime"].strftime("%Y-%m-%d %H:%M:%S"), 0, 0)
    pdf.cell(80)
    pdf.cell(30, 5, 'Tester: {}'.format(result_dict["Tester"]), 0, 1)
    
    pdf.cell(30, 5, 'WIB_TCP_Version: 0x{:02x}'.format(result_dict["WIB_TCP_FW_ver"]), 0, 0)
    pdf.cell(80)
    pdf.cell(30, 5, 'WIB_UDP_Version: 0x{:02x}'.format(result_dict["WIB_UDP_FW_ver"]), 0, 1)
    
    pdf.cell(30, 5, 'Temperature: {}'.format(result_dict["Env"]), 0, 0)
    pdf.cell(80)
    pdf.cell(30, 5, 'Input Capacitor(Cd): {}'.format(result_dict["Cd"]), 0, 1)
    pdf.cell(30, 5, 'Note: {}'.format(result_dict["Note"][0:80]), 0, 1)
#    for i in range((len(result_dict["Note"])//70) + 1):
#        if i == 0:
#            pdf.cell(30, 5, 'Note: {}'.format(result_dict["Note"][i*70:(i+1)*70]), 0, 1)
#        else:
#            pdf.cell(30, 5, '      {}'.format(result_dict["Note"][i*70:(i+1)*70]), 0, 1)
    
    print ("# FEMB configuration #")
    pdf.ln(2)
    pdf.cell(70)
    pdf.cell(30, 5, 'FEMB Configuration' , 0, 1, 'C')
    pdf.cell(30, 5, 'FE_CFG: {}'.format(result_dict["FE_CFG"]), 0, 1)
    pdf.cell(30, 5, 'ADC_CFG: {}'.format(result_dict["ADC_CFG0"]), 0, 1)
    pdf.cell(30, 5, 'ADC_CFG: {}'.format(result_dict["ADC_CFG1"]), 0, 1)
    pdf.cell(30, 5, 'CD_FE_pulse: {}'.format(result_dict["CD_FE_pulse"]), 0, 1)
    
    # Generate Power Check table
    print ("# Generate Power Check table")
    data=[["Power rail","V_set /V","V_meas /V","I_meas /A","P_meas /W"],
          ["LArASIC", 0, 0,0,0], 
          ["ColdADC", 0, 0,0,0], 
          ["COLDATA", 0, 0,0,0], 
          [" BIAS  ", 0, 0,0,0] 
          ]
    data[1][1] = result_dict["power_vfe_ref"][0]
    data[1][2] = result_dict["power_vfe_meas"][0]
    data[1][3] = result_dict["power_vfe_meas"][1]
    data[1][4] = result_dict["power_vfe_meas"][0]*result_dict["power_vfe_meas"][1]
    data[2][1] = result_dict["power_vadc_ref"][0]
    data[2][2] = result_dict["power_vadc_meas"][0]
    data[2][3] = result_dict["power_vadc_meas"][1]
    data[2][4] = result_dict["power_vadc_meas"][0]*result_dict["power_vadc_meas"][1]
    data[3][1] = result_dict["power_vcd_ref"][0]
    data[3][2] = result_dict["power_vcd_meas"][0]
    data[3][3] = result_dict["power_vcd_meas"][1]
    data[3][4] = result_dict["power_vcd_meas"][0]*result_dict["power_vcd_meas"][1]
    data[4][1] = result_dict["power_bias_ref"][0]
    data[4][2] = result_dict["power_bias_meas"][0]
    data[4][3] = result_dict["power_bias_meas"][1]
    data[4][4] = result_dict["power_bias_meas"][0]*result_dict["power_bias_meas"][1]
    femb_pwr_con = data[1][4] + data[2][4] + data[3][4] + data[4][4]

    pwr_result =Check_power_data(data):
    if femb_pwr_con>6.8:
        pwr_result = False

    if pwr_result:
        pwr_result_str = "Pass"
    else:
        pwr_result_str = "Fail"

    pdf.ln(2)
    pdf.cell(70)
    pdf.cell(30, 5, 'Power Consumption (including cable dissipation) = {:0.3f}W,   '.format(femb_pwr_con)+pwr_result_str, 0, 1, 'C')
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/5
    pdf.set_font('Times', '', 12) 
    th = pdf.font_size  # print ("# Text height is the same as current font size")
    pdf.ln(0.5*th)
    for j in range(len(data)):
        for i in range(len(data[j])):
            if j == 0 or i==0:
                pdf.cell(col_width, 2*th, "{}".format(data[j][i]), border=1, align='C')
            else:
                pdf.cell(col_width, 2*th, "{:0.3f}".format(data[j][i]), border=1, align='C')
        pdf.ln(2*th)
    pdf.ln(2)

    # Generate Monitoring Check table
    asic = 0
    print ("# Generate Monitoring Check table")
    data=[["ASIC# ","FE Vref","FE T","ADC VCMI","ADC VCMO","ADC VREFP","ADC VREFN",],
          ["{}".format(0), 0, 0, 0, 0, 0, 0], 
          ["{}".format(4), 0, 0, 0, 0, 0, 0], 
          ]
    asic = 0
    data[1][1] = int(result_dict["Mon_LArASIC{:02d}_BGR".format(asic)][0])
    data[1][2] = int(result_dict["Mon_LArASIC{:02d}_Temperature".format(asic)][0])
    data[1][3] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][1][0])
    data[1][4] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][2][0])
    data[1][5] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][3][0])
    data[1][6] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][4][0])

    asic = 4
    data[2][1] = int(result_dict["Mon_LArASIC{:02d}_BGR".format(asic)][0])
    data[2][2] = int(result_dict["Mon_LArASIC{:02d}_Temperature".format(asic)][0])
    data[2][3] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][1][0])
    data[2][4] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][2][0])
    data[2][5] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][3][0])
    data[2][6] = int(result_dict["ADC{:02d}_MeasRef".format(asic)][4][0])


    monitor_result = Check_monitor_data(data, result_dict["Env"])
    if monitor_result:
        monitor_result_str='True'
    else:
        monitor_result_str='False'

    pdf.ln(1)
    pdf.cell(70)
    pdf.cell(30, 5, 'Monitoring path for FE-ADC#0 (unit: mV),   '+monitor_result_str , 0, 1, 'C')
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/7
    pdf.set_font('Times', '', 12) 
    th = pdf.font_size  # print ("# Text height is the same as current font size")
    pdf.ln(0.4*th)
    for j in range(len(data)):
        for i in range(len(data[j])):
            if j == 0 or i==0:
                pdf.cell(col_width, 2*th, "{}".format(data[j][i]), border=1, align='C')
            else:
                pdf.cell(col_width, 2*th, "{:0.3f}".format(data[j][i]), border=1, align='C')
        pdf.ln(2*th)
    pdf.ln(2)

    ####################################################### 
    pdf.image(result_dict["response.png"], 10, 160, 190)    

    filename = result_dict["save_dir"] + "result.pdf"
    pdf.output(filename, 'F')
    pdf.close()

    with open(result_dict["save_dir"] + "result.bin", 'wb') as fp:
        pickle.dump(result_dict, fp)


def data_ana(femb_data):
    chn_rmss = []
    chn_peds = []
    chn_pkps = []
    chn_pkns = []
    chn_onewfs = []
    chn_avgwfs = []

    for chipi in range(8):
        plsn = (len(femb_data[chipi][0])//500)-10
        if plsn > 100:
            plsn = 100

        for i in range(plsn):
            if i == 0:
                avg_wf = np.array(femb_data[chipi][0][0:500])&0xffff
            else:
                avg_wf = avg_wf + (np.array(femb_data[chipi][0][500*i:500*i+500])&0xffff)
        avg_wf = avg_wf//plsn
        posp = np.where(avg_wf == np.max(avg_wf))[0][0] + 500-50

        for chn in range(16):
            peddata = []
            chndata = femb_data[chipi][chn][posp:]
            #one_wf = chndata[0:500]
            rms_min=0
            for i in range(plsn):
                peddata += chndata[150 + 500*i: 500 + 500*i] 
                tmprms = np.std(chndata[150 + 500*i: 500 + 500*i])
                if tmprms>rms_min:
                    one_wf =  chndata[500*i: 500 + 500*i]
                    rms_min = tmprms

                if i == 0:
                    avg_wf = np.array(chndata[0:500])&0xffff
                else:
                    avg_wf = avg_wf + (np.array(chndata[500*i:500*i+500])&0xffff)
            avg_wf = avg_wf//plsn

            rms    = np.std(peddata)
            ped    = int(np.mean(peddata))
            peakp = np.max(avg_wf)
            peakn = np.min(avg_wf)            

            chn_rmss.append( rms   )  
            chn_peds.append( ped   )  
            chn_pkps.append( peakp )  
            chn_pkns.append( peakn )  
            chn_onewfs.append(one_wf )  
            chn_avgwfs.append(avg_wf )  
    return chn_rmss,chn_peds, chn_pkps, chn_pkns, chn_onewfs, chn_avgwfs

def FEMB_SUB_PLOT(ax, x, y, title, xlabel, ylabel, color='b', marker='.', atwinx=False, ylabel_twx = "", e=None):
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

def FEMB_PLOT(chn_rmss,chn_peds, chn_pkps, chn_pkns, chn_onewfs, chn_avgwfs, save_dir):
#    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10,6))
    ax1 = plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((4, 4), (0, 2), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4, 4), (2, 0), colspan=2, rowspan=2)
    ax4 = plt.subplot2grid((4, 4), (2, 2), colspan=2, rowspan=2)
    chns = range(128)
    FEMB_SUB_PLOT(ax1, chns, chn_rmss, title="RMS Noise", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
    FEMB_SUB_PLOT(ax2, chns, chn_peds, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='r', marker='.')
    FEMB_SUB_PLOT(ax2, chns, chn_pkps, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='b', marker='.')
    FEMB_SUB_PLOT(ax2, chns, chn_pkns, title="Red: Pos Peak. Blue: Pedestal. Green: Neg Peak", xlabel="CH number", ylabel ="ADC / bin", color='g', marker='.')
    for chni in chns:
        ts = 100 
        x = (np.arange(ts)) * 0.5
        y3 = chn_onewfs[chni][25:ts+25]
        y4 = chn_avgwfs[chni][25:ts+25]
        FEMB_SUB_PLOT(ax3, x, y3, title="Waveform Overlap (1 cycle)", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))
        FEMB_SUB_PLOT(ax4, x, y4, title="Averaging(100 Cycles) Waveform Overlap", xlabel="Time / $\mu$s", ylabel="ADC /bin", color='C%d'%(chni%9))
                
    plt.tight_layout( rect=[0.05, 0.05, 0.95, 0.95])
    fn = save_dir + "response.png"
    plt.savefig(fn)
    plt.close()
    return fn

def FEMB_CHKOUT_folder(save_dir):
    if (os.path.exists(save_dir)):
        print ("Folder exist, please check the entering infomation...")
        #exit_en = input("Exit and Restart(Y/N)? : ")
        exit_en = "n"
        if ("Y" in exit_en) or ("y" in exit_en):
            input ("hit any button and then 'Enter' to exit")
            exit()
        else:
            i = 0
            while (True):
                i = i + 1
                fd_new = save_dir[:-1]+"_R{:03d}/".format(i)
                if (os.path.exists(fd_new)):
                    pass
                else:
                    try:
                        os.makedirs(fd_new)
                    except OSError:
                        print ("Error to create folder %s"%fd_new)
                        input ("hit any button and then 'Enter' to exit")
                        sys.exit()    
                    save_dir = fd_new
                    break
#        del_en = input("Delete the content in the folder(Y/N) ? : ")
#        print ("WARNING!!!")
#        print ("WARNING!!!")
#        print ("WARNING!!!")
#        print ("WARNING!!!")
#        print ("WARNING!!!")
#        del_en = input("Confirm(Y/N) ? : ")
#        if ("Y" in del_en) or ("y" in del_en):
#            for fn in os.listdir(save_dir):
#                # construct full file path
#                fp = save_dir + fn
#                if os.path.isfile(fp):
#                    print('Deleting file:', fp)
#                    os.remove(fp)
#        else:
#            print ("Exit, please restart...")
#            exit()
    else:
        try:
            os.makedirs(save_dir)
        except OSError:
            print ("Error to create folder %s"%save_dir)
            input ("hit any button and then 'Enter' to exit")
            sys.exit()    
    return save_dir

def pwr_chk(pwr_info, v_fe, v_adc, v_cd, v_bias, iref_fe, iref_adc, iref_cd, iref_bias):
    pwr_en = 1
    if abs(v_fe - pwr_info[0][0] ) > 0.2 :
        print ("Power rail for FE, set={}V, read={}V, please check connection".format(v_fe, pwr_info[0][0]))
        pwr_en = 0
    if abs(v_adc - pwr_info[1][0] ) > 0.2 :
        print ("Power rail for ADC, set={}V, read={}V, please check connection".format(v_fe, pwr_info[1][0]))
        pwr_en = 0
    if abs(v_cd - pwr_info[2][0] ) > 0.2 :
        print ("Power rail for CD, set={}V, read={}V, please check connection".format(v_fe, pwr_info[2][0]))
        pwr_en = 0
    if abs(v_bias - pwr_info[3][0] ) > 0.2 :
        print ("Power rail for BIAS, set={}V, read={}V, please check connection".format(v_fe, pwr_info[3][0]))
        pwr_en = 0
    
    if abs(iref_fe - pwr_info[0][1] ) > 0.2 :
        print ("Power rail for FE, current of range, ref={}A, read={}A, please check connection".format(iref_fe, pwr_info[0][1]))
        pwr_en = 0
    if abs(iref_adc - pwr_info[1][1] ) > 0.2 :
        print ("Power rail for ADC, current of range, ref={}A, read={}A, please check connection".format(iref_adc, pwr_info[1][1]))
        pwr_en = 0
    if abs(iref_cd - pwr_info[2][1] ) > 0.1 :
        print ("Power rail for CD, current of range, ref={}A, read={}A, please check connection".format(iref_cd, pwr_info[2][1]))
        pwr_en = 0
    if abs(iref_bias - pwr_info[3][1] ) > 0.1 :
        print ("Power rail for BIAS, current of range, ref={}A, read={}A, please check connection".format(iref_bias, pwr_info[3][1]))
        pwr_en = 0
    return pwr_en

def FEMB_CHK(rootdir, save_dir, femb, femb_sn, env, tester, ToyTPC, note):
    tcp = TCP_CFG()
    udp = CLS_UDP()
    conv = RAW_CONV()
    
    now = datetime.datetime.now()
    
    print ("Checkout test start...")
    result_dict ={} 
    result_dict["datetime"] = now
    result_dict["rootdir"] = rootdir
    
    
    ver = tcp.wib_ver()
    if (ver[1] == 0x100):
        print ("TCP link built.")
    result_dict["WIB_TCP_FW_ver"] = ver[1]
    
    longcable = False 
    if longcable: 
        print ("Long cable is in use...")
        tcp.tcp_poke(addr=0x08, data=longcable)
        if (tcp.tcp_peek(addr=0x08) == longcable):
            pass
        else:
            print("Configuration for long cable is error, please check, exit anyway.")
            input ("hit any button and then 'Enter' to exit")
            exit()
    else:
        print ("Short cable is in use...")
        tcp.tcp_poke(addr=0x08, data=longcable)
        if tcp.tcp_peek(addr=0x08) == longcable:
            pass
        else:
            print("Configuration for short cable is error, please check, exit anyway.")
            input ("hit any button and then 'Enter' to exit")
            exit()
    
    udpver = udp.read_reg_wib(reg=0x100)
    if (udpver == 0x1A5):
        print ("UDP link built.")
    result_dict["WIB_UDP_FW_ver"] = udpver
    
   # femb=3
    if femb == 0:
        tcp.link_cs = 0
    elif femb == 1:
        tcp.link_cs = 2
    elif femb == 2:
        tcp.link_cs = 4
    elif femb == 3:
        tcp.link_cs = 6

    
    result_dict["FEMB_SN"] = femb_sn
    result_dict["Slot"] = tcp.link_cs/2
    result_dict["Env"] = env 
    result_dict["Cd"] = ToyTPC
    result_dict["save_dir"] = save_dir 
    result_dict["Tester"] =  tester
    result_dict["Note"] = note 
    
    ################################################################################################
    ##power consumption
    print ("Turn on FEMB on WIB slot {}".format(femb))
    v_fe=3.0
    v_adc=3.5
    v_cd=2.8
    v_bias = 5.0
    iref_fe=0.42
    iref_adc=1.29
    iref_cd=0.18
    iref_bias =0.05
    
    tcp.femb_pwr_set(femb=femb, pwr_on=0)
    time.sleep(5)
    
    tcp.femb_pwr_set(femb=femb, pwr_on=1, v_fe=v_fe, v_adc=v_adc, v_cd=v_cd)
    time.sleep(2)
    tcp.set_fe_board(sts=0,snc=0,sg0=0,sg1=0,st0=1,st1=1,swdac=0,dac=0x0)
    tcp.femb_cfg()
    time.sleep(1)
    for i in range(20):
        pwr_info = tcp.femb_pwr_rd(femb=femb)
        time.sleep(0.5)
    pwr_info = tcp.femb_pwr_rd(femb=femb)
    time.sleep(1)

    pwr_en =0 
    while (pwr_en == 0):
        pwr_info = tcp.femb_pwr_rd(femb=femb)
        pwr_en = pwr_chk(pwr_info, v_fe, v_adc, v_cd, v_bias, iref_fe, iref_adc, iref_cd, iref_bias)
        if pwr_en ==0 :
            tcp.femb_pwr_set(femb=femb, pwr_on=0)
            tmp = input ("hit 'Y' or 'y' to exit, hit any other buttons to rechk")
            if ("Y" in tmp) or ("y" in tmp):
                exit()
            print ("Turn FEMB off and exit...")
        else:
            print ("FEMB power consumption is in the normal range")
            break
    result_dict["power_vfe_ref"] =  (v_fe,  iref_fe)
    result_dict["power_vadc_ref"] = (v_adc, iref_adc)
    result_dict["power_vcd_ref"] =  (v_cd,  iref_cd,)
    result_dict["power_bias_ref"] = (v_bias,iref_bias)
    
    ##########1#####################################################################################
    #FEMB configuration: 14mV/fC, 200mV BL, 2.0us, single-ended, 500pA, ASICDAC=0x10, Cali_enable, SDC off,
    result_dict["FE_CFG"] = "14mV/fC, 900mV BL, 2.0us, SE_OFF, 500pA, ASIC_CAL, ASICDAC=0x10"
    result_dict["ADC_CFG0"] = "CMOS reference set to default, Auto Calibration, "  
    result_dict["ADC_CFG1"] = "SE, SDC off, offset_binary_format, Auto Calibration, "  
    result_dict["CD_FE_pulse"] = "500 samples/pulse, CD Addr0x06:0x30,0x07:0x00, 0x08:0x38, 0x09:0x80"  
    
    print ("Measure monitoring parameters")
    tcp.set_fe_board(sts=0,snc=0,sg0=0,sg1=0,st0=1,st1=1,swdac=0,dac=0x0)
    tcp.femb_cfg()
    #for asic in range(8):
    for asic in [0, 4]:
        print ("Measure ASIC {}".format(asic))
        tmp = tcp.femb_adc_mon_cs(femb_no=femb, adc_no=asic)
        result_dict["ADC{:02d}_SetRef".format(asic)] = tmp[1]
        result_dict["ADC{:02d}_MeasRef".format(asic)] = tmp[0]
        tmp = tcp.femb_fe_mon_cs(femb_no=femb, ext_lemo=0, rst_fe=1, mon_type=2, mon_chip = asic)
        result_dict["Mon_LArASIC{:02d}_BGR".format(asic)] = tmp
        tmp = tcp.femb_fe_mon_cs(femb_no=femb, ext_lemo=0, rst_fe=1, mon_type=1, mon_chip = asic)
        result_dict["Mon_LArASIC{:02d}_Temperature".format(asic)] = tmp
    #    print (result_dict["ADC{:02d}_MeasRef".format(asic)]) 
        
    
    print ("Start FEMB configuration: 14mV/fC, 900mV BL, 2.0us, single-ended, 500pA, ASICDAC=0x10, Cali_enable, SDC off")
    tcp.set_fe_reset()
    tcp.set_fe_board(sts=1,snc=0,sg0=0,sg1=0,st0=1,st1=1,swdac=1,dac=0x10)
    tcp.femb_cfg()
    
    #check channel response
    print ("Check channel response")
    tcp.cd_fe_cali()
    tcp.fc_act_cal() #enalbe LArASIC calibration
    
    hdf_fp = save_dir + "rawdata.h5"
    result_dict["H5"] = hdf_fp
    
    udp.write_reg_wib_checked(2, 1)
    time.sleep(1)
    print("Enable UDP data stream")
    udp.write_reg_wib_checked(2, 1)
    time.sleep(1)
    ASICs = 8
    
    #to avoid potential cache data in PC
    asic=0
    wib_asic = (((femb << 16) & 0x000F0000) + ((asic << 8) & 0xFF00))
    udp.write_reg_wib_checked(7, 0x80000000)
    udp.write_reg_wib_checked(7, wib_asic | 0x80000000)
    udp.write_reg_wib_checked(7, wib_asic)
    time.sleep(0.01)
    data = udp.get_rawdata_packets(val=1000)
    
    femb_data = []
    dset = [ [] for i in range(128)]
    if os.path.isfile(hdf_fp):
        os.remove(hdf_fp)
    with h5py.File(hdf_fp, "a") as f:
        for asic in range(ASICs):
            print("FEMB{} ASIC{} is selected".format(femb, asic))
            chip_data = None
            while True:
                asic = asic & 0x0F
                wib_asic = (((femb << 16) & 0x000F0000) + ((asic << 8) & 0xFF00))
                udp.write_reg_wib_checked(7, 0x80000000)
                udp.write_reg_wib_checked(7, wib_asic | 0x80000000)
                udp.write_reg_wib_checked(7, wib_asic)
                time.sleep(0.01)
            #    fn = "Rawdata_" + data_time + "_" + strin + "_FEMB{}_ASIC{}".format(femb,asic) + ".bin"
            #    if "RMS" in strin:
            #        val = 20000
            #    else:
                val = 1000
                data = udp.get_rawdata_packets(val=val)
                chip_data = conv.raw_conv_feedloc(data)
                if chip_data != None:
                    femb_data.append(chip_data)
                    for i in range(16):
                        dset[i] = f.create_dataset('CH{}'.format(asic*16 + i), (len(chip_data[i]),), maxshape=(None,), dtype='u2', chunks=True) 
                        dset[i][:] = chip_data[i]
                    break
        print ("Start data analysis...")
        ana = data_ana(femb_data)
    
    print ("Measure power consumption...")
    pwr_info = tcp.femb_pwr_rd(femb=femb)
    result_dict["power_vfe_ref"] =  (v_fe,  iref_fe)
    result_dict["power_vadc_ref"] = (v_adc, iref_adc)
    result_dict["power_vcd_ref"] =  (v_cd,  iref_cd,)
    result_dict["power_bias_ref"] = (v_bias,iref_bias)
    result_dict["power_vfe_meas"] =  pwr_info[0]
    result_dict["power_vadc_meas"] = pwr_info[1]
    result_dict["power_vcd_meas"] =  pwr_info[2]
    result_dict["power_bias_meas"] = pwr_info[3]
    result_dict["RMS_noise"] = ana[0]
    reulst_dict["PEDS"] = ana[1]
    reulst_dict["Peak_p"] = ana[2]
    reulst_dict["Peak_n"] = ana[3]
    reulst_dict["Onewave"] = ana[4]
    reulst_dict["Average"] = ana[5]
    
    
    fn = FEMB_PLOT(ana[0],ana[1],ana[2],ana[3],ana[4],ana[5],save_dir)
    result_dict["response.png"] = fn
    generate_report(result_dict)
    
    print ("Turn FEMB off")
    tcp.femb_pwr_set(femb=femb, pwr_on=0)
    
    print ("Test is done...")
    print ("Report is saved at {}".format(result_dict["save_dir"]))
    
    
# save the test setting information
rootdir ="D:/IO_1826_1B/CHKOUT/"
tester = input ("please input your name: ")
env_cs = input("Test is performed at cold(LN2) (Y/N)? : ")
if ("Y" in env_cs) or ("y" in env_cs):
     env = "LN"
else:
     env = "RT"
ToyTPC_en = input("ToyTPC at FE inputs (Y/N) : ")
note = input("A short note (<80 letters):")
if ("Y" in ToyTPC_en) or ("y" in ToyTPC_en):
     ToyTPC = "150pF"
else:
     ToyTPC = "0pF"

# record the FEMB number
FEMB_sn=[]

for i in range(4):
    have_FEMB = input ("Is there a FEMB in slot "+str(i)+" (Y/N): ")
    if have_FEMB=="Y" or have_FEMB=="y":
        femb_sn = int(input ("please input FEMB SN (000-999): "))
        FEMB_sn.append(femb_sn)

if not FEMB_sn:
    sys.exit("no FEMB sn input")
else:
    femb=0
    for femb_sn in FEMB_sn:
        save_dir = rootdir + "FEMB{:03d}_{}_{}/".format(femb_sn, env, ToyTPC)
        save_dir = FEMB_CHKOUT_folder(save_dir)
        FEMB_CHK(rootdir, save_dir, femb, femb_sn, env, tester, ToyTPC, note)
        femb = femb+1


