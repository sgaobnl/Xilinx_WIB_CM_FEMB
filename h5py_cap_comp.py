# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 2/7/2021 10:39:53 AM
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
from apa_mapping import APA_MAP 
#from matplotlib.backends.backend_pdf import PdfPages
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches
apa40 = APA_MAP()
xchns = apa40.apa_mapping()[1]
uchns = apa40.apa_mapping()[2]
vchns = apa40.apa_mapping()[3]
#print (len(xchns))
#print (len(uchns))
#print (len(vchns))
#exit()

fembloc = 3
fdir = "D:/CM_FEMB/APA_data/"
#fp = "Rawdata_01_15_2021_13_59_09_APA40_LN_CHK_slot0123on_14_10_bl200_ascidac08_sts.bin"
fp = "Rawdata_01_15_2021_13_59_09_APA40_LN_CHK_slot0123on_14_10_bl200_ascidac08_sts_femb2.bin"
fp = "Rawdata_01_15_2021_13_59_09_APA40_LN_CHK_slot0123on_14_10_bl200_ascidac08_sts_femb3.bin"
import pickle
import copy
fsp =fdir + fp
with open(fsp, 'rb') as fn:
    femb_200 = pickle.load(fn)

#fp = "Rawdata_01_15_2021_13_55_05_APA40_LN_CHK_slot0123on_14_10_bl900_ascidac08_sts.bin"
fp = "Rawdata_01_15_2021_13_55_05_APA40_LN_CHK_slot0123on_14_10_bl900_ascidac08_sts_femb2.bin"
fp = "Rawdata_01_15_2021_13_55_05_APA40_LN_CHK_slot0123on_14_10_bl900_ascidac08_sts_femb3.bin"
fsp =fdir + fp
with open(fsp, 'rb') as fn:
    femb_900 = pickle.load(fn)

#fp = "RT_sts.bin"
#fp = "RT_sts_femb2.bin"
fp = "RT_sts_femb3.bin"
fsp =fdir + fp
with open(fsp, 'rb') as fn:
    femb_rt = pickle.load(fn)


if (fembloc ==1):
    with open("./APA_Capacitance_B2.bin", 'rb') as fn:
        apa_cap = pickle.load(fn)
    apa_cap[5] =  15
    apa_cap[20] = 15
    apa_cap[25] = 15
    apa_cap[27] = 15
    apa_cap[28] = 15
    apa_cap[29] = 15
    apa_cap[42] = 15
    apa_cap[64] = 15
    apa_cap[79] = 15
    apa_cap[123] = 15

    openchns = []
    for i in range(len(apa_cap)):
        if apa_cap[i] <=25:
            openchns.append(i)

elif (fembloc ==2):
    with open("./APA_Capacitance_B3.bin", 'rb') as fn:
        apa_cap = pickle.load(fn)
    apa_cap[3] = 15
    apa_cap[67] = 15
    apa_cap[83] = 15
    apa_cap[85] = 15
    apa_cap[110] = 15
    openchns = []
    for i in range(len(apa_cap)):
        if apa_cap[i] <=25:
            openchns.append(i)

elif (fembloc ==3):
    with open("./APA_Capacitance_B4.bin", 'rb') as fn:
        apa_cap = pickle.load(fn)

    apa_cap[2] = 15 
    # apa_cap[35] = 20
    apa_cap[42] = 15 
    #apa_cap[42] = 20
    #apa_cap[48] = 20
    apa_cap[51] = 15
    apa_cap[52] = 15
    apa_cap[54] = 15
    apa_cap[56] = 15
    apa_cap[58] = 15
    apa_cap[60] = 15
    apa_cap[65] = 15
    apa_cap[83] = 15
    apa_cap[88] = 15
    #apa_cap[104] = 20
    #apa_cap[105] = 20
    #apa_cap[118] = 20
    B4_with_cap = copy.deepcopy(apa_cap)

    B4_with_cap[1] =  B4_with_cap[1]  + 22
    B4_with_cap[15] =  B4_with_cap[15]  + 22
    B4_with_cap[16+1] =  B4_with_cap[16+1]  + 22
    B4_with_cap[16+14] =  B4_with_cap[16+14]  + 22
    B4_with_cap[16*4+1] =  B4_with_cap[16*4+1]  + 47
    B4_with_cap[16*4+14] =  B4_with_cap[16*4+14]  + 47
    B4_with_cap[16*4+7] =  B4_with_cap[16*4+7]  + 82
    B4_with_cap[16*4+11] =  B4_with_cap[16*4+11]  + 82
    B4_with_cap[7] =  B4_with_cap[7]  + 100 
    B4_with_cap[16+8] =  B4_with_cap[16+8]  + 100
    B4_with_cap[16*5+1] =  B4_with_cap[16*5+1]  + 100
    B4_with_cap[16*5+14] =  B4_with_cap[16*5+14]  + 100
    B4_with_cap[4] =  B4_with_cap[4]  + 150 
    B4_with_cap[16+11] =  B4_with_cap[16+11]  + 150
    B4_with_cap[16*5+3] =  B4_with_cap[16*5+3]  + 150
    B4_with_cap[16*5+8] =  B4_with_cap[16*5+8]  + 150

    # B4_with_cap[16+15] =  B4_with_cap[16+15]  + 120  #31bad channel
    B4_with_cap[16*2+4] =  B4_with_cap[16*2+4]  + 150 
    B4_with_cap[16*2+6] =  B4_with_cap[16*2+6]  +  120
    # B4_with_cap[16*3+1] =  B4_with_cap[16*3+1]  +  120 #49 bad channel
    B4_with_cap[16*3+2] =  B4_with_cap[16*3+2]  +  120
    B4_with_cap[16*3+5] =  B4_with_cap[16*3+5]  +  120
    B4_with_cap[16*3+11] =  B4_with_cap[16*3+11]  + 150 
    B4_with_cap[16*6+12] =  B4_with_cap[16*6+12]  + 150 
    B4_with_cap[16*6+15] =  B4_with_cap[16*6+15]  + 150 
    B4_with_cap[16*7+3] =  B4_with_cap[16*7+3]  +  150
    B4_with_cap[16*7+9] =  B4_with_cap[16*7+9]  +  120
    # B4_with_cap[16*7+13] =  B4_with_cap[16*7+13]  +  82 #125 bad channel
    apa_cap = B4_with_cap

    chnnos_extra_cap = [1, 15, 16+1, 16+14, 16*4+1, 16*4+14, 16*4+7, \
                        16*4+11, 7, 16+8, 16*5+1, 16*5+14, 4, 16+11, 16*5+3, 16*5+8,\
                        16*2+4, 16*2+6, 16*3+5, 16*3+11,\
                        16*6+12, 16*6+15, 16*7+3, 16*7+9, 
                        ]
    chnnos_no_cap = []
    #for chnno in range(len(B4_with_cap)):
    for chnno in range(len(apa_cap)):
        if chnno not in chnnos_extra_cap:
            chnnos_no_cap.append(chnno)

    openchns = []
    for i in range(len(apa_cap)):
        if apa_cap[i] <=25:
            openchns.append(i)

#


#import matplotlib.pyplot as plt
#fig = plt.figure(figsize=(16, 12))
#plt.rcParams.update({'font.size': 24})
#chnos = np.arange(128)
##plt.plot(chnos, femb_200[0], marker='o', color='C2', label="LN2, 200mV BL")
##plt.plot(chnos, femb_200[2], marker='o', color='C2', label="LN2, 200mV BL + Pulser")
##plt.plot(chnos, femb_900[0], marker='s', color='C3', label="LN2, 900mV BL")
##plt.plot(chnos, femb_900[2], marker='s', color='C3', label="LN2, 900mV BL + Pulser")
##plt.plot(chnos, femb_rt[0], marker='^', color='C4', label="RT, 200mV BL")
##plt.plot(chnos, femb_rt[2], marker='^', color='C4', label="RT, 200mV BL + Pulser")
#plt.title ("Pulse Response Distribution of FEMB#1 on 40% APA") 
#plt.xlabel("Channel Number")
#plt.ylabel("ADC amplitude \ bin")
##plt.ylabel("ENC \ e-")
#plt.xlim((-1, 129))
#plt.ylim((0, 4100))
#plt.grid()
#plt.legend()
#plt.show()
#plt.close()

xchns_r = [i for i in xchns if i not in openchns]
uchns_r = [i for i in uchns if i not in openchns]
vchns_r = [i for i in vchns if i not in openchns]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})
chnos = np.arange(128)
for i in range(9):
    plt.vlines(16*i, 0, 1500, linestyles="dashed", color='gray')

ax1 = fig.add_subplot(111)
#ln200 = np.array(femb_200[1])*200
#ln200x =[ln200[i] for i in xchns_r]
#ln200u =[ln200[i] for i in uchns_r]
#ln200v =[ln200[i] for i in vchns_r]
#lnopen =[ln200[i] for i in openchns]
#ax1.plot(xchns_r, ln200x, marker = 'o', color ='r', label = "X, 200mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(ln200x), np.std(ln200x)))
#ax1.plot(uchns_r, ln200u, marker = '>', color ='b', label = "U, 200mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(ln200u), np.std(ln200u)))
#ax1.plot(vchns_r, ln200v, marker = 's', color ='m', label = "V, 200mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(ln200v), np.std(ln200v)))
#ax1.plot(openchns, lnopen, marker = 'd', color ='g', label = "OPEN, 200mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(lnopen), np.std(lnopen)))

ln900 = np.array(femb_900[1])*200
ax1.plot(chnos, ln900, marker = 'o', color ='b', label = "LN2, ENC")
#ln900x =[ln900[i] for i in xchns_r]
#ln900u =[ln900[i] for i in uchns_r]
#ln900v =[ln900[i] for i in vchns_r]
#lnopen =[ln900[i] for i in openchns]
#ax1.plot(xchns_r, ln900x, marker = 'o', color ='b', label = "X, 900mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(ln900x), np.std(ln900x)))
#ax1.plot(uchns_r, ln900u, marker = '>', color ='b', label = "U, 900mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(ln900u), np.std(ln900u)))
#ax1.plot(vchns_r, ln900v, marker = 's', color ='b', label = "V, 900mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(ln900v), np.std(ln900v)))
#ax1.plot(openchns, lnopen, marker = 'd', color ='b', label = "OPEN, 900mV BL, LN2, ENC = (%d +/- %d) e-"%(np.mean(lnopen), np.std(lnopen)))
#ln_rt = np.array(femb_rt[1])*200
#ln_rtx =[ln_rt[i] for i in xchns_r]
#ln_rtu =[ln_rt[i] for i in uchns_r]
#ln_rtv =[ln_rt[i] for i in vchns_r]
#lnopen =[ln_rt[i] for i in openchns]
#ax1.plot(xchns_r, ln_rtx, marker = 'o', color ='g', label = "X, RT, ENC = (%d +/- %d) e-"%(np.mean(ln_rtx), np.std(ln_rtx)))
#ax1.plot(uchns_r, ln_rtu, marker = '>', color ='g', label = "U, RT, ENC = (%d +/- %d) e-"%(np.mean(ln_rtu), np.std(ln_rtu)))
#ax1.plot(vchns_r, ln_rtv, marker = 's', color ='g', label = "V, RT, ENC = (%d +/- %d) e-"%(np.mean(ln_rtv), np.std(ln_rtv)))
#ax1.plot(openchns, lnopen, marker = 'd', color ='g', label = "OPEN, RT, ENC = (%d +/- %d) e-"%(np.mean(lnopen), np.std(lnopen)))

#plt.legend(loc=1)

#Cd_xchns_r=[apa_cap[i] for i in xchns_r]
#Cd_uchns_r=[apa_cap[i] for i in uchns_r]
#Cd_vchns_r=[apa_cap[i] for i in vchns_r]
#Cd_opens=[apa_cap[i] for i in openchns]
#
#ax1.scatter(xchns_r, Cd_xchns_r, color = 'r', marker = 'x', label = "X, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_xchns_r), np.std(Cd_xchns_r)) )
#ax1.scatter(uchns_r, Cd_uchns_r, color = 'b', marker = '*', label = "U, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_uchns_r), np.std(Cd_uchns_r)) )
#ax1.scatter(vchns_r, Cd_vchns_r, color = 'm', marker = '+', label = "V, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_vchns_r), np.std(Cd_vchns_r)) )
#ax1.scatter(openchns, Cd_opens, color = 'g', marker = '<', label = "OPEN, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_opens), np.std(Cd_opens)) )

#ax1.plot(chnos, np.array(femb_900[1])*200, marker = '>', color ='b', label = "LN2, 900mV BL")
#ax1.plot(chnos, np.array(femb_rt[1])*195, marker = 's', color ='g', label = "RT, 200mV BL")
#ax1.set_ylim((0,150))
ax1.set_ylim((0,1500))
ax1.set_xlabel("Channel Number")
#ax1.set_ylabel("Detector Capacitance / pF")
plt.legend(loc=1, fontsize=14)
ax1.set_ylabel("ENC / e-")

ax1_1 = ax1.twinx()
#Cd_xchns=[apa_cap[i] for i in xchns]
#Cd_uchns=[apa_cap[i] for i in uchns]
#Cd_vchns=[apa_cap[i] for i in vchns]
#
#Cd_xchns_r=[apa_cap[i] for i in xchns_r]
#Cd_uchns_r=[apa_cap[i] for i in uchns_r]
#Cd_vchns_r=[apa_cap[i] for i in vchns_r]
#Cd_opens=[apa_cap[i] for i in openchns]
#
#ax1_1.scatter(xchns_r, Cd_xchns_r, color = 'r', marker = 'x', label = "X, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_xchns_r), np.std(Cd_xchns_r)) )
#ax1_1.scatter(uchns_r, Cd_uchns_r, color = 'b', marker = '*', label = "U, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_uchns_r), np.std(Cd_uchns_r)) )
#ax1_1.scatter(vchns_r, Cd_vchns_r, color = 'm', marker = '+', label = "V, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_vchns_r), np.std(Cd_vchns_r)) )
#ax1_1.scatter(openchns, Cd_opens, color = 'g', marker = '<', label = "OPEN, Cd = (%d +/- %.1f) pF"%(np.mean(Cd_opens), np.std(Cd_opens)) )

ax1_1.scatter(chnos, apa_cap, color = 'm', marker = 'x', label = "Cd" )
#ax1_1.scatter(xchns, Cd_xchns, color = 'r', marker = 'x', label = "X" )
#ax1_1.scatter(uchns, Cd_uchns, color = 'b', marker = '*', label = "U" )
#ax1_1.scatter(vchns, Cd_vchns, color = 'm', marker = '+', label = "V" )
ax1_1.set_ylim((0,250))
ax1_1.set_ylabel("Detector Capacitance / pF")
plt.legend(loc=2, fontsize=14)
    


#plt.plot(chnos, femb_200[0], marker='o', color='C2', label="LN2, 200mV BL")
#plt.plot(chnos, femb_200[2], marker='o', color='C2', label="LN2, 200mV BL + Pulser")
#plt.plot(chnos, femb_900[0], marker='s', color='C3', label="LN2, 900mV BL")
#plt.plot(chnos, femb_900[2], marker='s', color='C3', label="LN2, 900mV BL + Pulser")
#plt.plot(chnos, femb_rt[0], marker='^', color='C4', label="RT, 200mV BL")
#plt.plot(chnos, femb_rt[2], marker='^', color='C4', label="RT, 200mV BL + Pulser")
#plt.title ("Noise Performance of FEMB#1 on 40% APA") 
plt.xlim((-1, 129))
#plt.ylim((0, 4100))
plt.grid(axis = 'y')
plt.show()
plt.close()


import statsmodels.api as sm   
B4_with_cap = np.array(apa_cap)
cresults_200 = sm.OLS(np.array(femb_200[1])*200,sm.add_constant(B4_with_cap)).fit()
cresults_rt = sm.OLS(np.array(femb_rt[1])*195,sm.add_constant(B4_with_cap)).fit()
cconstant_200 = cresults_200.params[0]
cslope_200 = cresults_200.params[1]
fit_200 = cslope_200 * B4_with_cap + cconstant_200 

cresults_900 = sm.OLS(np.array(femb_900[1])*200,sm.add_constant(B4_with_cap)).fit()
cslope_900 = cresults_900.params[1]
cconstant_900 = cresults_900.params[0]
fit_900 = cslope_900 * B4_with_cap + cconstant_900 

cresults_rt = sm.OLS(np.array(femb_rt[1])*195,sm.add_constant(B4_with_cap)).fit()
cslope_rt = cresults_rt.params[1]
cconstant_rt = cresults_rt.params[0]
fit_rt = cslope_rt * B4_with_cap + cconstant_rt 

#print (cslope)

fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})
plt.plot(B4_with_cap, fit_200, color = 'r', label = "Fitting: Y = %.3f*X + %d"%(cslope_200, cconstant_200) )
plt.plot(B4_with_cap, fit_900, color = 'b', label = "Fitting: Y = %.3f*X + %d"%(cslope_900, cconstant_900) )
plt.plot(B4_with_cap, fit_rt,  color = 'g', label = "Fitting: Y = %.3f*X + %d"%(cslope_rt, cconstant_rt ) )
plt.scatter(B4_with_cap,np.array(femb_200[1])*200, color = 'r', marker ='o', label="LN2, 200mV BL")
plt.scatter(B4_with_cap,np.array(femb_900[1])*200, color = 'b', marker ='^', label="LN2, 900mV BL")
plt.scatter(B4_with_cap,np.array(femb_rt[1])*195 , color = 'g', marker ='s', label="RT, 200mV BL" )
plt.title ("Noise Projection") 
plt.ylabel("ENC / e-")
plt.xlabel("Input Capacitance / pF")
plt.legend()
plt.grid()
plt.show()
plt.close()
#encs = np.array(rmss)*200
#rt_enc = np.array(rt_rmss)*195
#plt.plot((np.array(chnos)-128*2)[128*2:128*3], encs[128*2:128*3],  marker = 'o', color ="C2", label="LN, 14mV/fC(200 e-/bin), 1.0us ")
#plt.plot((np.array(chnos)-128*2)[128*2:128*3], rt_enc,  marker = 's', color ="C3", label="RT, 14mV/fC(195 e-/bin), 1.0us")
#
#plt.title ("Noise Disctribution of FEMB#2 on 40% APA") 
#plt.xlabel("Channel Number")
#plt.ylabel("ENC \ e-")
##plt.xlim((128*1, 128*2))
#plt.xlim((-1, 129))
#plt.ylim((0, 1200))
#plt.grid()
#plt.legend()
#plt.show()
#plt.close()
#
#
#
##    ax1.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
##    import pickle
##    fsp =fdir + "femb_%dRT_rms.bin"%fembi
##    with open(fsp, 'wb') as fn:
##        pickle.dump(rmss, fn)
#
#
##
#for fembi in fembs:
#    fig = plt.figure(figsize=(16, 12))
#    plt.rcParams.update({'font.size': 18})
#    from detect_peaks import detect_peaks
#    dlen = 100000
#    rmss = []
#    pks = []
#    peds = []
#    ymax = []
#    for k in range(8):
#        x = 420 + k+1
#        plt.subplot(x)
#        for i in range(16):
#            key="CH{}".format(fembi*128 + 16*k + i)
#            y = f[key][0:dlen]
#            plocs = detect_peaks(y, mph=None, mpd=100, threshold=10, edge='rising')
#            print (plocs)
#    
#            xlen = plocs[2] - plocs[1] - 10
#            avgm = 100
#            tmp = []
#            for m in range(avgm):
#                if (m==0):
#                    ay=y[(plocs[1]-50):(plocs[1]+xlen-50)].astype('uint64')
#                    tmp = y[(plocs[1]+50):(plocs[1]+150)].astype('uint64')
#                else:
#                    ay=ay + y[(plocs[1 + m]-50):(plocs[1+m]+xlen-50)].astype('uint64')
#                    tmp = np.append(tmp, y[(plocs[1+m]+50):(plocs[1+m]+150)].astype('uint64'))
#            peds.append(np.mean(tmp))
#            rmss.append(np.std(tmp))
#            ay = (ay/avgm) - np.mean(tmp)
#            ymax.append(np.max(ay))
#            pks.append(np.max(ay))
#            x = np.arange(xlen)
#            plt.plot(x[0:100],ay[0:100], label=key, color = "C{}".format(k))
#    print (np.mean(ymax), np.std(ymax))
#    plt.tight_layout()
#    plt.show()
#    plt.close()
#    
#    fig = plt.figure(figsize=(16, 12))
#    plt.rcParams.update({'font.size': 18})
##    plt.subplot(311)
##    plt.plot(np.arange(len(peds)), peds, marker = '.', color ='b', label = "Pedestal / bin")
##    plt.ylim((0,4100))
##    plt.ylabel("ADC counts")
##    plt.grid()
##    plt.legend()
##    plt.subplot(312)
#    import pickle
#    fsp =fdir + fp[0:-3] + "_sts.bin" 
#    with open(fsp, 'wb') as fn:
#        pickle.dump([peds, rmss, ymax], fn)
#
#
#
###    x_c = [1,15,17, 30, 65, 78, 71, 75, 24, 7, 81, 94, 4, 27, 83, 88]
###    y_c = np.array([22, 22, 22, 22, 47, 47, 82, 82, 100, 100, 100, 100, 150, 150, 150, 150]) * 0.02
##    ax1 = fig.add_subplot(111)
##    ax1.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
##    import pickle
##    fsp =fdir + "femb_%dRT_rms.bin"%fembi
##    with open(fsp, 'wb') as fn:
##        pickle.dump(rmss, fn)
##
##
##    ax1.set_ylim((0,10))
##
##    if (fembi ==3):
##        ax1_1 = ax1.twinx()
##        chnnos = np.arange(128)
##        ax1_1.scatter(chnnos, B4_with_cap, color = 'g', marker = '.', label = "Capacitance / pF" )
##        
##
###    plt.ylabel("ADC counts")
###    plt.legend()
###    plt.subplot(313)
###    plt.plot(np.arange(len(pks)), np.array(peds),marker = '.',  color ='b', label = "Pedestal / bin")
###    plt.plot(np.arange(len(pks)), np.array(pks),marker = '.',  color ='g', label = "Pulse peak / bin")
###    plt.ylim((0,4100))
###    plt.ylabel("ADC counts")
###    plt.grid()
###    plt.legend()
##    plt.xlabel("Channel number")
##    plt.grid(axis='both')
##    plt.tight_layout()
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


