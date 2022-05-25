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

fp = "D:/IO_1826_1B/QC1/FEMB022_LN_150pF_R006/logs_tm008.bin"
with open(fp, 'rb') as fp:
    logs = pickle.load(fp)

for log in logs:
    print (log, logs[log])
