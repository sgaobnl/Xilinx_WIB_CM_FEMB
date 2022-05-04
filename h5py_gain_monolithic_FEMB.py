# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 3/5/2022 12:43:15 AM
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
import pickle
import statsmodels.api as sm

fdir = "D:/Monolithic_FEMB/Rawdata_VDDP_VDDA_together/"
frst = "D:/Monolithic_FEMB/Rawdata_VDDP_VDDA_together/results/"
fdir = "D:/Monolithic_FEMB/Rawdata/"
fdir = "D:/FEMB_IO1826_1A/RawdataP5B/"
frst = "D:/FEMB_IO1826_1A/RawdataP5B/results/"
fdir = "D:/FEMB_IO1826_1A/Rawdata_P4CD_2/"
frst = "D:/FEMB_IO1826_1A/Rawdata_P4CD_2/results/"
fps = [ 
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x04_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x08_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x0c_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x10_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x14_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x18_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x1c_S16ON.h5",

#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x30_S16ON.h5",

        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x04.h5",
        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x08.h5",
        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x0c.h5",
        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x10.h5",
        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x14.h5",
        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x18.h5",
        #"LN_000pF_BRD01_CDP4_ADCP2_FEP5B_SEOFF_500pA_900BL1420_S16ON_ADAC0x1c.h5",

#        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x08.h5",
        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x10.h5",
        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x18.h5",
        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x20.h5",
        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x28.h5",
        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x30.h5",
        "LN_150pF_BRD2_4_CDP4_ADCP2_FEP5B_SEOFF_500pA_200BL1420_S16ON_ADAC0x38.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEON_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x30_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_ADAC0x08_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_900BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_900BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_900BL1420_ADAC0x18_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_900BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_900BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_900BL1420_ADAC0x18_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_ADAC0x30_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_900BL1420_ADAC0x18_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_900BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_900BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_900BL1420_ADAC0x18_S16ON.h5",

#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x08_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x10_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x18_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x20_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x28_S16ON.h5",
#        "RT_000pF_BRD01_CDP3_ADCP2SEON_FEP5SEOFF_500pA_200BL1420_ADAC0x30_S16ON.h5",
#

        ]
#labels = ( "14 mV/fC, 0.5us",  "14 mV/fC, 1.0us",  "14 mV/fC, 2.0us",  "14 mV/fC, 3.0us" ) 

chips = 8

fp_amp_chns = []
for fp in fps:
    f = h5py.File(fdir + fp, 'r')
   #     "RT_000pF_BRD01_CDP3_ADCP2SE_FEP5BSE_500pA_200BL1420_S16ON_ADAC0x30.h5",
    dac_v = int(fp[fp.find("_ADAC0x")+7:fp.find("_ADAC0x")+9], 16)
    keys = list(f.keys())
    fembs=[0]
    import matplotlib.pyplot as plt
    period = 519
    
    amp_chns = []
    for fembi in fembs:
        for k in range(chips):
            for i in [4]:
                key="CH{}".format(128*fembi + 16*k + i)
                y = f[key][0:]
                y_oft1 = np.where(y[period:period*2] == np.max(y[period:period*2]))[0][0] 
                y_oft2 = np.where(y[period*2:period*3] == np.max(y[period*2:period*3]))[0][0] 
                period = y_oft2 - y_oft1 + period
                y_oft = y_oft1 + period

            for i in range(16):
                key="CH{}".format(128*fembi + 16*k + i)
                y = f[key][0:]
                
                #if i == 0:
                #    y_oft1 = np.where(y[period:period*2] == np.max(y[period:period*2]))[0][0] 
                #    y_oft2 = np.where(y[period*2:period*3] == np.max(y[period*2:period*3]))[0][0] 
                #    period = y_oft2 - y_oft1 + period
                #    y_oft = y_oft1 + period
                y = y[y_oft-50:]
                leny = len(y)
                avg_n = (leny//period - 10)
                for a in range(avg_n):
                    if (a==0):
                        ay=y[0:period].astype('uint64')
                    else:
                        ay=ay + y[period*a:period*(a+1)].astype('uint64')
                ay = ay/avg_n
                amp = np.max(ay) - ay[0]
                amp_chns.append(amp)
    fp_amp_chns.append([dac_v, amp_chns])

fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})

#for i in range(4):
for i in range(len(fp_amp_chns)):
    chns = np.arange(16*chips)
#    chns = np.delete(chns,54)
#    amps = np.delete(fp_amp_chns[i][1], 54)
#    #gains = np.delete(gains,54)
    amps = fp_amp_chns[i][1]

    plt.plot(chns, amps, marker = '.', label = "ASICDAC%02d"%fp_amp_chns[i][0])
    for m in range(chips):
        plt.vlines(m*16-0.5, 0, 5000, color = 'c')
    plt.legend()
plt.xlabel("FEMB CH#")
plt.ylabel("ADC amplitude / bin")
#plt.show()
plt.savefig(frst+fps[0][0:-4] + "gain_dis.png")
plt.close()

def linear_fit(x, y):
    error_fit = False 
    try:
        results = sm.OLS(y,sm.add_constant(x)).fit()
    except ValueError:
        error_fit = True 
    if ( error_fit == False ):
        error_gain = False 
        try:
            slope = results.params[1]
        except IndexError:
            slope = 0
            error_gain = True
        try:
            constant = results.params[0]
        except IndexError:
            constant = 0
    else:
        slope = 0
        constant = 0
        error_gain = True

    y_fit = np.array(x)*slope + constant
    delta_y = abs(y - y_fit)
    inl = delta_y / (max(y)-min(y))
    peakinl = max(inl)
    return slope, constant, peakinl, error_gain

cap=1.85E-13
dac_mv = 65/8.0/1000 #14mV/fC
enc_per_v = cap / (1.602E-19)
enc_daclsb = dac_mv * enc_per_v
encs = np.array([8,0x10,0x18,0x20,0x28,0x30]) *enc_daclsb

gains = []
#for i in range(128):
for i in range(16*chips):
    x = []
    y = []
    for k in fp_amp_chns:
        x.append( k[1][i] )
        y.append( k[0]*enc_daclsb )
    fit_results = linear_fit(x, y)
    gains.append(fit_results[0])
    if i%16 == 4:
        print (fit_results[0])

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})        
#chns = np.arange(128)
chns = np.arange(16*chips)

#chns = np.delete(chns,54)
#gains = np.delete(gains,54)

plt.plot(chns, np.array(gains), marker = '.', label = "14mV/fC, 2.0 $\mu$s"  )
#for i in range(8):
for i in range(chips):
    plt.vlines(i*16-0.5,0, (int(np.max(gains)) + 50), linestyles="dashed", colors='g')
plt.xlabel("Channel number")
plt.ylabel("Inverted Gain (e-/bin)")

plt.xlim ((-1,128))
plt.ylim ((0,200))
plt.legend()
plt.grid()
plt.savefig(frst+fps[0][0:-4] + "_gain_dis.png")
plt.close()

import pickle
fsp =frst + fps[0][0:-4] + "_gain_dis.bin"
with open(fsp, 'wb') as fn:
    pickle.dump(gains, fn)

