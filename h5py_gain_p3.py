# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 4/25/2021 11:20:27 PM
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
pattern05 = "LN_150pF_CDP3_P4FE_se_100pA_2001405bufoff_P2ADC_se_asicdac08"
pattern10 = "LN_150pF_CDP3_P4FE_se_100pA_2001410bufoff_P2ADC_se_asicdac08"
pattern20 = "LN_150pF_CDP3_P4FE_se_100pA_2001420bufoff_P2ADC_se_asicdac08"
pattern30 = "LN_150pF_CDP3_P4FE_se_100pA_2001430bufoff_P2ADC_se_asicdac08"

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

patterns = [pattern05, pattern10,pattern20,pattern30]

for abc in range(4):
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
                plocs, _ = find_peaks(py,  height=500)
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
                    plt.plot(x[0:100]*0.5,ay[0:100],  marker = '.', label= "ASIC00CH1", color = "C{}".format(abc))
                    plt.legend()
            plt.xlabel("Time / $\mu$s")
            plt.ylabel("Amplitude / bin")
            plt.title("Averaging Waveforms")
            plt.grid(True)
            plt.xlim((15,35))
            plt.ylim((-100,1500))
        print (np.mean(ymax), np.std(ymax))
plt.tight_layout()
#plt.show()
plt.savefig(frst+fp[0:-3] + "wfm_avg_gains.png")
plt.close()





#for fembi in fembs:
#    fig = plt.figure(figsize=(16, 12))
#    plt.rcParams.update({'font.size': 16})
#    for k in range(8):
#        x = 420 + k+1
#        plt.subplot(x)
#        for i in range(16):
#            key="CH{}".format(128*fembi + 16*k + i)
#            dlen = 4000
#            x = np.arange(dlen)
#            y = f[key][0:dlen]
#            ymaxpos = np.where(y[500:3500] == np.max(y[500:3500]))[0][0] + 500
##            plt.plot(x,y, label=key, color = "C{}".format(k))
#            plt.plot(x[0:100]*0.5,y[ymaxpos-50:ymaxpos+50] ,label=key, color = "C{}".format(i%10))
##            plt.ylim((0,4000)) 
#            plt.xlim((0,50)) 
#            plt.grid(True)
#            plt.xlabel("Time / $\mu$s")
#            plt.ylabel("Amplitude / bin")
#
#            plt.title("Waveform: CH{} to CH{}".format(k*16, (k+1)*16-1))
##            plt.ylim((np.mean(y)-10,(np.mean(y)+10))) 
#    #        plt.draw()
#    #        plt.legend()
#    #        plt.pause(0.5)
#    plt.tight_layout()
##    plt.show()
#    plt.savefig(frst+fp[0:-3] + "wfm.png")
#    plt.close()
#
#for fembi in fembs:
#    fig = plt.figure(figsize=(16, 12))
#    plt.rcParams.update({'font.size': 18})
#    #from detect_peaks import detect_peaks
#    from scipy.signal import find_peaks, peak_widths
#    dlen = 100000
#    rmss = []
#    pks = []
#    peds = []
#    ymax = []
#
#    for k in range(8):
#        x = 420 + k+1
#        plt.subplot(x)
#        for i in range(16):
#            key="CH{}".format(fembi*128 + 16*k + i)
#            y = f[key][0:dlen]
#            #plocs = detect_peaks(y, mph=None, mpd=50, threshold=500, edge='rising')
#            py = np.array(y.astype('int16')) - int(np.mean(y))
#            plocs, _ = find_peaks(py,  height=300)
#            if len(plocs) > 2:
#                break
#        print (plocs)
#        if len(plocs) < 2: 
#            plocs = np.arange(0, 369*261, 261)
#
#        for i in range(16):
#            key="CH{}".format(fembi*128 + 16*k + i)
#            y = f[key][0:dlen]
#            #plocs = detect_peaks(y, mph=None, mpd=50, threshold=500, edge='rising')
#            #py = np.array(y.astype('int16')) - int(np.mean(y))
#            #plocs, _ = find_peaks(py,  height=100)
#            xlen = plocs[2] - plocs[1] - 10
#            avgm = 10
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
#            ay = (ay/avgm) 
#            ymax.append(np.max(ay))
#            pks.append(np.max(ay))
#            x = np.arange(xlen)
#            if i%16 ==0: 
#                plt.plot(x[0:100]*0.5,ay[0:100], label= "ASIC#%d"%k, color = "C{}".format(k))
#                plt.legend()
#            else:
#                plt.plot(x[0:100]*0.5,ay[0:100],  color = "C{}".format(k))
#            #plt.plot(x[0:100]*0.5,ay[0:100],  color = "C{}".format(k))
#        plt.xlabel("Time / $\mu$s")
#        plt.ylabel("Amplitude / bin")
#        plt.title("Averaging Waveforms")
#        plt.grid(True)
#        plt.xlim((0,50))
#    print (np.mean(ymax), np.std(ymax))
##    plt.ylim((-1000,1000))
#    plt.tight_layout()
#    #plt.show()
#    plt.savefig(frst+fp[0:-3] + "wfm_avg.png")
#    plt.close()
#
#    import pickle
#    fsp =fdir + fp[0:-3] + "_sts_femb%d.bin"%fembi
#    with open(fsp, 'wb') as fn:
#        pickle.dump([peds, rmss, ymax], fn)
#
#
#    fig = plt.figure(figsize=(12, 8))
#    plt.rcParams.update({'font.size': 24})
#    chnnos = np.arange(128)
#    plt.plot(chnnos, ymax, marker = '.', color ='r', label = "Pulse Amplitude")
#    plt.plot(chnnos, peds, marker = '.', color ='b', label = "Pedestal")
#    for i in range(8):
#        plt.vlines(i*16-0.5,0, 4100, linestyles="dashed", colors='g')
#
#    plt.xlim((-1,129))
#    plt.ylim((0,4100))
#    plt.ylabel("ADC output / bin")
#    plt.xlabel("Channel Number")
#    plt.grid()
#    plt.legend()
#
#    plt.tight_layout()
#    plt.savefig(frst+fp[0:-3] + "pls_ped_dis.png")
#    plt.close()
#
#    fig = plt.figure(figsize=(12, 8))
#    plt.rcParams.update({'font.size': 24})
#
#
#
#    fig = plt.figure(figsize=(12, 8))
#    plt.rcParams.update({'font.size': 24})
#    ax1 = fig.add_subplot(111)
#    ax1.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
#    #ax1.plot(np.arange(len(rmss)), np.array(rmss)*200, marker = '.', color ='r', label = "LN2, Cd=150pF, ENC=(%d +/- %d) e-"%(np.mean(np.array(rmss)*200), np.std(np.array(rmss)*200)))
#    #import pickle
#    #fsp =fdir + "femb_%d_rms.bin"%fembi
#    #with open(fsp, 'wb') as fn:
#    #    pickle.dump(rmss, fn)
#    #ax1.set_ylim((0,2000))
#    for i in range(8):
#        plt.vlines(i*16-0.5,0, int(np.max(rmss))+2, linestyles="dashed", colors='g')
#    plt.ylabel("ADC counts / bin")
#    plt.legend()
#    plt.legend()
#    plt.xlabel("Channel number")
#    plt.grid(axis='both')
#    plt.tight_layout()
#    #plt.show()
#    plt.savefig(frst+fp[0:-3] + "pls_rms_dis.png")
#    plt.close()
#
#    exit()
#
##    plt.subplot(311)
##    plt.plot(np.arange(len(peds)), peds, marker = '.', color ='b', label = "Pedestal / bin")
##    plt.ylim((0,4100))
##    plt.ylabel("ADC counts")
##    plt.grid()
##    plt.legend()
##    plt.subplot(312)
#
#    if (fembi ==1):
#        import pickle
#        import copy
#        with open("./APA_Capacitance_B2.bin", 'rb') as fn:
#            apa_cap = pickle.load(fn)
#
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
##        B4_with_cap[16*3+2] =  B4_with_cap[16*3+2]  + 82 peaks, _ = find_peaks(ch1data,  height=pe)
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
#    #ax1.plot(np.arange(len(rmss)), rmss, marker = '.', color ='r', label = "RMS noise / bin")
#    ax1.plot(np.arange(len(rmss)), np.array(rmss)*200, marker = '.', color ='r', label = "LN2, Cd=150pF, ENC=(%d +/- %d) e-"%(np.mean(np.array(rmss)*200), np.std(np.array(rmss)*200)))
#    import pickle
#    fsp =fdir + "femb_%dRT_rms.bin"%fembi
#    with open(fsp, 'wb') as fn:
#        pickle.dump(rmss, fn)
#
#
#    ax1.set_ylim((0,2000))
#
#    if (fembi ==3):
#        ax1_1 = ax1.twinx()
#        chnnos = np.arange(128)
#        ax1_1.scatter(chnnos, B4_with_cap, color = 'g', marker = '.', label = "Capacitance / pF" )
#    elif  (fembi ==1):
#        ax1_1 = ax1.twinx()
#        chnnos = np.arange(128)
#        ax1_1.scatter(chnnos, apa_cap, color = 'g', marker = '.', label = "Capacitance / pF" )
#        
#
##    plt.ylabel("ADC counts")
##    plt.legend()
##    plt.subplot(313)
##    plt.plot(np.arange(len(pks)), np.array(peds),marker = '.',  color ='b', label = "Pedestal / bin")
##    plt.plot(np.arange(len(pks)), np.array(pks),marker = '.',  color ='g', label = "Pulse peak / bin")
##    plt.ylim((0,4100))
#    plt.ylabel("ENC / e-")
##    plt.grid()
#    plt.legend()
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


