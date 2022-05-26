# -*- coding: utf-8 -*-
"""
File Name: cls_udp.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:52:43 PM
Last modified: 5/17/2022 2:25:31 PM
"""

import pickle
import h5py

fp = "D:/IO_1826_1B/QC/FEMB222_LN_150pF/logs_tm008.bin"
with open(fp, 'rb') as fp:
    logs = pickle.load(fp)

for log in logs:
    print (log, logs[log])

#keys = []
#for key in logs:
#    keys.append(key)
#
#for key in keys[0:100]:
#    print (key)

#tmp1 = logs["D:/IO_1826_1B/QC/FEMB222_LN_150pF/ASICDAC_CALI/CALI_900mVBL_14_0mVfC_3_0us_ASICDAC0x04.h5"]
#tmp2 = logs["D:/IO_1826_1B/QC/FEMB222_LN_150pF/ASICDAC_CALI/CALI_900mVBL_14_0mVfC_3_0us_ASICDAC0x08.h5"]
#
#print (tmp1[0][0], tmp2[0][0])
#print (tmp1[1][0], tmp2[1][0])
#print (tmp1[2][0], tmp2[2][0])
#print (tmp1[3][0], tmp2[3][0])
#
#fp1 = "D:/IO_1826_1B/QC/FEMB222_LN_150pF/ASICDAC_CALI/CALI_900mVBL_14_0mVfC_3_0us_ASICDAC0x04ana.bin"
#fp2 = "D:/IO_1826_1B/QC/FEMB222_LN_150pF/ASICDAC_CALI/CALI_900mVBL_14_0mVfC_3_0us_ASICDAC0x08ana.bin"
#
#with open(fp1, 'rb') as fp1:
#    tmp3 = pickle.load(fp1)
#
#with open(fp2, 'rb') as fp2:
#    tmp4 = pickle.load(fp2)
#
#print ("AAAAAAAAAAAAAAAAAAAAA")
#print (tmp3[0][0], tmp4[0][0])
#print (tmp3[1][0], tmp4[1][0])
#print (tmp3[2][0], tmp4[2][0])
#print (tmp3[3][0], tmp4[3][0])
#
#fp3 = "D:/IO_1826_1B/QC/FEMB222_LN_150pF/ASICDAC_CALI/CALI_900mVBL_14_0mVfC_3_0us_ASICDAC0x04.h5"
#fp4 = "D:/IO_1826_1B/QC/FEMB222_LN_150pF/ASICDAC_CALI/CALI_900mVBL_14_0mVfC_3_0us_ASICDAC0x08.h5"
#
#fp3_d = h5py.File(fp3, 'r')
#fp3_k = list(fp3_d.keys())
#print (max(fp3_d["CH0"][0:1500]))
#fp4_d = h5py.File(fp4, 'r')
#fp4_k = list(fp4_d.keys())
#print (max(fp4_d["CH0"][0:1500]))

