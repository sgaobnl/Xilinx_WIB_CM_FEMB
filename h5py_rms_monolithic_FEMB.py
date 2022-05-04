# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 3/5/2022 12:43:47 AM
"""

#defaut setting for scientific caculation
#import numpy
#import scipy
#from numpy import *
#import numpy as np
#import scipy as sp
#import pylab as pl
import numpy as np
import struct
import os
#import file
import h5py
import copy
#from matplotlib.backends.backend_pdf import PdfPages
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches
#from apa_mapping import APA_MAP 
#apa40 = APA_MAP()
#xchns = apa40.apa_mapping()[1]
#uchns = apa40.apa_mapping()[2]
#vchns = apa40.apa_mapping()[3]

#fdir = "D:/Monolithic_FEMB/Rawdata/"
fdir = "D:/FEMB_IO1826_1A/Rawdata_P4CD_2/"
frst = fdir +  "results/"
#rt_fp05 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#ln_fp10 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#ln_fp20 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#ln_fp30 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"


#rt_fp05 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_RMS_S16ON_VDDP.h5"
#ln_fp10 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1410_RMS_S16ON_VDDP.h5"
#ln_fp20 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_RMS_S16ON_VDDP.h5"
#ln_fp30 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_RMS_S16ON_VDDP.h5"
#
#rt_fp05 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1405_RMS_S16ON_VDDP.h5"
#ln_fp10 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1410_RMS_S16ON_VDDP.h5"
#ln_fp20 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_RMS_S16ON_VDDP.h5"
#ln_fp30 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS_S16ON_VDDP.h5"
##
#rt_fp05 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1405_RMS_S16ON_VDDP.h5"
#ln_fp10 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1410_RMS_S16ON_VDDP.h5"
#ln_fp20 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_RMS_S16ON_VDDP.h5"
#ln_fp30 = "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1430_RMS_S16ON_VDDP.h5"
##
#rt_fp05 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1405_RMS_S16ON_VDDP.h5"
#ln_fp10 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1410_RMS_S16ON_VDDP.h5"
#ln_fp20 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_RMS_S16ON_VDDP.h5"
#ln_fp30 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1430_RMS_S16ON_VDDP.h5"
##
#rt_fp05 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FERT_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1405_S16ON_RMSP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1405_RMS_S16ON_VDDP.h5"
#ln_fp10 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1410_RMS_S16ON_VDDP.h5"
#ln_fp20 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_RMS_S16ON_VDDP.h5"
#ln_fp30 = "LN_150pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1430_RMS_S16ON_VDDP.h5"
#
#
#
#
#rt_fp05 = "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_RMS_S16ON.h5"
#ln_fp10 = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1410_RMS_S16ON.h5"
#ln_fp20 = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_RMS_S16ON.h5"
#ln_fp30 = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_RMS_S16ON.h5"
#
#rt_fp05 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#ln_fp10 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#ln_fp20 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#ln_fp30 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"
###
#rt_fp05 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1405_RMS_S16ON.h5"
#ln_fp10 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1410_RMS_S16ON.h5"
#ln_fp20 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_RMS_S16ON.h5"
#ln_fp30 = "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1430_RMS_S16ON.h5"
###
#rt_fp05 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1405_RMS_S16ON.h5"
#ln_fp10 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1410_RMS_S16ON.h5"
#ln_fp20 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_RMS_S16ON.h5"
#ln_fp30 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1430_RMS_S16ON.h5"
###
#rt_fp05 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#rt_fp10 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#rt_fp20 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#rt_fp30 = "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"
#ln_fp05 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1405_RMS_S16ON.h5"
#ln_fp10 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1410_RMS_S16ON.h5"
#ln_fp20 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_RMS_S16ON.h5"
#ln_fp30 = "LN_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1430_RMS_S16ON.h5"

#rt_fp05 = "RT_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1405_S16ON_RMS.h5"
#rt_fp10 = "RT_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1410_S16ON_RMS.h5"
#rt_fp20 = "RT_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_RMS.h5"
#rt_fp30 = "RT_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1430_S16ON_RMS.h5"
#ln_fp05 = "LN_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1405_S16ON_RMS.h5"
#ln_fp10 = "LN_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1410_S16ON_RMS.h5"
#ln_fp20 = "LN_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_RMS.h5"
#ln_fp30 = "LN_CAP002_150pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1430_S16ON_RMS.h5"

rt_fp05 = "RT_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1405_S16ON_RMS.h5"
rt_fp10 = "RT_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1410_S16ON_RMS.h5"
rt_fp20 = "RT_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_RMS.h5"
rt_fp30 = "RT_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1430_S16ON_RMS.h5"
ln_fp05 = "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1405_S16ON_RMS.h5"
ln_fp10 = "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1410_S16ON_RMS.h5"
ln_fp20 = "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_RMS.h5"
ln_fp30 = "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1430_S16ON_RMS.h5"

a1 = rt_fp05.find("_RMS")
p_title = rt_fp05[3:a1] 


rt_f05 = h5py.File(fdir + rt_fp05, 'r')
rt_f10 = h5py.File(fdir + rt_fp10, 'r')
rt_f20 = h5py.File(fdir + rt_fp20, 'r')
rt_f30 = h5py.File(fdir + rt_fp30, 'r')

ln_f05 = h5py.File(fdir + ln_fp05, 'r')
ln_f10 = h5py.File(fdir + ln_fp10, 'r')
ln_f20 = h5py.File(fdir + ln_fp20, 'r')
ln_f30 = h5py.File(fdir + ln_fp30, 'r')

rt_keys05 = list(ln_f05.keys())
rt_keys10 = list(ln_f10.keys())
rt_keys20 = list(ln_f20.keys())
rt_keys30 = list(ln_f30.keys())

ln_keys05 = list(ln_f05.keys())
ln_keys10 = list(ln_f10.keys())
ln_keys20 = list(ln_f20.keys())
ln_keys30 = list(ln_f30.keys())

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})

keyss = [rt_keys10, ln_keys10]
rtfs = [rt_f05, rt_f10, rt_f20, rt_f30]
lnfs = [ln_f05, ln_f10, ln_f20, ln_f30]
femb_no = 1

rmss_tp = []
for i in range(9):
    plt.vlines(16*i, 0, 10, linestyles="dashed", color='gray')

for i in range(4):
    keys = keyss[0]
    chnos = np.arange(128*femb_no)
    peds =  [0]*128*femb_no
    rmss =  [0]*128*femb_no
    dlen = 10000
    for key in keys:
        chno = int(key[2:])
        y = rtfs[i][key][0:dlen]
        ped = np.mean(y)
        rms = np.std(y)
        chnos[chno] = chno
        peds[chno] = ped
        rmss[chno] = rms
    if i == 0:
        tp = "0.5us"
    elif i == 1:
        tp = "1.0us"
    elif i == 2:
        tp = "2.0us"
    elif i == 3:
        tp = "3.0us"
    #plt.plot((np.array(chnos)-128*0)[128*0:128*1], rmss[128*0:128*1],  marker = 'x', color ="C%d"%i, label="RT, BL200mV, 14mV/fC, " + tp)
    #plt.plot((np.array(chnos)-128*0)[0:16], rmss[32:48],  marker = 'x', color ="C%d"%i, label="RT, BL200mV, 14mV/fC, " + tp)
    #plt.plot((np.array(chnos)-128*0)[64:128], rmss[64:128],  marker = 'x', color ="C%d"%i, label="RT, BL200mV, 14mV/fC, " + tp)
    plt.plot((np.array(chnos)-128*0), rmss,  marker = 'x', color ="C%d"%i, label="RT, BL200mV, 14mV/fC, " + tp)
    rmss_tp.append(["RT", i, rmss])

    keys = keyss[1]
    chnos = np.arange(128*femb_no)
    peds =  [0]*128*femb_no
    rmss =  [0]*128*femb_no
    dlen = 10000
    for key in keys:
        chno = int(key[2:])
        y = lnfs[i][key][0:dlen]
        ped = np.mean(y)
        rms = np.std(y)
        chnos[chno] = chno
        peds[chno] = ped
        rmss[chno] = rms
    if i == 0:
        tp = "0.5$\mu$s"
    elif i == 1:
        tp = "1.0$\mu$s"
    elif i == 2:
        tp = "2.0$\mu$s"
    elif i == 3:
        tp = "3.0$\mu$s"
    #plt.plot((np.array(chnos)-128*0)[128*0:128*1], rmss[128*0:128*1],  marker = '.', color ="C%d"%(i+4), label="LN, BL900mV, 14mV/fC, " + tp)
    #plt.plot((np.array(chnos)-128*0)[0:16], rmss[32:48],  marker = '.', color ="C%d"%i, label="LN, BL200mV, 14mV/fC, " + tp)
    #plt.plot((np.array(chnos)-128*0)[64:128], rmss[64:128],  marker = '.', color ="C%d"%i, label="LN, BL200mV, 14mV/fC, " + tp)
    plt.plot((np.array(chnos)-128*0), rmss,  marker = '.', color ="C%d"%i, label="LN, BL200mV, 14mV/fC, " + tp)
    rmss_tp.append(["LN", i, rmss])
    #plt.plot((np.array(chnos)-128*1)[128*1:128*2], encs[128*1:128*2],  marker = 'o', color ="C%d"%i, label="LN, 14mV/fC(200 e-/bin)," + tp)
    #encs_tp.append(encs[128*1:128*2])
#    plt.plot((np.array(chnos)-128*2)[128*2:128*3], peds[128*1:128*2],  marker = 'o', color ="C%d"%i, label="LN, 14mV/fC," + tp)
#    plt.plot((np.array(chnos)-128*1)[128*1:128*2], rt_enc,  marker = 's', color ="C3", label="RT, 14mV/fC(195 e-/bin), 1.0us")

#plt.title ("Noise Disctribution of FEMB (150pF Toy TPC)") 
plt.title ("Noise Disctribution of FEMB") 
plt.xlabel("Channel Number")
plt.ylabel("RMS Noise \ bit")
#plt.xlim((-1, 199))
plt.ylim((0, 10))
#plt.grid()
plt.legend(loc=4,fontsize=8)
#plt.show()
plt.savefig(frst+ p_title + "_pls_noise_dis.png")
plt.close()

#exit()

fig = plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})
x = [0.5, 1.0, 2.0, 3.0]
rt_rmsm = [0, 0, 0, 0]
rt_rmsstd = [0, 0, 0, 0]
ln_rmsm = [0, 0, 0, 0]
ln_rmsstd = [0, 0, 0, 0]
for tmp in rmss_tp:
    if tmp[0] == "RT":
        #ttmp = np.delete(np.array(tmp[2]), 95)
        #ttmp = tmp[2][49:64]
        #ttmp = tmp[2][32:48]
#        ttmp = tmp[2][49:64] + tmp[2][112:128]
        ttmp = tmp[2]
        m = np.mean(ttmp)
        std = np.std(ttmp)
        rt_rmsm[tmp[1]] = m
        rt_rmsstd[tmp[1]] = std 
    elif tmp[0] == "LN":
        #ttmp = tmp[2][32:48]
        ttmp = tmp[2]
        m = np.mean(ttmp)
        std = np.std(ttmp)
        ln_rmsm[tmp[1]] = m
        ln_rmsstd[tmp[1]] = std 
plt.errorbar(x, rt_rmsm, rt_rmsstd, label="RT", color='r', marker='o')
plt.errorbar(x, ln_rmsm, ln_rmsstd, label="LN", color='b', marker='^')
for i in range(4):
    plt.text(x[i]+0.1, rt_rmsm[i], "%.3f"%rt_rmsm[i])
for i in range(4):
    plt.text(x[i]+0.1, ln_rmsm[i], "%.3f"%ln_rmsm[i])
plt.xlabel("peaking time / ($\mu$s)")
plt.ylabel("RMS Noise / (bin)")
plt.xlim((0,3.5))
plt.ylim((0,10))
plt.legend()
plt.grid()
#plt.show()
plt.savefig(frst+ p_title + "_pls_noise_rms.png")
plt.close()

import pickle
#lnfg = frst + "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x08_S16O_gain_dis.bin"
#rtfg = frst + "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x08_S16O_gain_dis.bin"
fdir2 = "D:/FEMB_IO1826_1A/Rawdata_P4CD/"
frst2 = fdir2 +  "results/"
lnfg = frst2 + "LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x0_gain_dis.bin"
rtfg = frst2 + "RT_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x0_gain_dis.bin"

with open(lnfg, 'rb') as fn:
    lngains = pickle.load(fn)
avg_gainln = np.mean(lngains)
print (avg_gainln)
with open(rtfg, 'rb') as fn:
    rtgains = pickle.load(fn)
avg_gainrt = np.mean(rtgains)
print (avg_gainrt)

rt_encxtps_m = np.array(rt_rmsm) * avg_gainrt 
rt_encxtps_s = np.array(rt_rmsstd) * avg_gainrt 
ln_encxtps_m = np.array(ln_rmsm) * avg_gainln 
ln_encxtps_s = np.array(ln_rmsstd) * avg_gainln 

fig = plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})
x = [0.5, 1.0, 2.0, 3.0]
plt.errorbar(x, rt_encxtps_m, rt_encxtps_s, label="RT", color='r', marker='o')
plt.errorbar(x, ln_encxtps_m, ln_encxtps_s, label="LN", color='b', marker='^')
for i in range(4):
    plt.text(x[i]+0.05, rt_encxtps_m[i]+50, "%d"%rt_encxtps_m[i])
for i in range(4):
    plt.text(x[i]+0.05, ln_encxtps_m[i] +50, "%d"%ln_encxtps_m[i])
plt.xlabel("peaking time / ($\mu$s)")
plt.ylabel("ENC / (e-) ")
plt.xlim((0,3.5))
plt.ylim((0, 1500))
plt.grid()
plt.legend(loc=1, fontsize=18)

#plt.legend()
#plt.grid()
#plt.show()
plt.savefig(frst+ p_title + "_pls_noise_enc.png")
plt.close()

exit()

rt_encxtps_m_0pF = rt_encxtps_m 
ln_encxtps_m_0pF = ln_encxtps_m 
rt_encxtps_s_0pF = rt_encxtps_s 
ln_encxtps_s_0pF = ln_encxtps_s 


rt_fp05 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_RMS_S16ON.h5"
rt_fp10 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1410_RMS_S16ON.h5"
rt_fp20 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_RMS_S16ON.h5"
rt_fp30 = "RT_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_RMS_S16ON.h5"
ln_fp05 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_RMS_S16ON.h5"
ln_fp10 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1410_RMS_S16ON.h5"
ln_fp20 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_RMS_S16ON.h5"
ln_fp30 = "LN_150pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_RMS_S16ON.h5"

rt_f05 = h5py.File(fdir + rt_fp05, 'r')
rt_f10 = h5py.File(fdir + rt_fp10, 'r')
rt_f20 = h5py.File(fdir + rt_fp20, 'r')
rt_f30 = h5py.File(fdir + rt_fp30, 'r')

ln_f05 = h5py.File(fdir + ln_fp05, 'r')
ln_f10 = h5py.File(fdir + ln_fp10, 'r')
ln_f20 = h5py.File(fdir + ln_fp20, 'r')
ln_f30 = h5py.File(fdir + ln_fp30, 'r')

rt_keys05 = list(ln_f05.keys())
rt_keys10 = list(ln_f10.keys())
rt_keys20 = list(ln_f20.keys())
rt_keys30 = list(ln_f30.keys())

ln_keys05 = list(ln_f05.keys())
ln_keys10 = list(ln_f10.keys())
ln_keys20 = list(ln_f20.keys())
ln_keys30 = list(ln_f30.keys())

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 8})

keyss = [rt_keys10, ln_keys10]
rtfs = [rt_f05, rt_f10, rt_f20, rt_f30]
lnfs = [ln_f05, ln_f10, ln_f20, ln_f30]
femb_no = 1

rmss_tp = []
for i in range(4):
    keys = keyss[0]
    chnos = np.arange(128*femb_no)
    peds =  [0]*128*femb_no
    rmss =  [0]*128*femb_no
    dlen = 10000
    for key in keys:
        chno = int(key[2:])
        y = rtfs[i][key][0:dlen]
        ped = np.mean(y)
        rms = np.std(y)
        chnos[chno] = chno
        peds[chno] = ped
        rmss[chno] = rms
    if i == 0:
        tp = "0.5us"
    elif i == 1:
        tp = "1.0us"
    elif i == 2:
        tp = "2.0us"
    elif i == 3:
        tp = "3.0us"
    #plt.plot((np.array(chnos)-128*0)[128*0:128*1], rmss[128*0:128*1],  marker = 'x', color ="C%d"%i, label="RT, BL200mV, 14mV/fC, " + tp)
    #plt.plot((np.array(chnos)-128*0)[0:16], rmss[32:48],  marker = 'x', color ="C%d"%i, label="RT, BL200mV, 14mV/fC, " + tp)
    plt.plot((np.array(chnos)-128*0)[128*0:128*1], rmss[128*0:128*1],  marker = 'x', color ="C%d"%(i+4), label="RT, BL900mV, 14mV/fC, " + tp)
    rmss_tp.append(["RT", i, rmss])

    keys = keyss[1]
    chnos = np.arange(128*femb_no)
    peds =  [0]*128*femb_no
    rmss =  [0]*128*femb_no
    dlen = 10000
    for key in keys:
        chno = int(key[2:])
        y = lnfs[i][key][0:dlen]
        ped = np.mean(y)
        rms = np.std(y)
        chnos[chno] = chno
        peds[chno] = ped
        rmss[chno] = rms
    if i == 0:
        tp = "0.5$\mu$s"
    elif i == 1:
        tp = "1.0$\mu$s"
    elif i == 2:
        tp = "2.0$\mu$s"
    elif i == 3:
        tp = "3.0$\mu$s"
    plt.plot((np.array(chnos)-128*0)[128*0:128*1], rmss[128*0:128*1],  marker = '.', color ="C%d"%(i+4), label="LN, BL900mV, 14mV/fC, " + tp)
    #plt.plot((np.array(chnos)-128*0)[0:16], rmss[32:48],  marker = '.', color ="C%d"%i, label="LN, BL200mV, 14mV/fC, " + tp)
    rmss_tp.append(["LN", i, rmss])
    #plt.plot((np.array(chnos)-128*1)[128*1:128*2], encs[128*1:128*2],  marker = 'o', color ="C%d"%i, label="LN, 14mV/fC(200 e-/bin)," + tp)
    #encs_tp.append(encs[128*1:128*2])
#    plt.plot((np.array(chnos)-128*2)[128*2:128*3], peds[128*1:128*2],  marker = 'o', color ="C%d"%i, label="LN, 14mV/fC," + tp)
#    plt.plot((np.array(chnos)-128*1)[128*1:128*2], rt_enc,  marker = 's', color ="C3", label="RT, 14mV/fC(195 e-/bin), 1.0us")

plt.title ("Noise Disctribution of FEMB (150pF Toy TPC)") 
plt.xlabel("Channel Number")
plt.ylabel("RMS Noise \ bit")
#plt.xlim((-1, 199))
#plt.ylim((0, 10))
plt.grid()
plt.legend()
#plt.show()
#plt.savefig(frst+ "pls_noise_dis.png")
plt.close()

#exit()

fig = plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})
x = [0.5, 1.0, 2.0, 3.0]
rt_rmsm = [0, 0, 0, 0]
rt_rmsstd = [0, 0, 0, 0]
ln_rmsm = [0, 0, 0, 0]
ln_rmsstd = [0, 0, 0, 0]
for tmp in rmss_tp:
    if tmp[0] == "RT":
        #ttmp = np.delete(np.array(tmp[2]), 95)
        #ttmp = tmp[2][49:64]
        #ttmp = tmp[2][112:128]
#        ttmp = tmp[2][49:64] + tmp[2][112:128]
        ttmp = tmp[2]
        m = np.mean(ttmp)
        std = np.std(ttmp)
        rt_rmsm[tmp[1]] = m
        rt_rmsstd[tmp[1]] = std 
    elif tmp[0] == "LN":
        #ttmp = tmp[2][112:128]
        ttmp = tmp[2]
        m = np.mean(ttmp)
        std = np.std(ttmp)
        ln_rmsm[tmp[1]] = m
        ln_rmsstd[tmp[1]] = std 
plt.errorbar(x, rt_rmsm, rt_rmsstd, label="RT", color='r', marker='o')
plt.errorbar(x, ln_rmsm, ln_rmsstd, label="LN", color='b', marker='^')
for i in range(4):
    plt.text(x[i]+0.1, rt_rmsm[i], "%.3f"%rt_rmsm[i])
for i in range(4):
    plt.text(x[i]+0.1, ln_rmsm[i], "%.3f"%ln_rmsm[i])
plt.xlabel("peaking time / ($\mu$s)")
plt.ylabel("RMS Noise / (bin)")
plt.xlim((0,3.5))
plt.ylim((0,10))
plt.legend()
plt.grid()
#plt.show()
plt.savefig(frst+ "pls_noise_rms.png")
plt.close()

import pickle
lnfg = frst + "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_GAIN_ADAC0x08_S16O_gain_dis.bin"
rtfg = frst + "LN_150pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_GAIN_ADAC0x08_S16O_gain_dis.bin"
with open(lnfg, 'rb') as fn:
    lngains = pickle.load(fn)
avg_gainln = np.mean(lngains)
print (avg_gainln)
with open(rtfg, 'rb') as fn:
    rtgains = pickle.load(fn)
avg_gainrt = np.mean(rtgains)
print (avg_gainrt)

rt_encxtps_m = np.array(rt_rmsm) * avg_gainrt 
rt_encxtps_s = np.array(rt_rmsstd) * avg_gainrt 
ln_encxtps_m = np.array(ln_rmsm) * avg_gainln 
ln_encxtps_s = np.array(ln_rmsstd) * avg_gainln 

fig = plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 16})
x = [0.5, 1.0, 2.0, 3.0]
plt.errorbar(x, rt_encxtps_m, rt_encxtps_s, label="RT, 150pF Cd", color='r', marker='o')
plt.errorbar(x, rt_encxtps_m_0pF, rt_encxtps_s_0pF, label="RT, 0pF Cd", color='m', marker='*')
plt.errorbar(x, ln_encxtps_m, ln_encxtps_s, label="LN, 150pF Cd", color='b', marker='^')
plt.errorbar(x, ln_encxtps_m_0pF, ln_encxtps_s_0pF, label="LN, 0pF Cd", color='g', marker='>')
for i in range(4):
    plt.text(x[i]-0.15, rt_encxtps_m[i]+50, "%d"%rt_encxtps_m[i], color = 'r')
for i in range(4):
    plt.text(x[i]-0.15, rt_encxtps_m_0pF[i]-100, "%d"%rt_encxtps_m_0pF[i], color = 'm')

for i in range(4):
    plt.text(x[i]-0.15, ln_encxtps_m[i] +50, "%d"%ln_encxtps_m[i], color = 'b')
for i in range(4):
    plt.text(x[i]-0.15, ln_encxtps_m_0pF[i]-100, "%d"%ln_encxtps_m_0pF[i], color = 'g')

plt.xlabel("peaking time / ($\mu$s)")
plt.ylabel("ENC / (e-) ")
plt.xlim((0,3.5))
plt.ylim((0, 1500))
plt.grid()
plt.legend(loc=1, fontsize=18)

#plt.legend()
#plt.grid()
#plt.show()
plt.savefig(frst+ "pls_noise_rms_all.png")
plt.close()



#encxtps_s = [np.std (encx_05), np.std (encx_10), np.std (encx_20), np.std (encx_30)]
#encutps_m = [np.mean(encu_05), np.mean(encu_10), np.mean(encu_20), np.mean(encu_30)]
#encutps_s = [np.std (encu_05), np.std (encu_10), np.std (encu_20), np.std (encu_30)]
#encvtps_m = [np.mean(encv_05), np.mean(encv_10), np.mean(encv_20), np.mean(encv_30)]
#encvtps_s = [np.std (encv_05), np.std (encv_10), np.std (encv_20), np.std (encv_30)]
#encotps_m = [np.mean(enco_05), np.mean(enco_10), np.mean(enco_20), np.mean(enco_30)]
#encotps_s = [np.std (enco_05), np.std (enco_10), np.std (enco_20), np.std (enco_30)]
#
#
#import matplotlib.pyplot as plt
#fig = plt.figure(figsize=(12, 8))
#plt.rcParams.update({'font.size': 24})
#tps = [0.5, 1.0, 2.0, 3.0]
#plt.errorbar(tps, encxtps_m, encxtps_s, marker = 'o', color = 'g', label = "%d X wires"%(len(xchns_r) ))
#plt.errorbar(tps, encutps_m, encutps_s, marker = '>', color = 'r', label = "%d U wires"%(len(uchns_r)))
#plt.errorbar(tps, encvtps_m, encvtps_s, marker = 's', color = 'b', label = "%d V wires"%(len(vchns_r)))
#plt.errorbar(tps, encotps_m, encotps_s, marker = 'd', color = 'm', label = "%d Open CHs"%(len(openchns)))
#plt.text(0.2, 1000, "O:",  color = 'm', fontsize=18) 
#plt.text(0.5, 1000, int(encotps_m[0]), color = 'm', fontsize=18) 
#plt.text(1.0, 1000, int(encotps_m[1]), color = 'm', fontsize=18) 
#plt.text(2.0, 1000, int(encotps_m[2]), color = 'm', fontsize=18) 
#plt.text(3.0, 1000, int(encotps_m[3]), color = 'm', fontsize=18) 
#
#plt.text(0.2, 1300, "X:",  color = 'g', fontsize=18) 
#plt.text(0.5, 1300, int(encxtps_m[0]), color = 'g', fontsize=18) 
#plt.text(1.0, 1300, int(encxtps_m[1]), color = 'g', fontsize=18) 
#plt.text(2.0, 1300, int(encxtps_m[2]), color = 'g', fontsize=18) 
#plt.text(3.0, 1300, int(encxtps_m[3]), color = 'g', fontsize=18) 
#
#plt.text(0.2, 1200, "V:",  color = 'b', fontsize=18) 
#plt.text(0.5, 1200, int(encvtps_m[0]), color = 'b', fontsize=18) 
#plt.text(1.0, 1200, int(encvtps_m[1]), color = 'b', fontsize=18) 
#plt.text(2.0, 1200, int(encvtps_m[2]), color = 'b', fontsize=18) 
#plt.text(3.0, 1200, int(encvtps_m[3]), color = 'b', fontsize=18) 
#
#plt.text(0.2, 1100, "U:",  color = 'r', fontsize=18) 
#plt.text(0.5, 1100, int(encutps_m[0]), color = 'r', fontsize=18) 
#plt.text(1.0, 1100, int(encutps_m[1]), color = 'r', fontsize=18) 
#plt.text(2.0, 1100, int(encutps_m[2]), color = 'r', fontsize=18) 
#plt.text(3.0, 1100, int(encutps_m[3]), color = 'r', fontsize=18) 
#
#plt.ylim((0, 2000))
#plt.grid()
#plt.legend(loc=1, fontsize=18)
##plt.title("ENC Measurement ")
#plt.xlabel("Peak time / ($\mu$s)")
#plt.ylabel("ENC / (e-) ")
#plt.xlim((0,4))
#plt.show()
#plt.close()
#chnos = np.arange(128)
#for i in range(9):
#    plt.vlines(16*i, 0, 1500, linestyles="dashed", color='gray')



#fig = plt.figure(figsize=(12, 6))
#plt.rcParams.update({'font.size': 16})
#for i in [1]:
#    keys = keyss[0]
#    chnos = np.arange(512)
#    peds =  [0]*512
#    rmss =  [0]*512
#    dlen = 20000
#    for key in keys:
#        chno = int(key[2:])
#        y = rtfs[i][key][0:dlen]
#        ped = np.mean(y)
#        rms = np.std(y)
#        chnos[chno] = chno
#        peds[chno] = ped
#        rmss[chno] = rms
#    tp = "1.0us"
#    enc = np.array(rmss[128*0:128*1])*rtgains
#    tmp = copy.deepcopy(enc)
#    encmean = np.mean(np.delete(tmp, 91))
#    encstd = np.std(np.delete(tmp, 91))
#    #plt.plot((np.array(chnos)-128*0)[128*0:128*1], enc,  marker = 'x', color ="C%d"%i, label="RT, 14mV/fC, "+ tp + "\n ENC = %d $\pm$ %d"%(encmean, encstd))
#    plt.plot((np.array(chnos)-128*0)[128*0:64], enc[0:64],  marker = 'x', color ="C%d"%i, label="RT, 14mV/fC, "+ tp + "\n ENC = %d $\pm$ %d"%(encmean, encstd))
#
#    keys = keyss[1]
#    chnos = np.arange(512)
#    peds =  [0]*512
#    rmss =  [0]*512
#    dlen = 20000
#    for key in keys:
#        chno = int(key[2:])
#        y = lnfs[i][key][0:dlen]
#        ped = np.mean(y)
#        rms = np.std(y)
#        chnos[chno] = chno
#        peds[chno] = ped
#        rmss[chno] = rms
#    tp = "1.0us"
#    enc = np.array(rmss[128*0:128*1])*lngains
#    tmp = copy.deepcopy(enc)
#    encmean = np.mean(tmp[0:64])
#    encstd = np.std(tmp[0:64])
#    #plt.plot((np.array(chnos)-128*0)[128*0:128*1], enc,  marker = 'o', color ="C%d"%(i+4), label="LN, 14mV/fC, " + tp + "\n ENC = %d $\pm$ %d"%(encmean, encstd))
#    plt.plot((np.array(chnos)-128*0)[0:64], enc[0:64],  marker = 'o', color ="C%d"%(i+4), label="LN, 14mV/fC, " + tp + "\n ENC = %d $\pm$ %d"%(encmean, encstd))
#    #plt.plot((np.array(chnos)-128*1)[128*1:128*2], encs[128*1:128*2],  marker = 'o', color ="C%d"%i, label="LN, 14mV/fC(200 e-/bin)," + tp)
#    #encs_tp.append(encs[128*1:128*2])
##    plt.plot((np.array(chnos)-128*2)[128*2:128*3], peds[128*1:128*2],  marker = 'o', color ="C%d"%i, label="LN, 14mV/fC," + tp)
##    plt.plot((np.array(chnos)-128*1)[128*1:128*2], rt_enc,  marker = 's', color ="C3", label="RT, 14mV/fC(195 e-/bin), 1.0us")
#
#plt.title ("Noise Disctribution of FEMB (150pF Toy TPC)") 
#plt.xlabel("Channel Number")
#plt.ylabel("ENC \ e-")
#plt.xlim((-1, 70))
#plt.ylim((0, 1500))
#plt.grid()
#plt.legend()
##plt.show()
#plt.savefig(frst+ "pls_enc_dis.png")
#plt.close()


#fembloc = 1
#import pickle
#if (fembloc ==1):
#    with open("./APA_Capacitance_B2.bin", 'rb') as fn:
#        apa_cap = pickle.load(fn)
#    apa_cap[5] =  15
#    apa_cap[20] = 15
#    apa_cap[25] = 15
#    apa_cap[27] = 15
#    apa_cap[28] = 15
#    apa_cap[29] = 15
#    apa_cap[42] = 15
#    apa_cap[64] = 15
#    apa_cap[79] = 15
#    apa_cap[123] = 15
#
#    openchns = []
#    for i in range(len(apa_cap)):
#        if apa_cap[i] <=25:
#            openchns.append(i)
#
#xchns_r = [i for i in xchns if i not in openchns]
#uchns_r = [i for i in uchns if i not in openchns]
#vchns_r = [i for i in vchns if i not in openchns]
#
#encx_05 =[encs_tp[0][i] for i in xchns_r]
#encx_10 =[encs_tp[1][i] for i in xchns_r]
#encx_20 =[encs_tp[2][i] for i in xchns_r]
#encx_30 =[encs_tp[3][i] for i in xchns_r]
#encu_05 =[encs_tp[0][i] for i in uchns_r]
#encu_10 =[encs_tp[1][i] for i in uchns_r]
#encu_20 =[encs_tp[2][i] for i in uchns_r]
#encu_30 =[encs_tp[3][i] for i in uchns_r]
#encv_05 =[encs_tp[0][i] for i in vchns_r]
#encv_10 =[encs_tp[1][i] for i in vchns_r]
#encv_20 =[encs_tp[2][i] for i in vchns_r]
#encv_30 =[encs_tp[3][i] for i in vchns_r]
#enco_05 =[encs_tp[0][i] for i in openchns]
#enco_10 =[encs_tp[1][i] for i in openchns]
#enco_20 =[encs_tp[2][i] for i in openchns]
#enco_30 =[encs_tp[3][i] for i in openchns]
#
##print (np.mean(encx_05), np.mean(encx_10), np.mean(encx_20), np.mean(encx_30) )
##print (encx_30)
#encxtps_m = [np.mean(encx_05), np.mean(encx_10), np.mean(encx_20), np.mean(encx_30)]
#encxtps_s = [np.std (encx_05), np.std (encx_10), np.std (encx_20), np.std (encx_30)]
#encutps_m = [np.mean(encu_05), np.mean(encu_10), np.mean(encu_20), np.mean(encu_30)]
#encutps_s = [np.std (encu_05), np.std (encu_10), np.std (encu_20), np.std (encu_30)]
#encvtps_m = [np.mean(encv_05), np.mean(encv_10), np.mean(encv_20), np.mean(encv_30)]
#encvtps_s = [np.std (encv_05), np.std (encv_10), np.std (encv_20), np.std (encv_30)]
#encotps_m = [np.mean(enco_05), np.mean(enco_10), np.mean(enco_20), np.mean(enco_30)]
#encotps_s = [np.std (enco_05), np.std (enco_10), np.std (enco_20), np.std (enco_30)]
#
#
#import matplotlib.pyplot as plt
#fig = plt.figure(figsize=(12, 8))
#plt.rcParams.update({'font.size': 24})
#tps = [0.5, 1.0, 2.0, 3.0]
#plt.errorbar(tps, encxtps_m, encxtps_s, marker = 'o', color = 'g', label = "%d X wires"%(len(xchns_r) ))
#plt.errorbar(tps, encutps_m, encutps_s, marker = '>', color = 'r', label = "%d U wires"%(len(uchns_r)))
#plt.errorbar(tps, encvtps_m, encvtps_s, marker = 's', color = 'b', label = "%d V wires"%(len(vchns_r)))
#plt.errorbar(tps, encotps_m, encotps_s, marker = 'd', color = 'm', label = "%d Open CHs"%(len(openchns)))
#plt.text(0.2, 1000, "O:",  color = 'm', fontsize=18) 
#plt.text(0.5, 1000, int(encotps_m[0]), color = 'm', fontsize=18) 
#plt.text(1.0, 1000, int(encotps_m[1]), color = 'm', fontsize=18) 
#plt.text(2.0, 1000, int(encotps_m[2]), color = 'm', fontsize=18) 
#plt.text(3.0, 1000, int(encotps_m[3]), color = 'm', fontsize=18) 
#
#plt.text(0.2, 1300, "X:",  color = 'g', fontsize=18) 
#plt.text(0.5, 1300, int(encxtps_m[0]), color = 'g', fontsize=18) 
#plt.text(1.0, 1300, int(encxtps_m[1]), color = 'g', fontsize=18) 
#plt.text(2.0, 1300, int(encxtps_m[2]), color = 'g', fontsize=18) 
#plt.text(3.0, 1300, int(encxtps_m[3]), color = 'g', fontsize=18) 
#
#plt.text(0.2, 1200, "V:",  color = 'b', fontsize=18) 
#plt.text(0.5, 1200, int(encvtps_m[0]), color = 'b', fontsize=18) 
#plt.text(1.0, 1200, int(encvtps_m[1]), color = 'b', fontsize=18) 
#plt.text(2.0, 1200, int(encvtps_m[2]), color = 'b', fontsize=18) 
#plt.text(3.0, 1200, int(encvtps_m[3]), color = 'b', fontsize=18) 
#
#plt.text(0.2, 1100, "U:",  color = 'r', fontsize=18) 
#plt.text(0.5, 1100, int(encutps_m[0]), color = 'r', fontsize=18) 
#plt.text(1.0, 1100, int(encutps_m[1]), color = 'r', fontsize=18) 
#plt.text(2.0, 1100, int(encutps_m[2]), color = 'r', fontsize=18) 
#plt.text(3.0, 1100, int(encutps_m[3]), color = 'r', fontsize=18) 
#
#plt.ylim((0, 2000))
#plt.grid()
#plt.legend(loc=1, fontsize=18)
##plt.title("ENC Measurement ")
#plt.xlabel("Peak time / ($\mu$s)")
#plt.ylabel("ENC / (e-) ")
#plt.xlim((0,4))
#plt.show()
#plt.close()
##chnos = np.arange(128)
##for i in range(9):
##    plt.vlines(16*i, 0, 1500, linestyles="dashed", color='gray')
#
#
##
###peds = [] 
###rmss = []
##import matplotlib.pyplot as plt
##for fembi in fembs:
##    fig = plt.figure(figsize=(24, 18))
##    plt.rcParams.update({'font.size': 24})
##    for k in range(8):
##        x = 420 + k+1
##        plt.subplot(x)
##        for i in range(16):
##            key="CH{}".format(128*fembi + 16*k + i)
##            dlen = 500
##            x = np.arange(dlen)
##            y = f[key][0:dlen]
##            plt.plot(x,y, label=key, color = "C{}".format(k))
##    #        plt.draw()
##    #        plt.legend()
##    #        plt.pause(0.5)
##    plt.tight_layout()
###    plt.show()
##    plt.close()
###
##            peds.append(np.mean(tmp))
##            rmss.append(np.std(tmp))
##    
##    fig = plt.figure(figsize=(24, 18))
##    plt.rcParams.update({'font.size': 24})
##    plt.subplot(311)
##    plt.plot(np.arange(len(peds)), peds, marker = '.', color ='b', label = "Pedestal / bin")
##    plt.ylim((0,4100))
##    plt.ylabel("ADC counts")
##    plt.grid()
##    plt.legend()
##    plt.subplot(312)
##    plt.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
##    plt.ylabel("ADC counts")
##    plt.grid()
##    plt.legend()
##    plt.subplot(313)
##    plt.plot(np.arange(len(pks)), np.array(peds),marker = '.',  color ='b', label = "Pedestal / bin")
##    plt.plot(np.arange(len(pks)), np.array(pks),marker = '.',  color ='g', label = "Pulse peak / bin")
##    plt.ylim((0,4100))
##    plt.ylabel("ADC counts")
##    plt.grid()
##    plt.legend()
##    plt.xlabel("Channel number")
##    plt.show()
##    plt.close()
##
##print (peds)
##print (rmss)
##print (pks)
#
#
##for k in range(8):
##    x = 420 + k+1
##    plt.subplot(x)
##    for i in range(16):
##        key="CH{}".format(16*k + i)
##
##        dlen = 500
##        x = np.arange(dlen)
##        y = f[key][0:dlen]
##        plt.plot(x,y, label=key, color = "C{}".format(k))
###        plt.draw()
###        plt.legend()
###        plt.pause(0.5)
##plt.show()
##plt.close()
#
##
##chdata0=dset0[0000000:8010000]
##chdata1=dset1[0000000:80100000]
##chdata13=dset13[0000000:80100000]
##
##if False:
##    print ("Plots for 1 second data with trigger indicators")
##    fig = plt.figure(figsize=(24, 18))
##    plt.rcParams.update({'font.size': 32})
##    plt.subplot(311)
##    plt.plot(np.arange(len(chdata0[0:100000])), chdata0[0:100000], color ='b', label = "CH0")
##    plt.legend()
##    plt.subplot(312)
##    plt.plot(np.arange(len(chdata1[0:100000])), chdata1[0:100000], color ='r', label = "CH1(new SiPM)")
##    plt.legend()
##    plt.subplot(313)
##    plt.plot(np.arange(len(chdata13[0:100000])), chdata13[0:100000], color ='g', label = "CH13(old SiPM)")
##    plt.legend()
##    plt.show()
##    plt.close()
##
##print ("Histogram of T0 trigger")
##plt.rcParams.update({'font.size': 32})
##fig = plt.figure(figsize=(24, 18))
##triglocs = np.where((chdata1>>12) > 0)[0]
##trig_num = len(triglocs)
##if trig_num > 4002:
##    trig_num = 4002
##oft = 10000
##oft1 = -2
##oft2 = 4
##trig_num = np.arange(0,trig_num-2, 1)
##pslocs = []
##for i in trig_num:
##    swave = chdata1[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
##    tmp1 = np.max(swave)
##    tmp2 = np.min(swave)
##    pk = tmp1 - tmp2
##    if pk > 100:
##        psloc = np.where(swave==tmp1)[0][0]
##        pslocs.append([i, psloc, pk])
##
##trigseq, locs, pks = zip(*pslocs)
##loc = int(round(np.mean(locs)))
##print ("peak location of majority LED pulse responses is {}".format(loc))
##psvs = []
##for i in trig_num:
##    psvs.append(chdata1[triglocs[i] + oft +oft1 + loc])
##plt.hist(psvs, bins= 200, label="Total Pulse Count = {} \n Pedestal at ~{:d} ADC bins".format(len(trig_num), int(np.mean(chdata1[0:10000]))))
##plt.title("Histogram")
##plt.xlabel("ADC bins")
##plt.ylabel("Counts")
##plt.xlim((0, 4100))
##plt.legend()
##plt.grid()
##plt.show()
##plt.close()
##
##
##if True:
##    plt.rcParams.update({'font.size': 32})
##    fig = plt.figure(figsize=(24, 18))
##    ablocs = []
##    for x in pslocs:
##        if x[1] != loc:
##            ablocs.append(x)
##    oft1 = -10
##    oft2 = 90
##    for m in ablocs[:]:
##        i = m[0]
##        pltch0 = chdata0[triglocs[i]+oft  +oft1:triglocs[i] + oft+oft2]
##        pltch1 = chdata1[triglocs[i]+oft  +oft1:triglocs[i] + oft+oft2]
##        pltch13 = chdata13[triglocs[i]+oft+oft1:triglocs[i] + oft+oft2]
##        plt.subplot(311)
##        plt.plot(np.arange(len(pltch0)), pltch0, marker = '.')
##        plt.subplot(312)
##        plt.plot(np.arange(len(pltch1)), pltch1, marker='.')
##        plt.subplot(313)
##        plt.plot(np.arange(len(pltch13)), pltch13, marker = '.')
###        plt.draw()
###        plt.pause(1)
##
##    for x in pslocs:
##        if x[1] == loc:
##            i = x[0]
##            pltch0 = chdata0[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
##            pltch1 = chdata1[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
##            pltch13 = chdata13[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
##            plt.subplot(311)
##            plt.plot(np.arange(len(pltch0)), pltch0, marker='.', label="CH0")
##            plt.legend()
##
##            plt.subplot(312)
##            plt.plot(np.arange(len(pltch1)), pltch1, color='r', marker='s', label="CH1(new SiPM)")
##            plt.legend()
##
##            plt.subplot(313)
##            plt.plot(np.arange(len(pltch13)), pltch13, marker='.', label="CH13(Old SiPM)")
##            plt.legend()
##            break
##    plt.title("Waveforms with different peak location from 1st trigger are plotted")
##    plt.show()
##    plt.close()


