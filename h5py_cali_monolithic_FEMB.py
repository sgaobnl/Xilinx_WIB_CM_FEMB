# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 8/21/2021 3:19:38 AM
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


fdir = "D:/Monolithic_FEMB/Rawdata/"
frst = "D:/Monolithic_FEMB/Results/"
a = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_10mV_S16ON.h5"
b = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_20mV_S16ON.h5"
c = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_30mV_S16ON.h5"
d = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_40mV_S16ON.h5"
e = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_50mV_S16ON.h5"
f = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_60mV_S16ON.h5"
g = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH0_70mV_S16ON.h5"


lns = [a,b,c,d,e,f,g]

with open(fdir+a, 'rb') as f:
    p0,r,a = pickle.load(f)

from asic_dac_fit import asic_dac_fit
cap=1.85E-13
enc_per_v = cap / (1.602E-19)
enc_daclsb = asic_dac_fit() * enc_per_v
encs = np.array([8,0x10,0x18,0x20, 0x28,0x30]) *enc_daclsb

#oft = fit_results[0]*peds[0] + fit_results[1]
#encs = np.array(encs) - oft

amps = []
for s in lns:
    with open(fdir+s, 'rb') as f:
        p,r,a = pickle.load(f)
    amps.append(a)

gains = []
for i in range(128):
    tmp = []
    for k in amps:
        tmp.append(k[i])
    fit_results = linear_fit(tmp[0:5], encs[0:5] )
    gains.append(fit_results[0])


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})        
chns = np.arange(128)
for k in range(len(amps)):
    plt.plot(chns, amps[k], marker = '.', label = "ASICDAC = " + hex(k*4+4) )
for i in range(8):
    plt.vlines(i*16-0.5,0, 4200, linestyles="dashed", colors='g')

plt.plot(chns, p0, marker = 'o', label = "pedestal")
plt.xlim ((-1,199))
plt.ylim ((0,4200))
plt.legend()
plt.grid()
plt.xlabel("Channel number")
plt.ylabel("Amplitude (bin)")
#plt.show()
plt.savefig(frst+lns[0][0:-4] + "lnpls_res_dis.png")
plt.close()

fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})        
chns = np.arange(128)
plt.plot(chns, gains, marker = '.', label = "14mV/fC, 1.0 $\mu$s"  )
for i in range(8):
    plt.vlines(i*16-0.5,0, (int(np.max(gains)) + 50), linestyles="dashed", colors='g')

plt.xlabel("Channel number")
plt.ylabel("Inverted Gain (e-/bin)")

plt.xlim ((-1,128))
plt.ylim ((0,200))
plt.legend()
plt.grid()
#plt.show()
plt.savefig(frst+lns[0][0:-4] + "ln_gain_dis.png")
plt.close()

import pickle
fsp =fdir + lns[0][0:-4] + "_ln_gain_dis.bin"
with open(fsp, 'wb') as fn:
    pickle.dump(gains, fn)
