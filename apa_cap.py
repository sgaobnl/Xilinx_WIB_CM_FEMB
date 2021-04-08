# -*- coding: utf-8 -*-
"""
File Name: chkout_ana.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 11/13/2019 1:50:47 PM
Last modified: 2/7/2021 2:57:08 AM
"""

#defaut setting for scientific caculation
#import numpy
#import scipy
#from numpy import *
#import numpy as np
#import scipy as sp
#import pylab as pl


import struct
import time
from datetime import datetime
import numpy as np
import sys
import os
import copy
import math
import pickle
import statsmodels.api as sm

fn = "./APA_Capacitance_B4.csv"
ccs = []
with open(fn, 'r') as fp:
    for cl in fp:
        tmp = cl.split(",")
        x = []
        for i in tmp:
            if "\n" in i:
                i = i.replace("\n", "")
            x.append(i.replace(" ", ""))
        ccs.append(x)
caps = [0]*128
for i in range(len(ccs)):
    caps[i] = ccs[i][0]
    caps[i+32] = ccs[i][1]
    caps[i+64] = ccs[i][2]
    caps[i+96] = ccs[i][3]

chip12 = caps[0:32][::-1]
chip4 = caps[32:48]
chip3 = caps[48:64]
chip5 = caps[64:80][::-1]
chip6 = caps[80:96][::-1]
chip78 = caps[96:128]

caps = chip12 + chip3 + chip4 + chip5 + chip6 + chip78
tmp = []
for i in caps:
    tmp.append(int(i))
caps = tmp

#for i in range(len(ccs)):
#    caps[i] = int(ccs[i][0])
#    caps[95-i] = int(ccs[i][2])
#    if (i<16):
#        caps[47-i] = int(ccs[i][1])
#        caps[64+47-i] = int(ccs[i][3])
#    else:
#        caps[63-(i%16)] = int(ccs[i][1])
#        caps[64+63-(i%16)] = int(ccs[i][3])

fn = "./APA_Capacitance_B4.bin"
with open(fn, 'wb+') as fp:
    pickle.dump(caps, fp)

print (caps[0:32])
print (caps[32:64])
print (caps[64:96])
print (caps[96:128])
    
#ccs = ccs[1:]

