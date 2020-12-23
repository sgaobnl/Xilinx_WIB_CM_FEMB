#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:54:11 2019

@author: shanshangao
"""
# This file takes care of the full configuration of ColdADC.
# Input: reference, SDC enable, calibration weights (new or old), sampling rate.
# Set sampling rate, power supply configuration (different between BJT and CMOS references), configure ADC itself.

import time
import sys
import pickle

def get_wghts(fn):
    val = []
    reg = []
    with open(fn, "rb") as fp:   #unpickle raw weights
      reg,val = pickle.load(fp)
#    print(val)
#    print(reg)
    for i in range(len(val)):
        print("{:02X}  {:02X}".format(reg[i],val[i]))
#    cq.bc.adc_load_weights(reg, val)

fn = "/Users/shanshangao/Documents/GitHub/Xilinx_WIB_CM_FEMB/Weights_Records_ColdADC_P1_0065_LN/Raw_Weights_CMOS_16M.bin"

get_wghts(fn)

