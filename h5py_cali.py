# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 2/4/2021 7:22:20 AM
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
fdir = "D:/CM_FEMB/APA_data/"
#fdir = "D:/CM_FEMB/Rawdata/"
#fdir = "D:/CM_FEMB/CEbox/"
#fdir = "D:/CM_FEMB/Rawdata/"
fdir = "D:/CM_FEMB/APA_data_run1/"
#fdir = "D:/CM_FEMB/Rawdata/"
fdir = "D:/CM_FEMB/Rawdata/"
fp = "CALI_RT_CM12_AM10_NoToyTPC_0pF_14_20_bl200_bufoff_asicdac04.h5"

f = h5py.File(fdir + fp, 'r')
keys = list(f.keys())
fembs=[0]
#fembs=[0,2,3]
import matplotlib.pyplot as plt

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
#    plt.tight_layout()
#    plt.show()
#    plt.close()
#
for fembi in fembs:
    fig = plt.figure(figsize=(16, 12))
    plt.rcParams.update({'font.size': 18})
    from detect_peaks import detect_peaks
    dlen = 100000
    rmss = []
    pks = []
    peds = []
    ymax = []
    for k in range(8):
        x = 420 + k+1
        plt.subplot(x)
        for i in range(16):
            key="CH{}".format(fembi*128 + 16*k + i)
            y = f[key][0:dlen]
            plocs = detect_peaks(y, mph=None, mpd=100, threshold=10, edge='rising')
            print (plocs)
    
            xlen = plocs[2] - plocs[1] - 10
            avgm = 100
            tmp = []
            for m in range(avgm):
                if (m==0):
                    ay=y[(plocs[1]-50):(plocs[1]+xlen-50)].astype('uint64')
                    tmp = y[(plocs[1]+50):(plocs[1]+150)].astype('uint64')
                else:
                    ay=ay + y[(plocs[1 + m]-50):(plocs[1+m]+xlen-50)].astype('uint64')
                    tmp = np.append(tmp, y[(plocs[1+m]+50):(plocs[1+m]+150)].astype('uint64'))
            peds.append(np.mean(tmp))
            rmss.append(np.std(tmp))
            ay = (ay/avgm) - np.mean(tmp)
            ymax.append(np.max(ay))
            pks.append(np.max(ay))
            x = np.arange(xlen)
            plt.plot(x[0:100],ay[0:100], label=key, color = "C{}".format(k))
    print (np.mean(ymax), np.std(ymax))
    plt.tight_layout()
    plt.show()
    plt.close()
    
    fig = plt.figure(figsize=(16, 12))
    plt.rcParams.update({'font.size': 18})
#    plt.subplot(311)
#    plt.plot(np.arange(len(peds)), peds, marker = '.', color ='b', label = "Pedestal / bin")
#    plt.ylim((0,4100))
#    plt.ylabel("ADC counts")
#    plt.grid()
#    plt.legend()
#    plt.subplot(312)
    import pickle
    fsp =fdir + fp[0:-3] + "_sts.bin" 
    with open(fsp, 'wb') as fn:
        pickle.dump([peds, rmss, ymax], fn)


#    if (fembi ==3):
#        import pickle
#        import copy
#        with open("./APA_Capacitance_B4.bin", 'rb') as fn:
#            apa_cap = pickle.load(fn)
#
#        apa_cap[2] = 20
##        apa_cap[35] = 20
#        apa_cap[42] = 20
#        #apa_cap[42] = 20
#        #apa_cap[48] = 20
#        apa_cap[51] = 20
#        apa_cap[52] = 20
#        apa_cap[54] = 20
#        apa_cap[56] = 20
#        apa_cap[58] = 20
#        apa_cap[60] = 20
#        apa_cap[65] = 20
#        apa_cap[83] = 20
#        apa_cap[88] = 20
#        #apa_cap[104] = 20
#        #apa_cap[105] = 20
#        #apa_cap[118] = 20
#        B4_with_cap = copy.deepcopy(apa_cap)
#
#        B4_with_cap[1] =  B4_with_cap[1]  + 22
#        B4_with_cap[15] =  B4_with_cap[15]  + 22
#        B4_with_cap[16+1] =  B4_with_cap[16+1]  + 22
#        B4_with_cap[16+14] =  B4_with_cap[16+14]  + 22
#        B4_with_cap[16*4+1] =  B4_with_cap[16*4+1]  + 47
#        B4_with_cap[16*4+14] =  B4_with_cap[16*4+14]  + 47
#        B4_with_cap[16*4+7] =  B4_with_cap[16*4+7]  + 82
#        B4_with_cap[16*4+11] =  B4_with_cap[16*4+11]  + 82
#        B4_with_cap[7] =  B4_with_cap[7]  + 100 
#        B4_with_cap[16+8] =  B4_with_cap[16+8]  + 100
#        B4_with_cap[16*5+1] =  B4_with_cap[16*5+1]  + 100
#        B4_with_cap[16*5+14] =  B4_with_cap[16*5+14]  + 100
#        B4_with_cap[4] =  B4_with_cap[4]  + 150 
#        B4_with_cap[16+11] =  B4_with_cap[16+11]  + 150
#        B4_with_cap[16*5+3] =  B4_with_cap[16*5+3]  + 150
#        B4_with_cap[16*5+8] =  B4_with_cap[16*5+8]  + 150
#
##        B4_with_cap[16+15] =  B4_with_cap[16+15]  + 120  #31bad channel
#        B4_with_cap[16*2+4] =  B4_with_cap[16*2+4]  + 150 
#        B4_with_cap[16*2+6] =  B4_with_cap[16*2+6]  +  120
##        B4_with_cap[16*3+1] =  B4_with_cap[16*3+1]  +  120 #49 bad channel
#        B4_with_cap[16*3+2] =  B4_with_cap[16*3+2]  +  120
#        B4_with_cap[16*3+5] =  B4_with_cap[16*3+5]  +  120
#        B4_with_cap[16*3+11] =  B4_with_cap[16*3+11]  + 150 
#        B4_with_cap[16*6+12] =  B4_with_cap[16*6+12]  + 150 
#        B4_with_cap[16*6+15] =  B4_with_cap[16*6+15]  + 150 
#        B4_with_cap[16*7+3] =  B4_with_cap[16*7+3]  +  150
#        B4_with_cap[16*7+9] =  B4_with_cap[16*7+9]  +  120
##        B4_with_cap[16*7+13] =  B4_with_cap[16*7+13]  +  82 #125 bad channel
#
##        B4_with_cap[16+15] =  B4_with_cap[16+15]  + 120 
##        B4_with_cap[16*2+4] =  B4_with_cap[16*2+4]  + 120 
##        B4_with_cap[16*2+6] =  B4_with_cap[16*2+6]  +  120
##        B4_with_cap[16*3+1] =  B4_with_cap[16*3+1]  + 82 
##        B4_with_cap[16*3+2] =  B4_with_cap[16*3+2]  + 82 
##        B4_with_cap[16*3+5] =  B4_with_cap[16*3+5]  +  120
##        B4_with_cap[16*3+11] =  B4_with_cap[16*3+11]  + 120 
##        B4_with_cap[16*6+12] =  B4_with_cap[16*6+12]  + 120 
##        B4_with_cap[16*6+15] =  B4_with_cap[16*6+15]  + 82 
##        B4_with_cap[16*7+3] =  B4_with_cap[16*7+3]  +  120
##        B4_with_cap[16*7+9] =  B4_with_cap[16*7+9]  +  120
##        B4_with_cap[16*7+13] =  B4_with_cap[16*7+13]  +  82
#
#        chnnos_extra_cap = [1, 15, 16+1, 16+14, 16*4+1, 16*4+14, 16*4+7, \
#                            16*4+11, 7, 16+8, 16*5+1, 16*5+14, 4, 16+11, 16*5+3, 16*5+8,\
#                            16+15, 16*2+4, 16*2+6, 16*3+1, 16*3+5, 16*3+11,\
#                            16*6+12, 16*6+15, 16*7+3, 16*7+9, 16*7+13,
#                            ]
#        chnnos_no_cap = []
#        for chnno in range(len(B4_with_cap)):
#            if chnno not in chnnos_extra_cap:
#                chnnos_no_cap.append(chnno)
#
##    x_c = [1,15,17, 30, 65, 78, 71, 75, 24, 7, 81, 94, 4, 27, 83, 88]
##    y_c = np.array([22, 22, 22, 22, 47, 47, 82, 82, 100, 100, 100, 100, 150, 150, 150, 150]) * 0.02
#    ax1 = fig.add_subplot(111)
#    ax1.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
#    import pickle
#    fsp =fdir + "femb_%dRT_rms.bin"%fembi
#    with open(fsp, 'wb') as fn:
#        pickle.dump(rmss, fn)
#
#
#    ax1.set_ylim((0,10))
#
#    if (fembi ==3):
#        ax1_1 = ax1.twinx()
#        chnnos = np.arange(128)
#        ax1_1.scatter(chnnos, B4_with_cap, color = 'g', marker = '.', label = "Capacitance / pF" )
#        
#
##    plt.ylabel("ADC counts")
##    plt.legend()
##    plt.subplot(313)
##    plt.plot(np.arange(len(pks)), np.array(peds),marker = '.',  color ='b', label = "Pedestal / bin")
##    plt.plot(np.arange(len(pks)), np.array(pks),marker = '.',  color ='g', label = "Pulse peak / bin")
##    plt.ylim((0,4100))
##    plt.ylabel("ADC counts")
##    plt.grid()
##    plt.legend()
#    plt.xlabel("Channel number")
#    plt.grid(axis='both')
#    plt.tight_layout()
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


