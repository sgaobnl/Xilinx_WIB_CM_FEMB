# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 4/25/2021 11:47:16 PM
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

fdir = "D:/CM_FEMB_P3/Rawdata_0423/"
frst = "D:/CM_FEMB_P3/results_0423/"
pattern = "RT_150pF_CDP3_P4FE_se_100pA_2001410bufoff_P2ADC_se_asicdac04"
pattern = "RT_150pF_CDP3_P4FE_se_100pA_2001410bufoff_P2ADC_se_asicdac1f"
pattern = "RT_150pF_CDP3_P4FE_se_100pA_9001410bufoff_P2ADC_se_asicdac10"
pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001410bufoff_P2ADC_se_asicdac04"
pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001410bufoff_P2ADC_se_asicdac20"
pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac04"
pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac08"
pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac0c"
pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac10"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac14"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac18"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac1c"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac20"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac04"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac08"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac0c"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac10"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac14"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac18"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac1c"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac20"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac04"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac08"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac0c"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac10"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac14"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac18"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac1c"
#pattern = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac20"
#pattern05 = "LN_150pF_CDP3_P4FE_se_100pA_2004710bufoff_P2ADC_se_asicdac08"
#pattern10 = "LN_150pF_CDP3_P4FE_se_100pA_2007810bufoff_P2ADC_se_asicdac08"
pattern10on = "LN_150pF_CDP3_P4FE_se_100pA_2001410bufoff_P2ADC_se_asicdac08"
pattern10off = "LN_150pF_CDP3_P4FE_se_100pA_2001410bufon_P2ADC_se_asicdac08"
#pattern30 = "LN_150pF_CDP3_P4FE_se_100pA_2002510bufoff_P2ADC_se_asicdac08"

def sinc_interp(x, s, u):
    if len(x) != len(s):
        raise ValueError('x and s must be the same length')
    # Find the period    
    T = s[1] - s[0]
    sincM = np.tile(u, (len(s), 1)) - np.tile(s[:, np.newaxis], (1, len(u)))
    y = np.dot(x, np.sinc(sincM/T))
    return y

#04122021
#pattern = "LN_150pF_P4FE_se_100pA_bufoff_P2_ADC_se_14_10_asicdac08_bl200"
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8, 6))
plt.rcParams.update({'font.size': 18})

patterns = [pattern10on, pattern10off]

for abc in range(2):
    pattern  = patterns[abc]
    fp = pattern + ".h5"
    
    f = h5py.File(fdir + fp, 'r')
    keys = list(f.keys())
    fembs=[0]
    
    
    for fembi in fembs:
        from scipy.signal import find_peaks, peak_widths
        dlen = 300000
        rmss = []
        pks = []
        peds = []
        ymax = []
        for k in range(1):
            for i in range(16):
                key="CH{}".format(fembi*128 + 16*k + i)
                y = f[key][0:dlen]
                py = np.array(y.astype('int16')) - int(np.mean(y))
                if abc == 0: 
                    plocs, _ = find_peaks(py,  height=200)
                elif abc == 1: 
                    plocs, _ = find_peaks(py,  height=400)
                elif abc == 2: 
                    plocs, _ = find_peaks(py,  height=600)
                else:
                    plocs, _ = find_peaks(py,  height=800)

                if len(plocs) > 2:
                    break
            if len(plocs) < 2: 
                plocs = np.arange(0, 369*261, 261)
    
            for i in [1]:
                key="CH{}".format(fembi*128 + 16*k + i)
                y = f[key][0:dlen]
                xlen = plocs[2] - plocs[1] - 10
                avgm = 10
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
                x = np.arange(xlen)
#                k = 0 
#                l = 100 
#                i_p = 100
#                s = np.arange(k, l)
#                u = np.linspace(k,l,(l-k)*i_p)
#                aysinc = sinc_interp(ay[0:100], s, u)
#                print (len(aysinc))
#
                if i%16 ==0: 
                    plt.plot(x[0:100]*0.5,ay[0:100], label= "ASIC#%d"%k, color = "C{}".format(abc))
                    plt.legend()
                else:
                    #plt.plot(x[0:100]*0.5,ay[0:100], marker = '.',  color = "C{}".format(abc))
                    plt.plot(x[0:100]*0.5,ay[0:100],  marker = '.', label= "Peak = {}".format(int(np.max(ay[0:100]))), color = "C{}".format(abc))
                    plt.legend()
            plt.xlabel("Time / $\mu$s")
            plt.ylabel("Amplitude / bin")
            plt.title("Averaging Waveforms")
            plt.grid(True)
            plt.xlim((15,35))
            plt.ylim((-100,2500))
        print (np.mean(ymax), np.std(ymax))
plt.tight_layout()
#plt.show()
plt.savefig(frst+fp[0:-3] + "wfm_avg_tps.png")
plt.close()




