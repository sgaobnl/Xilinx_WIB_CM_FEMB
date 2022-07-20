# -*- coding: utf-8 -*-
"""
File Name: cls_udp.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:52:43 PM
Last modified: 5/25/2022 10:54:43 AM
"""

import pickle

fp = "/home/hanjie/Desktop/protoDUNE/cold_electronics/FEMB_QC/FEMB_QC_data/FEMB346_LN_150pF/logs_tm004.bin"
with open(fp, 'rb') as fp:
    logs = pickle.load(fp)

for log in logs:
    print (log)

print(len(logs['D:/IO_1826_1B/QC/FEMB346_LN_150pF/PWR/power_cycle2_CHK_response_SE.h5'][4][0]))
