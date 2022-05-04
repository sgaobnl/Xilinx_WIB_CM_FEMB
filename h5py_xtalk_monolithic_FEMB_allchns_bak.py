# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 12/27/2021 10:41:08 AM
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
import pickle
#from matplotlib.backends.backend_pdf import PdfPages
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches

fdir = "I:/the monolithic femb data backup/Rawdata_0821/"
frst = "I:/the monolithic femb data backup/Rawdata_0821/result2/"
xtalk_f = "I:/the monolithic femb data backup/Rawdata_0821/result2/xtalk_result.bin"

#chipid= 3
#xts_all = []
#for tmpi in range(16):
#    fp = "LN_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_XTALK_CH%x_70mV_S16ON.h5"%(tmpi)
#    print (fp)
#    
#    
#    f = h5py.File(fdir + fp, 'r')
#    keys = list(f.keys())
#    fembs=[0]
#    import matplotlib.pyplot as plt
#    
#    
#    def sinc_interp(x, s, u):
#        if len(x) != len(s):
#            raise ValueError('x and s must be the same length')
#        # Find the period    
#        T = s[1] - s[0]
#        sincM = np.tile(u, (len(s), 1)) - np.tile(s[:, np.newaxis], (1, len(u)))
#        y = np.dot(x, np.sinc(sincM/T))
#        return y
#    
#    from scipy.ndimage.interpolation import shift
#    from scipy.signal import find_peaks
#    xts = []
#    
#    
#    pps = []
#    pns = []
#    peds = []
#    fig = plt.figure(figsize=(12, 8))
#    plt.rcParams.update({'font.size': 12})
#    period = 1000 
#    chip_inj = chipid 
#    ch_inj = tmpi 
#    
#    for fembi in fembs:
#        for k in [chip_inj]:
#            for i in [ch_inj]:
#                key="CH{}".format(128*fembi + 16*k + i)
#                y = f[key][0:]
#                y_oft1 = np.where(y[period:period*2] == np.max(y[period:period*2]))[0][0] 
#                y_oft2 = np.where(y[period*2:period*3] == np.max(y[period*2:period*3]))[0][0] 
#                period = y_oft2 - y_oft1 + period
#                y_oft = y_oft1 + period
#    
#            for i in [ch_inj]:
#                key="CH{}".format(128*fembi + 16*k + i)
#                y = f[key][0:]
#                y_plt_oft = y_oft-50
#                y = y[y_plt_oft:]
#                leny = len(y)
#                avg_n = (leny//period - 10)
#                for a in range(avg_n):
#                    if (a==0):
#                        ay=y[0:period].astype('uint64')
#                    else:
#                        ay=ay + y[period*a:period*(a+1)].astype('uint64')
#                ay = ay/avg_n
#                pchn = (np.max(ay)) - (np.max(ay[0:20])) 
#    
#            for i in range(16):
#                x = 1 + i
#                plt.subplot(4, 4, x)
#    
#                key="CH{}".format(128*fembi + 16*k + i)
#                y = f[key][0:]
#    
#                y_plt_oft = y_oft-50
#                y = y[y_plt_oft:]
#                leny = len(y)
#                avg_n = (leny//period - 10)
#                for a in range(avg_n):
#                    if (a==0):
#                        ay=y[0:period].astype('uint64')
#                    else:
#                        ay=ay + y[period*a:period*(a+1)].astype('uint64')
#                ay = ay/avg_n
#    
#                pltlen =100 
#                ay = ay[50 - (pltlen//2):50+(pltlen//2)]
#                p_max = np.max(ay) - np.mean(ay[0:pltlen//5])
#                n_max = np.mean(ay[0:20]) - np.min(ay)
#                if p_max > n_max:
#                    xt_amp = p_max
#                else:
#                    xt_amp = n_max
#                x = np.arange(pltlen)
#                pps.append(np.max(ay))
#                pns.append(np.min(ay))
#                peds.append(int(np.mean(ay[0:20])))
#                
#                plt.plot(x*0.5,ay , marker='.', label="xtalk = %.2f%%"% (xt_amp*100/pchn), color = "C{}".format(i%10))
#                xt = xt_amp/pchn
#                xts.append(xt)
#                plt.legend()
#                plt.grid(True)
#                plt.ylabel("Output / bin ")
#                plt.xlim((0,(pltlen//2)))
#                plt.xlabel("Time / us ")
#    
#        plt.tight_layout()
#        plt.savefig(frst + fp[0:-3] + "chip%d_chk_xtalk_wfm.png"%k)
#        plt.close()
#    xts_all.append(xts)
#
#with open(xtalk_f, 'wb') as f:
#    pickle.dump(xts_all, f)
##print (xts_all)
#xts_all = None

import matplotlib.pyplot as plt
from matplotlib import cm
fig, ax = plt.subplots(figsize=(12,8))
plt.rcParams.update({'font.size': 12})
with open (xtalk_f, 'rb') as f:
    xts_all = pickle.load(f)

c = ax.pcolor(xts_all, cmap=cm.YlOrRd, vmin = 0, vmax = 0.02, edgecolors = 'k')
ax.set_ylabel ("Channel # with Injected Pulser")
ax.set_xlabel ("Crosstalk distribution")
cbar = fig.colorbar(c, ticks=[0,0.002, 0.004, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016, 0.018, 0.02 ])
cbar.ax.set_yticklabels(['0 ','0.2%', '0.4%', '0.6%', '0.8%','1.0%', '1.2%', '1.4%', '1.6%', '1.8%', '2.0%'])
cbar.ax.set_ylabel( "Crosstalk / Injection Pulser (Peak-to-Peak Amplitude)")  # vertically oriented colorbar
plt.tight_layout()
for y in range(16):
    for x in range(16):
        if xts_all[y][x] > 0.9:
            pass
        else:
            ax.text(x+0.2, y+0.3,"%.2f"%(xts_all[y][x]*100), color='b', fontsize=8) 
#plt.savefig(xtalk_f[0:-4] + ".png", format = "png")
plt.savefig(frst + "xtalk_2d.png")
plt.close()


