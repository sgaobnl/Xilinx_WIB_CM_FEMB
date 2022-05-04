# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 11/1/2021 7:12:23 AM
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
import matplotlib.pyplot as plt

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


fdir = "D:/Monolithic_FEMB/Rawdata_VDDP_VDDA_together/"
frst = "D:/Monolithic_FEMB/Rawdata_VDDP_VDDA_together/results/"
fdir = "D:/Monolithic_FEMB/Rawdata_10232021/"
frst = "D:/Monolithic_FEMB/Rawdata_10232021/results/"
fps = [ 
#    "Rawdata_08_29_2021_16_17_24_RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_S16ON_lin_chip3ch0.h5",
    #"RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch1.h5",
    #"RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch0_mV.h5",
    #"RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3ch0_mV.h5",
    #"RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch4.h5",
    #"RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin1mV400mVoft_chip3ch1_mV.h5",
    #"RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_S16ON_lin1mV000mVoft_chip3ch1_mV.h5",
#    "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_CALI_CHIP3CH3_80mV_S16ON.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH0_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH1_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH2_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH3_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH4_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH5_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH6_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH7_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH8_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH9_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHa_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHb_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHc_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHd_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHe_mV.h5",
    "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHf_mV.h5",


        ]
#labels = ( "14 mV/fC, 0.5us",  "14 mV/fC, 1.0us",  "14 mV/fC, 2.0us",  "14 mV/fC, 3.0us" ) 

#chips = [3] 

amp_chip = []
for fp in fps:
    fp_amp_chns = []
    f = h5py.File(fdir + fp, 'r')
    chipid = int(fp[fp.find("chip")+4]) 
    chid = int(fp[fp.find("chip")+7], 16) 
    fembch = chipid*16 + chid

    keys = list(f.keys())

    chkeys = []
    for key in keys:
        if "CH{:03d}".format(fembch) in key:
            chkeys.append(key)

    print (chkeys)
    period = 1000 

    for key in chkeys:
        if "AMP040" in key:
            y = f[key][0:]
            y_oft1 = np.where(y[period:period*2] == np.max(y[period:period*2]))[0][0] 
            y_oft2 = np.where(y[period*2:period*3] == np.max(y[period*2:period*3]))[0][0] 
            period = y_oft2 - y_oft1 + period

    for key in chkeys:
        y = f[key][0:]
        y_oft1 = np.where(y[period:period*2] == np.max(y[period:period*2]))[0][0] 
        y_oft = y_oft1 + period
        y = y[y_oft-50:]
        leny = len(y)
        avg_n = (leny//period - 10)
        for a in range(avg_n):
            if (a==0):
                ay=y[0:period].astype('uint64')
            else:
                ay=ay + y[period*a:period*(a+1)].astype('uint64')
        ay = ay/avg_n
        ay_ped = np.mean(ay[0:10])
        amp = np.max(ay) - ay_ped
        dac_mv = (int(key[key.find("AMP")+3:key.find("AMP")+6])) / 10.0
        fp_amp_chns.append([dac_mv, amp, ay, ay_ped])
    amp_chip.append([fembch, fp_amp_chns])

fig = plt.figure(figsize=(24, 12))
plt.rcParams.update({'font.size': 12})
#ax = []
for m in range(len(amp_chip)):
#for m in range(1):
    #if amp_chip[0] == 11:
    #    continue
    n = amp_chip[m][0]%16
    ax = plt.subplot2grid((4,4), (n//4,n%4))
    fembch = amp_chip[m][0]
    fp_amp_chns = amp_chip[m][1]

    for i in range(len(fp_amp_chns)):
        y = fp_amp_chns[i][2]
        if max(y) < (4000-fp_amp_chns[i][3]):
            fc = fp_amp_chns[i][0]*(1E-3)*(1.203E-9)/(1E-12)
            pltlen = 40
            x = np.arange(pltlen)[0:pltlen]
            ax.plot(x*0.5,y[50-(pltlen//2):50+(pltlen//2)] , marker='.', label="%d fC"%fc, color = "C{}".format(i%10))
        ax.grid(True)
        ax.set_title("FEMB_CH#%d (ASIC#%dCH#%d)"%(fembch, fembch//16, fembch%16))
        ax.set_ylim((0,4100))
        ax.set_xlim((0,pltlen//2))
        ax.set_xlabel("Time / $\mu$s")
        ax.set_ylabel("ADC counts / bin")
        #ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(frst+fps[0][0:-4] + "ext_waveform.png")
#plt.show()
plt.close()

inls = []
fig = plt.figure(figsize=(24, 12))
plt.rcParams.update({'font.size': 12})
for m in range(len(amp_chip)):
    fembch = amp_chip[m][0]
#    if amp_chip[0] == 11:
#        continue
    fp_amp_chns = amp_chip[m][1]
    amps = []
    ess = []
    for i in range(len(fp_amp_chns)):
        amp = fp_amp_chns[i][1]
        fc = fp_amp_chns[i][0]*(1E-3)*(1.203E-9)/(1E-12)
        if fc <= 90:
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
    inls.append([amp_chip[m][0]%16,inl])

    n = amp_chip[m][0]%16
    ax = plt.subplot2grid((4,4), (n//4,n%4))
    ax.plot (np.array(ess)/6250, residue/((y[-1] - y[0])), color = 'b', marker = 'o', label = "Gain = %d (e-/LSB)\n INL = %.2f%%"%(fit_results[0], inl))
    ax.grid()
    #ax.set_title("FEMB CH#%d"%fembch)
    ax.set_title("FEMB_CH#%d (ASIC#%dCH#%d)"%(fembch, fembch//16, fembch%16))
    ax.set_xlim((0,4000))
    ax.set_xlim((0,100))
    ax.set_ylim((-0.005,0.005))
    #ax.set_xlabel("Amplitude / bit")
    ax.set_xlabel("Charge / fC")
    ax.set_ylabel("Non-linearity")
    #    plt.title("Residual plot")
    #    plt.grid()
    #    plt.legend()
plt.tight_layout()
plt.savefig(frst+fps[0][0:-4] + "ext_residual.png")
#plt.show()
plt.close()

if True:
    fig = plt.figure(figsize=(12, 8))
    plt.rcParams.update({'font.size': 16})        
    x = []
    y = []
    for tmp in inls:
        x.append(tmp[0])
        y.append(tmp[1])
    print (x)
    print (y)
    plt.plot (x, y, marker = 'o',  color = 'r')
    plt.xlim((-2,18))
    plt.ylim((0,0.5))
    plt.xlabel("CH # of Chip#3")
    plt.ylabel("INL = %.2f%%")
#    plt.title("Linear Fit")
    plt.grid()
#    plt.legend()
    plt.savefig(frst+fps[0][0:-4] + "linear_dis.png")
#    plt.show()
    plt.close()



fp_amp_chns = amp_chip[0][1]

if False:
#if True:
    if True:
    #if False:
        fig = plt.figure(figsize=(12, 8))
        plt.rcParams.update({'font.size': 16})
        
        for i in range(len(fp_amp_chns)):
            y = fp_amp_chns[i][2]
            if max(y) < (4000-fp_amp_chns[i][3]):
                fc = fp_amp_chns[i][0]*(1E-3)*(1.203E-9)/(1E-12)
                pltlen = 40
                x = np.arange(pltlen)[0:pltlen]
                plt.plot(x*0.5,y[50-(pltlen//2):50+(pltlen//2)] , marker='.', label="%d fC"%fc, color = "C{}".format(i%10))
        plt.grid(True)
        plt.ylim((0,4100))
        plt.xlim((0,pltlen//2))
        plt.xlabel("Time / $\mu$s")
        plt.ylabel("ADC counts / bin")
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.savefig(frst+fps[0][0:-4] + "ext_waveform.png")
        #plt.show()
        plt.close()
    
    if True:
        amps = []
        ess = []
        for i in range(len(fp_amp_chns)):
            amp = fp_amp_chns[i][1]
            fc = fp_amp_chns[i][0]*(1E-3)*(1.203E-9)/(1E-12)
            #fc = fp_amp_chns[i][0]*(1E-3)*(1.203E-9)/(1E-12)
            if fc <= 90:
            #if True:
                es = fc*6250
                amps.append(amp)
                ess.append(es)
        
        x = amps
        print (amps)
        y = ess
        fit_results = linear_fit(x, y)
        
        fity = np.array(x)*fit_results[0] + fit_results[1]
        residue = np.array(fity) - np.array(y)
        max_res = np.max(residue)
        min_res = np.min(residue)
        inl = ((max_res-min_res)/(2*(y[-1] - y[0])))*100
    
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
    
        fig = plt.figure(figsize=(12, 8))
        plt.rcParams.update({'font.size': 16})        
        #plt.scatter (x, np.array(y)/6250, marker = "o", color = 'r')
        plt.plot (x, residue/((y[-1] - y[0])), color = 'b', marker = 'o', label = "Gain = %d (e-/LSB)\n INL = %.2f%%"%(fit_results[0], inl))
        plt.xlim((0,4000))
        plt.ylim((-0.005,0.005))
        plt.xlabel("Amplitude / bit")
        plt.ylabel("Non-linearity")
    #    plt.title("Residual plot")
        plt.grid()
        plt.legend()
        plt.savefig(frst+fps[0][0:-4] + "ext_residual.png")
        #plt.show()
        plt.close()

exit()

if False:
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

if False:
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
