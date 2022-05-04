# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 8/21/2021 5:10:25 AM
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
frst = "D:/Monolithic_FEMB/Rawdata/results/"
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
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_10mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_20mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_30mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_40mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_50mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_60mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_CALI_CHIP3CH3_70mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_CALI_CHIP3CH3_80mV_S16ON.h5",

    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_10mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_20mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_30mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_40mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_50mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_60mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1405_CALI_CHIP3CH3_70mV_S16ON.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_CALI_CHIP3CH3_80mV_S16ON.h5",



        ]
#labels = ( "14 mV/fC, 0.5us",  "14 mV/fC, 1.0us",  "14 mV/fC, 2.0us",  "14 mV/fC, 3.0us" ) 

chips = [3] 

fp_amp_chns = []
for fp in fps:
    f = h5py.File(fdir + fp, 'r')
    dac_v = int(fp[fp.find("CH3_")+4:fp.find("CH3_")+6]) * (1E-3)
    keys = list(f.keys())
    fembs=[0]
    import matplotlib.pyplot as plt
    period = 1000 
    
    amp_chns = []
    for fembi in fembs:
        #for k in range(chips):
        for k in chips:
            for i in [3]:
                key="CH{}".format(128*fembi + 16*k + i)
                y = f[key][0:]
                y_oft1 = np.where(y[period:period*2] == np.max(y[period:period*2]))[0][0] 
                y_oft2 = np.where(y[period*2:period*3] == np.max(y[period*2:period*3]))[0][0] 
                period = y_oft2 - y_oft1 + period
                y_oft = y_oft1 + period

            #for i in range(16):
            for i in [3]:
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
    fp_amp_chns.append([dac_v, amp_chns, ay])


fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})

for i in range(len(fp_amp_chns)):
    y = fp_amp_chns[i][2]
    fc = fp_amp_chns[i][0]*(1.203E-9)/(1E-12)
    print (fp_amp_chns[i][0], fc)
    #pltlen = len( y )
    pltlen = 40
    x = np.arange(pltlen)[0:pltlen]
    #y = np.arange(pltlen)
    plt.plot(x*0.5,y[50-(pltlen//2):50+(pltlen//2)] , marker='.', label="%d fC"%fc, color = "C{}".format(i))
#plt.plot(x*0.5,y[ymaxpos-(pltlen//2):ymaxpos+(pltlen//2)] , marker='.', label="ASIC%02d"%k, color = "C{}".format(k))
plt.grid(True)
plt.ylim((0,5000))
plt.xlim((0,pltlen//2))
plt.xlabel("Time / $\mu$s")
plt.ylabel("ADC counts / bin")

plt.legend()
plt.tight_layout()
plt.savefig(frst+fps[0][0:-4] + "ext_waveform.png")
#plt.show()
plt.close()

#exit()


#fig = plt.figure(figsize=(12, 8))
#plt.rcParams.update({'font.size': 16})
#
##for i in range(4):
#for i in range(len(fp_amp_chns)):
#    chns = np.arange(16*chips)
#    amps = fp_amp_chns[i][1]
#
#    plt.plot(chns, amps, marker = '.', label = "ASICDAC%02d"%fp_amp_chns[i][0])
#    for m in range(chips):
#        plt.vlines(m*16-0.5, 0, 5000, color = 'c')
#    plt.legend()
#plt.xlabel("FEMB CH#")
#plt.ylabel("ADC amplitude / bin")
##plt.show()
#plt.savefig(frst+fps[0][0:-4] + "gain_dis.png")
#plt.close()
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
    return slope, constant, error_gain

#cap=1.85E-13
#dac_mv = 65/8.0/1000 #14mV/fC
#enc_per_v = cap / (1.602E-19)
#enc_daclsb = dac_mv * enc_per_v
#encs = np.array([8,0x10,0x18,0x20,0x28,0x30]) *enc_daclsb
amps = []
ess = []
for i in range(len(fp_amp_chns)):
    amp = fp_amp_chns[i][1][0]
    fc = fp_amp_chns[i][0]*(1.203E-9)/(1E-12)
    es = fc*6250
    amps.append(amp)
    ess.append(es)


x = amps
y = ess
fit_results = linear_fit(x, y)

fity = np.array(x)*fit_results[0] + fit_results[1]
residue = np.array(fity) - np.array(y)
max_res = np.max(residue)
min_res = np.min(residue)
inl = ((max_res-min_res)/(2*(y[-1] - y[0])))*100
#inls.append(inl)
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 16})        
plt.scatter (x, np.array(y)/6250, marker = "o", color = 'r')
plt.plot (x, fity/6250, color = 'b', label = "Gain = %d (e-/LSB)\n INL = %.2f%%"%(fit_results[0], inl))
plt.xlim((0,4000))
plt.ylim((0,100))
plt.xlabel("Amplitude / bit")
plt.ylabel("Charge / fC")
plt.title("Linear Fit")
plt.grid()
plt.legend()
plt.savefig(frst+fps[0][0:-4] + "ext_linear.png")
#plt.show()
plt.close()

exit()

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

