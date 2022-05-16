# -*- coding: utf-8 -*-
"""
File Name: cls_udp.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:52:43 PM
Last modified: 5/15/2022 10:37:42 AM
"""

import pickle

fp = "D:/IO_1826_1B/QC/FEMB222_LN_150pF/logs_tm008.bin"
with open(fp, 'rb') as fp:
    logs = pickle.load(fp)

for log in logs:
    print (log, logs[log])
