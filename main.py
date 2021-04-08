# -*- coding: utf-8 -*-
"""
File Name: cls_femb_config.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:50:34 PM
Last modified: 4/8/2021 10:24:15 AM
"""

import numpy as np
import sys
import os
import string
import time
from datetime import datetime
from cls_udp import CLS_UDP


datadir = "D:/CM_FEMB_P2/Rawdata/"
#datadir = "D:/CM_FEMB/CEbox/"
now = datetime.now()
data_time = now.strftime("%m_%d_%Y_%H_%M_%S")
strin = input("Enter file name without space:")

udp = CLS_UDP()
udp.write_reg_wib_checked(2, 1)
time.sleep(1)
print("Enable UDP data stream")
udp.write_reg_wib_checked(2, 1)
time.sleep(1)
FEMBs = [0,1,2,3] 
FEMBs = [0]
#FEMBs = [1] 
ASICs = 8

femb=0
asic=0
wib_asic = (((femb << 16) & 0x000F0000) + ((asic << 8) & 0xFF00))
udp.write_reg_wib_checked(7, 0x80000000)
udp.write_reg_wib_checked(7, wib_asic | 0x80000000)
udp.write_reg_wib_checked(7, wib_asic)
time.sleep(0.01)
data = udp.get_rawdata_packets(val=1000)

for femb in FEMBs:
    for asic in range(ASICs):
        print("FEMB{} ASIC{} is selected".format(femb, asic))
        asic = asic & 0x0F
        wib_asic = (((femb << 16) & 0x000F0000) + ((asic << 8) & 0xFF00))
        udp.write_reg_wib_checked(7, 0x80000000)
        udp.write_reg_wib_checked(7, wib_asic | 0x80000000)
        udp.write_reg_wib_checked(7, wib_asic)
        time.sleep(0.01)
        fn = "Rawdata_" + data_time + "_" + strin + "_FEMB{}_ASIC{}".format(femb,asic) + ".bin"
        if "RMS" in strin:
            val = 50000
        else:
            val = 10000
        data = udp.get_rawdata_packets(val=val)
        with open(datadir + fn, "wb") as fp:
            fp.write(data)

print("Done")
#print (udp.read_reg_wib(2))




