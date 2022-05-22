import pickle
import matplotlib.pyplot as plt
import numpy as np


hdf_dir = "D:/IO_1826_1B/QC/FEMB209_LN_150pF/"

fp = hdf_dir+"logs_tm007.bin"

with open(fp, 'rb') as fp:
    logs = pickle.load(fp)
#for keys in logs:
#    print(keys)
        
if "LN" not in logs["Env"] :
    sncs = ["900mVBL", "200mVBL"]
    sgs = ["14_0mVfC" ]
    sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]
else:
    sncs = ["900mVBL", "200mVBL"]
    sgs = ["14_0mVfC", "25_0mVfC", "7_8mVfC", "4_7mVfC" ]
    sts = ["1_0us", "0_5us",  "3_0us", "2_0us"]
        
fig_wave_p,axes_wave_p = plt.subplots(4,4)
fig_wave_n,axes_wave_n = plt.subplots(4,4)
        
fig_peak_dac, axes_peak_dac= plt.subplots(4,4)
        
nx=0
ny=0
        
for i in range(len(sncs)):
#for i in range(1):
    snc = i
    if i == 0:
       vmaxdac = 0x20
    else:
       vmaxdac = 0x40
     
    for j in range(len(sgs)):
    #for j in range(1):
        sg0 = j%2
        sg1 = j//2
        if j == 0: #14mV/fC
           ks = [0,1,2,3]
        else:
           ks = [3] #only 2.0us
        
        for k in ks: 
        #for k in range(1): 
            st0 = k%2
            st1 = k//2
        
            wave_peak = []
            dac_value = []
        
            for asicdac in range(0, vmaxdac, 4):
             #for asicdac in range(0,6,4):
                cali_fp = hdf_dir + "ASICDAC_CALI/CALI_{}_{}_{}_ASICDAC0x{:02x}.h5".format(sncs[i], sgs[j], sts[k], asicdac)
                       
                asic_log = logs[cali_fp]
        
                wave_peak.append(asic_log[2][0])
                dac_value.append(asicdac)
        
                xx_p = [i for i in range(40,60)]
                xx_n = [i for i in range(90,120)]
                axes_wave_p[nx,ny].plot(xx_p, asic_log[5][0][40:60],label='DAC={}'.format(asicdac))
                axes_wave_n[nx,ny].plot(xx_n, asic_log[5][0][90:120],label='DAC={}'.format(asicdac))
        
                axes_wave_p[nx,ny].set_xlabel('time')
                axes_wave_p[nx,ny].set_title('{} {} {}'.format(sncs[i], sgs[j], sts[k]))
                axes_wave_p[nx,ny].legend(loc='upper left')
        
                axes_wave_n[nx,ny].set_xlabel('time')
                axes_wave_n[nx,ny].set_title('{} {} {}'.format(sncs[i], sgs[j], sts[k]))
                axes_wave_n[nx,ny].legend(loc='upper left')
                   
            dac_np = np.array(dac_value)
            peak_np = np.array(wave_peak)
            axes_peak_dac[nx,ny].scatter(dac_np,peak_np,c='r')
            slope,intercept = np.polyfit(dac_np,peak_np,1)
            axes_peak_dac[nx,ny].plot(dac_np, slope*dac_np+intercept,label='{:.2f}*x+{:.2f}'.format(slope,intercept))
            axes_peak_dac[nx,ny].set_title('{} {} {}'.format(sncs[i], sgs[j], sts[k]))
            axes_peak_dac[nx,ny].legend(loc='upper right')
        
            if ny==3: 
               nx=nx+1
               ny=0
            else:
               ny=ny+1
        
plt.show()




        
