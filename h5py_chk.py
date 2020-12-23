# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 12/23/2020 3:28:05 PM
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

fdir = "D:/CM_FEMB/Rawdata/"
#fp = "CHK_LN_CM04_AM01_Toy04L21R_150pF_14_10_bl200_bufoff_asicdac08_150pF.h5"
fp = "_CHK_LN_CM05_AM08_Toy04L21R_150pF_14_10_bl200_bufoff_asicdac08_150pF.h5"
f = h5py.File(fdir + fp, 'r')
keys = list(f.keys())
print(keys)
#dset0 = f["CH0"]
#dset1 = f["CH1"]
#dset13 = f["CH13"]
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(24, 18))
plt.rcParams.update({'font.size': 32})

for k in range(8):
    x = 420 + k+1
    plt.subplot(x)
    for i in range(16):
        key="CH{}".format(16*k + i)
        dlen = 500
        x = np.arange(dlen)
        y = f[key][0:dlen]
        plt.plot(x,y, label=key, color = "C{}".format(k))
#        plt.draw()
#        plt.legend()
#        plt.pause(0.5)
plt.show()
plt.close()
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
#oft = 10000
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


