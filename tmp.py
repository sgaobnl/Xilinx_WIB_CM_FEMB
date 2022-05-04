# -*- coding: utf-8 -*-
"""
File Name: cls_femb_config.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:50:34 PM
Last modified: 4/7/2022 10:52:54 AM
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


print ("Generator the test report...")
import datetime
now = datetime.datetime.now()
from fpdf import FPDF
result_dict = {}
result_dict["Tester"] = "SG"
result_dict["FEMB_SN"] = 0
result_dict["WIB_TCP_FW_ver"] = 0
result_dict["WIB_UDP_FW_ver"] = 0
result_dict["Env"] = "RT"
result_dict["Cd"] = "RT"
result_dict["FE_CFG"] = "14mV/fC, 900mV BL, 2.0us, SE_OFF, 500pA, ASIC_CAL, ASICDAC=0x10"
result_dict["ADC_CFG0"] = "CMOS reference set to default, Auto Calibration, "  
result_dict["ADC_CFG1"] = "SE, SDC off, offset_binary_format, Auto Calibration, "  
result_dict["CD_FE_pulse"] = "500samples/pulse, CD Addr0x06=0x30, Addr0x07=0x00, Addr0x08=0x38, Addr0x09=0x80"  

pdf = FPDF(orientation = 'P', unit = 'mm', format='Letter')
pdf.alias_nb_pages()

print ("##### FEMB Checkout Test Report #####")
pdf.add_page()
pdf.set_font('Times', 'B', 20)
pdf.cell(85)
print (pdf.l_margin)
pdf.l_margin = pdf.l_margin*2
pdf.cell(30, 5, 'FEMB{:03d} Checkout Test Report'.format(result_dict["FEMB_SN"]), 0, 1, 'C')
pdf.ln(10)

pdf.set_font('Times', '', 12)
pdf.cell(30, 5, 'Date&Time: %s'%now.strftime("%Y-%m-%d %H:%M:%S"), 0, 0)
pdf.cell(80)
pdf.cell(30, 5, 'Tester: {}'.format(result_dict["Tester"]), 0, 1)


pdf.cell(30, 5, 'WIB_TCP_Version: 0x{:02x}'.format(result_dict["WIB_TCP_FW_ver"]), 0, 0)
pdf.cell(80)
pdf.cell(30, 5, 'WIB_UDP_Version: 0x{:02x}'.format(result_dict["WIB_UDP_FW_ver"]), 0, 1)

pdf.cell(30, 5, 'Temperature: {}'.format(result_dict["Env"]), 0, 0)
pdf.cell(80)
pdf.cell(30, 5, 'Input Capacitor(Cd): {}pF'.format(result_dict["Cd"]), 0, 1)

print ("# FEMB configuration #")
pdf.ln(5)
pdf.cell(85)
pdf.cell(30, 5, 'FEMB Configuration' , 0, 1, 'C')
pdf.cell(30, 5, 'FE_CFG: {}'.format(result_dict["FE_CFG"]), 0, 1)
pdf.cell(30, 5, 'ADC_CFG0: {}'.format(result_dict["ADC_CFG0"]), 0, 1)
pdf.cell(30, 5, 'ADC_CFG0: {}'.format(result_dict["ADC_CFG1"]), 0, 1)
pdf.cell(30, 5, 'CD_FE_pulse: {}'.format(result_dict["CD_FE_pulse"]), 0, 1)


# Generate Power Check table
print ("# Generate Power Check table")
pdf.ln(5)
pdf.cell(85)
pdf.cell(30, 5, 'Power Consumption (including cable dissapation)' , 0, 1, 'C')
# Colon width is 1/4 of effective page width
epw = pdf.w - 2*pdf.l_margin
col_width = epw/5
pdf.set_font('Times', '', 12) 
#with open(rawdir + 'Power_Check/Power_Check_CMOS.csv', "r") as csvfile:
#    data = list(csv.reader(csvfile))
data=[["Power rail","V_set /V","V_meas /V","I_meas /mA","P_meas /mW"],
      ["LArASIC", 2, 3,4,5], 
      ["ColdADC", 2, 3,4,5], 
      ["COLDATA", 2, 3,4,5], 
      [" BIAS  ", 2, 3,4,5] 
      ]

# Text height is the same as current font size
print ("# Text height is the same as current font size")
th = pdf.font_size 
pdf.ln(0.5*th)
for row in data:
    for datum in row:
        # pyFPDF expects a string, not a number
        pdf.cell(col_width, 2*th, str(datum), border=1, align='C')
    pdf.ln(2*th)

pdf.ln(5)

pdf.image("D:/IO_1826_1B/CHKOUT/FEMB000_0_0pF/response.png", 10, 150, 200)


filename = "D:/IO_1826_1B/CHKOUT/FEMB000_0_0pF/abc.pdf"
pdf.output(filename, 'F')
pdf.close()
#print (a)
#dataNtuple = struct.unpack_from(">%dQ"%(rd_len),a)
#for x in dataNtuple:
#    print (hex(x))
#print (dataNtuple)

#datadir = "D:/CM_FEMB_P2/Rawdata/"
#datadir = "D:/CM_FEMB/CEbox/"
#datadir = "D:/Monolithic_FEMB/Rawdata/"
#datadir = "D:/FEMB_IO1826_1A/Toy_PCB_TPC/"
#now = datetime.now()
#data_time = now.strftime("%m_%d_%Y_%H_%M_%S")
#strin = input("Enter file name without space:")
#print (strin)
#
#udp = CLS_UDP()
#udp.write_reg_wib_checked(2, 1)
#time.sleep(1)
#print("Enable UDP data stream")
#udp.write_reg_wib_checked(2, 1)
#time.sleep(1)
#FEMBs = [0,1,2,3] 
#FEMBs = [0]
##FEMBs = [1] 
#ASICs = 8
#
#femb=0
#asic=0
#wib_asic = (((femb << 16) & 0x000F0000) + ((asic << 8) & 0xFF00))
#udp.write_reg_wib_checked(7, 0x80000000)
#udp.write_reg_wib_checked(7, wib_asic | 0x80000000)
#udp.write_reg_wib_checked(7, wib_asic)
#time.sleep(0.01)
#data = udp.get_rawdata_packets(val=1000)
#
#for femb in FEMBs:
#    for asic in range(ASICs):
#        print("FEMB{} ASIC{} is selected".format(femb, asic))
#        asic = asic & 0x0F
#        wib_asic = (((femb << 16) & 0x000F0000) + ((asic << 8) & 0xFF00))
#        udp.write_reg_wib_checked(7, 0x80000000)
#        udp.write_reg_wib_checked(7, wib_asic | 0x80000000)
#        udp.write_reg_wib_checked(7, wib_asic)
#        time.sleep(0.01)
#        fn = "Rawdata_" + data_time + "_" + strin + "_FEMB{}_ASIC{}".format(femb,asic) + ".bin"
#        if "RMS" in strin:
#            val = 20000
#        else:
#            val = 2000
#        data = udp.get_rawdata_packets(val=val)
#        with open(datadir + fn, "wb") as fp:
#            fp.write(data)
#
#print("Done")
##print (udp.read_reg_wib(2))
#
#
#
#
