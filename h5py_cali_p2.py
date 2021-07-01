# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 4/12/2021 4:27:41 PM
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


fdir = "D:/CM_FEMB_P2/Rawdata040921/"
frst = "D:/CM_FEMB_P2/results_04092021/"
a = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac04_bl200_CM_08_sts_femb0.bin"
b = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac08_bl200_CM_08_sts_femb0.bin"
c = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac0c_bl200_CM_08_sts_femb0.bin"
d = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac10_bl200_CM_08_sts_femb0.bin"
e = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac14_bl200_CM_08_sts_femb0.bin"
f = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac18_bl200_CM_08_sts_femb0.bin"
g = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac1c_bl200_CM_08_sts_femb0.bin"
h = "LN_150pF_P4FE_se_bufoff_100pA_P2_ADC_se_14_10_asicdac1f_bl200_CM_08_sts_femb0.bin"

a = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x04_bl200_sts_femb0.bin"
b = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x08_bl200_sts_femb0.bin"
c = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x0c_bl200_sts_femb0.bin"
d = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x10_bl200_sts_femb0.bin"
e = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x14_bl200_sts_femb0.bin"
#f = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x18_bl200_sts_femb0.bin"
#g = "RT_noTPC_P4FE_se_bufoff_P2_ADC_se_14_10_asicdac0x1c_bl200_sts_femb0.bin"

lns = [a,b,c,d,e,f,g]

with open(fdir+a, 'rb') as f:
    p0,r,a = pickle.load(f)

from asic_dac_fit import asic_dac_fit
cap=1.85E-13
enc_per_v = cap / (1.602E-19)
enc_daclsb = asic_dac_fit() * enc_per_v
encs = np.array([4,8,0x0c, 0x10,0x14]) *enc_daclsb

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
#exit()


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
#plt.show()
plt.savefig(frst+lns[0][0:-4] + "pls_res_dis.png")
plt.close()

fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})        
chns = np.arange(128)
plt.plot(chns, gains, marker = '.', label = "14mV/fC, 1.0 $\mu$s"  )
for i in range(8):
    plt.vlines(i*16-0.5,0, (int(np.max(gains)) + 50), linestyles="dashed", colors='g')

#plt.xlim ((-1,199))
#plt.ylim ((0,4200))
plt.legend()
plt.grid()
plt.show()
plt.savefig(frst+lns[0][0:-4] + "rt_gain_dis.png")
plt.close()

import pickle
fsp =fdir + lns[0][0:-4] + "_rt_gain_dis.bin"
with open(fsp, 'wb') as fn:
    pickle.dump(gains, fn)
