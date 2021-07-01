# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 2/10/2021 2:32:37 PM
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
#from matplotlib.backends.backend_pdf import PdfPages
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches
from detect_peaks import detect_peaks
fdir = "D:/CM_FEMB/APA_data/"

rt_fp = "Rawdata_12_29_2020_14_36_20_APA40_CHK_14_10_asicdac08_bl200.h5"
rt_f = h5py.File(fdir + rt_fp, 'r')
rt_keys = list(rt_f.keys())

ln_fp = "Rawdata_12_31_2020_07_40_48_APA40_slot0123on_CHK_LN_14_10_bl200_asicdac08.h5"
ln_fp = "Rawdata_12_31_2020_11_35_40_APA40_slot0123on_CHK_LN_14_10_bl200_asicdac08.h5"
ln_f = h5py.File(fdir + ln_fp, 'r')
ln_keys = list(ln_f.keys())

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(24, 18))
plt.rcParams.update({'font.size': 24})

keyss = [rt_keys, ln_keys]
fs = [rt_f, ln_f]

for i in range(2):
    keys = keyss[i]
    
    chnos = np.arange(512)
    peds =  [0]*512
    rmss =  [0]*512
    pks =  [0]*512
    dlen = 100000
    for key in keys:
        chno = int(key[2:])
        y = fs[i][key][0:dlen]

        plocs = detect_peaks(y, mph=None, mpd=100, threshold=100, edge='rising')
    
        xlen = plocs[1] - plocs[0] - 10
        avgm = 100
        tmp = []
        for m in range(avgm):
            if (m==0):
                ay=y[(plocs[1]-50):(plocs[1]+xlen-50)].astype('uint64')
                tmp = y[(plocs[1]+50):(plocs[1]+150)].astype('uint64')
            else:
                ay=ay + y[(plocs[1 + m]-50):(plocs[1+m]+xlen-50)].astype('uint64')
                tmp = np.append(tmp, y[(plocs[1+m]+50):(plocs[1+m]+150)].astype('uint64'))
        ay = ay/avgm
        x = np.arange(xlen)

        ped = np.mean(tmp)
        rms = np.std(tmp)
        chnos[chno] = chno
        peds[chno] = ped
        rmss[chno] = rms
        pks[chno] = np.max(ay)
    if i == 0:
        label = "RT"
    else:
        label = "LN"
    plt.subplot(211)
    plt.plot(chnos, rmss, marker = '.', color ="C{}".format(i), label=label)
    plt.subplot(212)
    plt.plot(chnos, np.array(pks)-np.array(peds), marker = '.', color ="C{}".format(i), label=label)

plt.grid()
plt.legend()
plt.show()
plt.close()

#
##peds = [] 
##rmss = []
#import matplotlib.pyplot as plt
#for fembi in fembs:
#    fig = plt.figure(figsize=(24, 18))
#    plt.rcParams.update({'font.size': 24})
#    for k in range(8):
#        x = 420 + k+1
#        plt.subplot(x)
#        for i in range(16):
#            key="CH{}".format(128*fembi + 16*k + i)
#            dlen = 500
#            x = np.arange(dlen)
#            y = f[key][0:dlen]
#            plt.plot(x,y, label=key, color = "C{}".format(k))
#    #        plt.draw()
#    #        plt.legend()
#    #        plt.pause(0.5)
#    plt.tight_layout()
##    plt.show()
#    plt.close()
##
#            peds.append(np.mean(tmp))
#            rmss.append(np.std(tmp))
#    
#    fig = plt.figure(figsize=(24, 18))
#    plt.rcParams.update({'font.size': 24})
#    plt.subplot(311)
#    plt.plot(np.arange(len(peds)), peds, marker = '.', color ='b', label = "Pedestal / bin")
#    plt.ylim((0,4100))
#    plt.ylabel("ADC counts")
#    plt.grid()
#    plt.legend()
#    plt.subplot(312)
#    plt.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
#    plt.ylabel("ADC counts")
#    plt.grid()
#    plt.legend()
#    plt.subplot(313)
#    plt.plot(np.arange(len(pks)), np.array(peds),marker = '.',  color ='b', label = "Pedestal / bin")
#    plt.plot(np.arange(len(pks)), np.array(pks),marker = '.',  color ='g', label = "Pulse peak / bin")
#    plt.ylim((0,4100))
#    plt.ylabel("ADC counts")
#    plt.grid()
#    plt.legend()
#    plt.xlabel("Channel number")
#    plt.show()
#    plt.close()
#
#print (peds)
#print (rmss)
#print (pks)


#for k in range(8):
#    x = 420 + k+1
#    plt.subplot(x)
#    for i in range(16):
#        key="CH{}".format(16*k + i)
#
#        dlen = 500
#        x = np.arange(dlen)
#        y = f[key][0:dlen]
#        plt.plot(x,y, label=key, color = "C{}".format(k))
##        plt.draw()
##        plt.legend()
##        plt.pause(0.5)
#plt.show()
#plt.close()

#
#chdata0=dset0[0000000:8010000]
#chdata1=dset1[0000000:80100000]
#chdata13=dset13[0000000:80100000]
#
#if False:
#    print ("Plots for 1 second data with trigger indicators")
#    fig = plt.figure(figsize=(24, 18))
#    plt.rcParams.update({'font.size': 32})
#    plt.subplot(311)
#    plt.plot(np.arange(len(chdata0[0:100000])), chdata0[0:100000], color ='b', label = "CH0")
#    plt.legend()
#    plt.subplot(312)
#    plt.plot(np.arange(len(chdata1[0:100000])), chdata1[0:100000], color ='r', label = "CH1(new SiPM)")
#    plt.legend()
#    plt.subplot(313)
#    plt.plot(np.arange(len(chdata13[0:100000])), chdata13[0:100000], color ='g', label = "CH13(old SiPM)")
#    plt.legend()
#    plt.show()
#    plt.close()
#
#print ("Histogram of T0 trigger")
#plt.rcParams.update({'font.size': 32})
#fig = plt.figure(figsize=(24, 18))
#triglocs = np.where((chdata1>>12) > 0)[0]
#trig_num = len(triglocs)
#if trig_num > 4002:
#    trig_num = 4002
#oft = 10000        ax1 = fig.add_subplot(111)
        menc = np.mean(encs)
        senc = np.std(encs)
        ax1_1 = ax1.twinx()
        ax1_1.scatter(chnnos, apa_cap, color = 'g', maRawdata_01_26_2021_10_58_26_CEbox_7_16_CM03_AM06.h5rker = '.', label = "APA wire capacitance" )
#oft1 = -2
#oft2 = 4
#trig_num = np.arange(0,trig_num-2, 1)
#pslocs = []
#for i in trig_num:
#    swave = chdata1[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
#    tmp1 = np.max(swave)
#    tmp2 = np.min(swave)
#    pk = tmp1 - tmp2
#    if pk > 100:
#        psloc = np.where(swave==tmp1)[0][0]
#        pslocs.append([i, psloc, pk])
#
#trigseq, locs, pks = zip(*pslocs)
#loc = int(round(np.mean(locs)))
#print ("peak location of majority LED pulse responses is {}".format(loc))
#psvs = []
#for i in trig_num:
#    psvs.append(chdata1[triglocs[i] + oft +oft1 + loc])
#plt.hist(psvs, bins= 200, label="Total Pulse Count = {} \n Pedestal at ~{:d} ADC bins".format(len(trig_num), int(np.mean(chdata1[0:10000]))))
#plt.title("Histogram")
#plt.xlabel("ADC bins")
#plt.ylabel("Counts")
#plt.xlim((0, 4100))
#plt.legend()
#plt.grid()
#plt.show()
#plt.close()
#
#
#if True:
#    plt.rcParams.update({'font.size': 32})
#    fig = plt.figure(figsize=(24, 18))
#    ablocs = []
#    for x in pslocs:
#        if x[1] != loc:
#            ablocs.append(x)
#    oft1 = -10
#    oft2 = 90
#    for m in ablocs[:]:
#        i = m[0]
#        pltch0 = chdata0[triglocs[i]+oft  +oft1:triglocs[i] + oft+oft2]
#        pltch1 = chdata1[triglocs[i]+oft  +oft1:triglocs[i] + oft+oft2]
#        pltch13 = chdata13[triglocs[i]+oft+oft1:triglocs[i] + oft+oft2]
#        plt.subplot(311)
#        plt.plot(np.arange(len(pltch0)), pltch0, marker = '.')
#        plt.subplot(312)
#        plt.plot(np.arange(len(pltch1)), pltch1, marker='.')
#        plt.subplot(313)
#        plt.plot(np.arange(len(pltch13)), pltch13, marker = '.')
##        plt.draw()
##        plt.pause(1)
#
#    for x in pslocs:
#        if x[1] == loc:
#            i = x[0]
#            pltch0 = chdata0[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
#            pltch1 = chdata1[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
#            pltch13 = chdata13[triglocs[i] + oft + oft1:triglocs[i] + oft + oft2]
#            plt.subplot(311)
#            plt.plot(np.arange(len(pltch0)), pltch0, marker='.', label="CH0")
#            plt.legend()
#
#            plt.subplot(312)
#            plt.plot(np.arange(len(pltch1)), pltch1, color='r', marker='s', label="CH1(new SiPM)")
#            plt.legend()
#
#            plt.subplot(313)
#            plt.plot(np.arange(len(pltch13)), pltch13, marker='.', label="CH13(Old SiPM)")
#            plt.legend()
#            break
#    plt.title("Waveforms with different peak location from 1st trigger are plotted")
#    plt.show()
#    plt.close()


