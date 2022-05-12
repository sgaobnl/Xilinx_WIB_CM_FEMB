# -*- coding: utf-8 -*-
"""
File Name: cls_udp.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:52:43 PM
Last modified: 5/12/2022 1:10:35 PM
"""

import numpy as np
import sys
import os
import string
import time
#from datetime import datetime
from QC_runs import QC_runs
import pickle

tm = int(sys.argv[1])

qc = QC_runs()
times = []
times.append(time.time())

if tm == 1:
    qc.FEMB_CHKOUT_Input()
    times.append(time.time())
    times.append(time.time())

with open("./fembs_on_wib.bin", 'rb') as fp:
    fembs_on_wib = pickle.load(fp)
qc.fembs_on_wib = fembs_on_wib

for femb_no in qc.fembs_on_wib:
    print ("FEMB on WIB SLOT {} is being tested".format(femb_no))
    qc.tcp.link_cs = 2*femb_no
    if tm == 2:
        qc.load_logs(femb_no=femb_no)
        qc.femb_initpwr_chk(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 3:
        qc.load_logs(femb_no=femb_no)
        qc.femb_pwr_meas(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 4:
        qc.load_logs(femb_no=femb_no)
        qc.femb_pwr_cycles(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 5:
        qc.load_logs(femb_no=femb_no)
        qc.femb_chks(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 6:
        qc.load_logs(femb_no=femb_no)
        qc.femb_rmss(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 7:
        qc.load_logs(femb_no=femb_no)
        qc.femb_asicdac_calis(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 8:
        qc.load_logs(femb_no=femb_no)
        qc.femb_mons(femb_no=femb_no)
        times.append(time.time())
        qc.dump_logs(tm=tm)
        times.append(time.time())
    
    if tm == 9:
        qc.load_logs(femb_no=femb_no)
        qc.close(femb_no=femb_no)
        times.append(time.time())

for dt in range (len(times)):
    if dt >=1:
        print (time.ctime(times[dt]), int(times[dt] - times[dt-1]))
    else:
        print (time.ctime(times[dt]))

