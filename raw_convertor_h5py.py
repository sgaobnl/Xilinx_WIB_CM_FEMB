# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 2/6/2021 11:25:58 PM
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

class RAW_CONV():
    def raw_conv_feedloc(self, raw_data):
        smps = int(len(raw_data) //2)
        dataNtuple =struct.unpack_from(">%dH"%(smps),raw_data)
        if (self.jumbo_flag == True):
            pkg_len = int(0x1E06/2)
        else:
            pkg_len = int(0x406/2)

        feed_loc=[]
        pkg_index  = []
        datalength = int( (len(dataNtuple) // pkg_len) -3) * (pkg_len)
        data_rest = raw_data[(datalength + pkg_len)*2:]
        i = int(0)
        k = []
        j = int(0)
        smps_num = 0
        chn_data=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
        while (i <= datalength ):
            #print (''.join('{:04x} '.format(x) for x in dataNtuple[i:i+pkg_len]) )
            data_a =  ((dataNtuple[i+0]<<16)&0x00FFFFFFFF) + (dataNtuple[i+1]& 0x00FFFFFFFF) + 0x0000000001
            data_b =  ((dataNtuple[i+0+pkg_len]<<16)&0x00FFFFFFFF) + (dataNtuple[i+1+pkg_len]& 0x00FFFFFFFF)
            acc_flg = ( data_a  == data_b )
            face_flg = ((dataNtuple[i+2+6] == 0xface) or (dataNtuple[i+2+6] == 0xfeed))
            #exit()

            if (face_flg == True ) and ( acc_flg == True ) :
                pkg_index.append(i)
                pkg_start = i
                i = i + pkg_len
                onepkgdata = dataNtuple[pkg_start : pkg_start + pkg_len]
                j = 8
                peak_len = 100
                while j < len(onepkgdata) :
                    if (onepkgdata[j] == 0xface ) or (onepkgdata[j] == 0xfeed ):
                        if  (onepkgdata[j] == 0xfeed ):
                            trg_flg = 0x1000 
                        else:
                            trg_flg = 0x0000 
                        chn_data[0].append( trg_flg + ((onepkgdata[j+1] & 0XFFF0)>>4) )
                        chn_data[1].append( trg_flg + ((onepkgdata[j+1] & 0XF)<<8) + ((onepkgdata[j+2] & 0XFF00)>>8) )
                        chn_data[2].append( trg_flg + ((onepkgdata[j+2] & 0XFF)<<4) + ((onepkgdata[j+3] & 0XF000)>>12) )
                        chn_data[3].append( trg_flg + ((onepkgdata[j+3] & 0XFFF)) )

                        chn_data[4].append( trg_flg + ((onepkgdata[j+4] & 0XFFF0)>>4) )
                        chn_data[5].append( trg_flg + ((onepkgdata[j+4] & 0XF)<<8) + ((onepkgdata[j+5] & 0XFF00)>>8) )
                        chn_data[6].append( trg_flg + ((onepkgdata[j+5] & 0XFF)<<4) + ((onepkgdata[j+6] & 0XF000)>>12) )
                        chn_data[7].append( trg_flg + ((onepkgdata[j+6] & 0XFFF)) )

                        chn_data[8].append( trg_flg + ((onepkgdata[j+7] & 0XFFF0)>>4) )
                        chn_data[9].append( trg_flg + ((onepkgdata[j+7] & 0XF)<<8) + ((onepkgdata[j+8] & 0XFF00)>>8) )
                        chn_data[10].append( trg_flg + ((onepkgdata[j+8] & 0XFF)<<4) + ((onepkgdata[j+9] & 0XF000)>>12) )
                        chn_data[11].append( trg_flg + ((onepkgdata[j+9] & 0XFFF)) )

                        chn_data[12].append( trg_flg + ((onepkgdata[j+10] & 0XFFF0)>>4) )
                        chn_data[13].append( trg_flg + ((onepkgdata[j+10] & 0XF)<<8) + ((onepkgdata[j+11] & 0XFF00)>>8) )
                        chn_data[14].append( trg_flg + ((onepkgdata[j+11] & 0XFF)<<4) + ((onepkgdata[j+12] & 0XF000)>>12) )
                        chn_data[15].append( trg_flg + ((onepkgdata[j+12] & 0XFFF)) )

#                        chn_data[7].append( trg_flg + ((onepkgdata[j+1] & 0X0FFF)<<0 ))
#                        chn_data[6].append( trg_flg + ((onepkgdata[j+2] & 0X00FF)<<4)+ ((onepkgdata[j+1] & 0XF000) >> 12))
#                        chn_data[5].append( trg_flg + ((onepkgdata[j+3] & 0X000F)<<8) +((onepkgdata[j+2] & 0XFF00) >> 8 ))
#                        chn_data[4].append( trg_flg + ((onepkgdata[j+3] & 0XFFF0)>>4 ))
#
#                        chn_data[3].append( trg_flg + (onepkgdata[ j+3+1] & 0X0FFF)<<0 )
#                        chn_data[2].append( trg_flg + ((onepkgdata[j+3+2] & 0X00FF)<<4) + ((onepkgdata[j+3+1] & 0XF000) >> 12))
#                        chn_data[1].append( trg_flg + ((onepkgdata[j+3+3] & 0X000F)<<8) + ((onepkgdata[j+3+2] & 0XFF00) >> 8 ))
#                        chn_data[0].append( trg_flg + ((onepkgdata[j+3+3] & 0XFFF0)>>4) )
#
#                        chn_data[15].append(trg_flg +  ((onepkgdata[j+6+1] & 0X0FFF)<<0 ))
#                        chn_data[14].append(trg_flg +  ((onepkgdata[j+6+2] & 0X00FF)<<4 )+ ((onepkgdata[j+6+1] & 0XF000) >> 12))
#                        chn_data[13].append(trg_flg +  ((onepkgdata[j+6+3] & 0X000F)<<8 )+ ((onepkgdata[j+6+2] & 0XFF00) >> 8 ))
#                        chn_data[12].append(trg_flg +  ((onepkgdata[j+6+3] & 0XFFF0)>>4 ))
#
#                        chn_data[11].append(trg_flg +  ((onepkgdata[j+9+1] & 0X0FFF)<<0 ))
#                        chn_data[10].append(trg_flg +  ((onepkgdata[j+9+2] & 0X00FF)<<4 )+ ((onepkgdata[j+9+1] & 0XF000) >> 12))
#                        chn_data[9].append( trg_flg +  ((onepkgdata[j+9+3] & 0X000F)<<8 )+ ((onepkgdata[j+9+2] & 0XFF00) >> 8 ))
#                        chn_data[8].append( trg_flg +  ((onepkgdata[j+9+3] & 0XFFF0)>>4 ))
                        if (onepkgdata[j] == 0xfeed ):
                            feed_loc.append(smps_num)
                        smps_num = smps_num + 1
                    else:
                        pass
                    j = j + 13
            else:
                #pass
                i = i + 1
                print("Wrong data at addr = {}".format(i))

        return data_rest, chn_data

    def __init__(self):
        self.jumbo_flag = False

COV = RAW_CONV ()
fdir = "D:/CM_FEMB/Rawdata/"
fdir = "D:/CM_FEMB/CEbox/"
fdir = "D:/CM_FEMB/Rawdata/"
fdir = "D:/CM_FEMB/APA_data/"
fdir = "D:/CM_FEMB/Rawdata/"
fdir = "D:/CM_FEMB/CEbox/"
fdir = "D:/CM_FEMB/Rawdata/"
for root, dirs, files in os.walk(fdir):
    break

#pattern = "CHK_LN_CM04_AM01_Toy04L21R_150pF_ADC_Test_Pattern"
#pattern = "Rawdata_12_28_2020_09_56_22_CHK_RT_CM08_AM07_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
#pattern =  "Rawdata_12_28_2020_10_32_49_CHK_LN_CM08_AM07_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_11_17_25_CHK_LN_CM15_AM02_ToyTPC04L21R_150pF_14_10_bl200_bufoff"
pattern =  "Rawdata_12_28_2020_11_48_59_CHK_LN_CM10_AM07_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08_reg41_8"
pattern =  "Rawdata_12_28_2020_11_51_06_CHK_LN_CM10_AM07_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08_reg41_6"
pattern =  "Rawdata_12_28_2020_13_05_58_CHK_LN_CM07_AM04_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08_extra_caps"
pattern =  "Rawdata_12_28_2020_13_38_58_CHK_LN_CM04_AM01_ToyTPC04L21R_150pF_14_10_bl900_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_13_38_17_CHK_LN_CM04_AM01_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_13_48_16_CHK_LN_CM04_AM01_ToyTPC04L21R_150pF_14_10_bl900_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_14_23_18_CHK_LN_CM05_AM08_ToyTPC04L21R_150pF_14_10_bl900_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_14_22_15_CHK_LN_CM05_AM08_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_14_45_58_CHK_RT_CM14_AM03_ToyTPC04L21R_150pF_14_10_bl900_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_14_57_39_CHK_LN_CM14_AM03_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_14_58_49_CHK_LN_CM14_AM03_ToyTPC04L21R_150pF_14_10_bl900_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_15_29_08_CHK_LN_CM09_AM05_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_15_55_50_CHK_LN_CM11_AM09_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_16_31_49_CHK_LN_CM12_AM10_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_07_44_14_CHK_LN_CM12_AM10_ToyTPC04L21R_150pF_14_05_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_07_52_02_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac12"
pattern =  "Rawdata_12_29_2020_08_39_30_CHK_LN_CM07_AM04_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_09_22_01_CHK_LN_CM13_AM09_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_14_36_20_APA40_CHK_14_10_asicdac08_bl200"
pattern =  "Rawdata_12_29_2020_16_34_13_APA40_slot023on_CHK_14_10_bl200_asicdac08"
pattern =  "Rawdata_12_29_2020_16_21_50_APA40_slot023on_RMS_14_10_bl200"
pattern =  "Rawdata_12_29_2020_16_24_32_APA40_slot023on_RMS_14_05_bl200"
pattern =  "Rawdata_12_29_2020_16_27_04_APA40_slot023on_RMS_14_20_bl200"
pattern =  "Rawdata_12_29_2020_16_30_21_APA40_slot023on_RMS_14_30_bl200"
pattern =  "Rawdata_12_30_2020_11_45_07_APA40_slot0123on_CALI_14_30_bl200_asicdac08"
pattern =  "Rawdata_12_29_2020_15_12_01_APA40_RMS_14_30_bl200"
pattern =  "Rawdata_12_29_2020_15_07_54_APA40_RMS_14_20_bl200"
pattern =  "Rawdata_12_29_2020_15_04_19_APA40_RMS_14_05_bl200"
pattern =  "Rawdata_12_29_2020_14_51_36_APA40_RMS_14_10_bl200"
pattern =  "Rawdata_12_31_2020_07_24_59_APA40_slot0123on_RMS_LN_14_10_bl200"
pattern =  "Rawdata_12_31_2020_07_29_25_APA40_slot0123on_RMS_LN_14_05_bl200"
pattern =  "Rawdata_12_31_2020_07_36_57_APA40_slot0123on_RMS_LN_14_30_bl200"
pattern =  "Rawdata_12_31_2020_07_33_30_APA40_slot0123on_RMS_LN_14_20_bl200"


pattern =  "Rawdata_12_31_2020_08_14_34_APA40_slot0on_CHK_LN_14_30_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_08_17_36_APA40_slot0on_CHK_LN_14_30_bl900_asicdac08"
pattern =  "Rawdata_12_31_2020_07_40_48_APA40_slot0123on_CHK_LN_14_30_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_07_43_52_APA40_slot0123on_CHK_LN_14_30_bl900_asicdac08"
pattern =  "Rawdata_12_31_2020_09_04_06_APA40_slot1on_CHK_LN_14_10_bl900_asicdac08_asic2ch1tsten"
pattern =  "Rawdata_12_29_2020_15_16_32_APA40_RMS_14_10_bl900"
pattern =  "Rawdata_12_30_2020_11_50_51_APA40_slot0123on_CALI_14_30_bl200_asicdac12"
pattern =  "Rawdata_12_30_2020_13_24_47_APA40_slot0123on_CALI_14_30_bl200_asicdac04"
pattern =  "Rawdata_12_31_2020_07_41_21_APA40_slot0123on_CALI_LN_14_30_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_08_01_23_APA40_slot0123on_RMS_LN_14_05_bl200"
pattern =  "Rawdata_12_31_2020_07_57_25_APA40_slot0123on_CALI_LN_14_30_bl200_asicdac04"
pattern =  "Rawdata_12_31_2020_07_52_29_APA40_slot0123on_CALI_LN_14_30_bl200_asicdac12"
pattern =  "Rawdata_12_31_2020_07_57_25_APA40_slot0123on_CALI_LN_14_30_bl200_asicdac04"
pattern =  "Rawdata_12_31_2020_11_35_40_APA40_slot0123on_CHK_LN_14_10_bl900_asicdac08"
pattern =  "Rawdata_12_31_2020_11_32_49_APA40_slot0123on_CHK_LN_14_10_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_11_25_01_APA40_onePScableon_RMS_LN_14_10_bl900_FEMB3"
pattern =  "Rawdata_12_31_2020_11_24_32_APA40_onePScableon_RMS_LN_14_10_bl200_FEMB3"
pattern =  "Rawdata_12_31_2020_11_23_46_APA40_onePScableon_CHK_LN_14_10_bl200_asicdac08_FEMB3"
pattern =  "Rawdata_12_31_2020_11_22_59_APA40_onePScableon_CHK_LN_14_10_bl900_asicdac08_FEMB3"
pattern =  "Rawdata_12_31_2020_11_20_54_APA40_onePScableon_CHK_LN_14_10_bl900_asicdac08_FEMB2"
pattern =  "Rawdata_12_31_2020_11_20_09_APA40_onePScableon_CHK_LN_14_10_bl200_asicdac08_FEMB2"
pattern =  "Rawdata_12_31_2020_11_19_18_APA40_onePScableon_RMS_LN_14_10_bl200_FEMB2"
pattern =  "Rawdata_12_31_2020_11_18_34_APA40_onePScableon_RMS_LN_14_10_bl900_FEMB2"
pattern =  "Rawdata_12_31_2020_11_13_26_APA40_onePScableon_CHK_LN_14_10_bl200_asicdac08_FEMB1"
pattern =  "Rawdata_12_31_2020_11_12_28_APA40_onePScableon_CHK_LN_14_10_bl900_asicdac08_FEMB1"
pattern =  "Rawdata_12_31_2020_11_08_10_APA40_onePScableon_RMS_LN_14_10_bl900_FEMB0"
pattern =  "Rawdata_12_31_2020_11_09_03_APA40_onePScableon_RMS_LN_14_10_bl200_FEMB0"
pattern =  "Rawdata_12_31_2020_11_10_42_APA40_onePScableon_RMS_LN_14_10_bl200_FEMB1"
pattern =  "Rawdata_12_31_2020_11_11_24_APA40_onePScableon_RMS_LN_14_10_bl900_FEMB1"
pattern =  "Rawdata_12_31_2020_11_05_55_APA40_onePScableon_CHK_LN_14_10_bl200_asicdac08_FEMB0"
pattern =  "Rawdata_12_31_2020_11_04_45_APA40_slot0on_CHK_LN_14_10_bl200_asicdac08_FEMB3"
pattern =  "Rawdata_12_31_2020_11_04_02_APA40_slot0on_CHK_LN_14_10_bl900_asicdac08_FEMB3"
pattern =  "Rawdata_12_31_2020_11_03_07_APA40_slot0on_RMS_LN_14_10_bl900_FEMB3"
pattern =  "Rawdata_12_31_2020_11_02_10_APA40_slot0on_RMS_LN_14_10_bl200_FEMB3"
pattern =  "Rawdata_12_31_2020_11_00_39_APA40_slot0on_RMS_LN_14_10_bl200_FEMB2"
pattern =  "Rawdata_12_31_2020_10_59_45_APA40_slot0on_RMS_LN_14_10_bl900_FEMB2"
pattern =  "Rawdata_12_31_2020_10_44_08_APA40_slot0123on_RMS_LN_14_10_bl900"
pattern =  "Rawdata_12_31_2020_10_40_46_APA40_slot0123on_RMS_LN_14_10_bl200"
pattern =  "Rawdata_12_31_2020_10_38_27_APA40_slot0123on_CHK_LN_14_10_bl900_asicdac08"
pattern =  "Rawdata_12_31_2020_10_36_11_APA40_slot0123on_CHK_LN_14_10_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_08_06_14_APA40_slot0on_RMS_LN_14_05_bl200_FEMB0"
pattern =  "Rawdata_12_31_2020_08_07_58_APA40_slot0on_RMS_LN_14_10_bl200_FEMB0"
pattern =  "Rawdata_12_31_2020_08_09_34_APA40_slot0on_RMS_LN_14_20_bl200_FEMB0"
pattern =  "Rawdata_12_31_2020_08_12_30_APA40_slot0on_RMS_LN_14_30_bl200_FEMB0"
pattern =  "Rawdata_12_31_2020_09_04_06_APA40_slot1on_CHK_LN_14_10_bl200_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_06_13_APA40_slot1on_CHK_LN_14_10_bl900_asicdac08_FEMB1"
pattern =  "Rawdata_12_31_2020_09_37_04_APA40_slot1on_CHK_LN_14_10_bl900_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_39_47_APA40_slot1on_CHK_LN_14_05_bl200_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_40_48_APA40_slot1on_CHK_LN_14_05_bl900_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_41_38_APA40_slot1on_CHK_LN_14_20_bl900_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_42_46_APA40_slot1on_CHK_LN_14_20_bl200_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_43_37_APA40_slot1on_CHK_LN_14_30_bl200_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_44_17_APA40_slot1on_CHK_LN_14_30_bl900_asicdac08_asic2ch1tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_50_34_APA40_slot1on_CHK_LN_14_10_bl900_asicdac08_asic7tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_51_43_APA40_slot1on_CHK_LN_14_10_bl200_asicdac08_asic7tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_53_26_APA40_slot1on_CHK_LN_14_10_bl900_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_54_24_APA40_slot1on_CHK_LN_14_20_bl900_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_55_14_APA40_slot1on_CHK_LN_14_20_bl200_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_56_07_APA40_slot1on_CHK_LN_14_10_bl200_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_57_26_APA40_slot1on_CHK_LN_47_10_bl900_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_58_13_APA40_slot1on_CHK_LN_78_10_bl900_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_09_59_19_APA40_slot1on_CHK_LN_25_10_bl900_asicdac08_asic7ch06tsten_FEMB1"
pattern =  "Rawdata_12_31_2020_10_35_31_APA40_slot0123on_CHK_LN_14_10_bl200_asicdac08_FEMB1"
pattern =  "Rawdata_12_31_2020_10_48_17_APA40_slot0on_CHK_LN_14_10_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_10_49_47_APA40_slot0on_CHK_LN_14_10_bl900_asicdac08_FEMB0"
pattern =  "Rawdata_12_31_2020_10_51_36_APA40_slot0on_RMS_LN_14_10_bl900"
pattern =  "Rawdata_12_31_2020_10_52_29_APA40_slot0on_RMS_LN_14_10_bl200"
pattern =  "Rawdata_12_31_2020_10_53_43_APA40_slot0on_RMS_LN_14_10_bl200"
pattern =  "Rawdata_12_31_2020_10_54_40_APA40_slot0on_RMS_LN_14_10_bl900"
pattern =  "Rawdata_12_31_2020_10_59_08_APA40_slot0on_CHK_LN_14_10_bl900_asicdac08_FEMB2"
pattern =  "Rawdata_12_31_2020_10_58_14_APA40_slot0on_CHK_LN_14_10_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_10_56_27_APA40_slot0on_CHK_LN_14_10_bl200_asicdac08"
pattern =  "Rawdata_12_31_2020_10_55_41_APA40_slot0on_CHK_LN_14_10_bl900_asicdac08"
pattern =  "FM12"
pattern =  "FM86"
pattern =  "CEbox_7_27"
pattern =  "FM3300"
pattern =  "FM3300_1"
pattern =  "Rawdata_01_05_2021_13_07_26_CEbox_FM12"
pattern =  "Rawdata_12_28_2020_10_59_41_CHK_RT_CM15_AM02_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_14_10_28_CHK_RT_CM05_AM08_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_11_38_00_CHK_RT_CM10_AM07_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_28_2020_13_28_08_CHK_RT_CM04_AM01_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "RT"
pattern =  "Rawdata_01_15_2021_13_08_37_APA40_LN_CHK_slot0123on_14_10_asic08_bl200"
pattern =  "Rawdata_01_15_2021_13_13_56_APA40_LN_RMS_slot0123on_14_10_bl200"
pattern =  "Rawdata_01_15_2021_13_17_37_APA40_LN_RMS_slot0123on_14_05_bl200"
pattern =  "Rawdata_01_15_2021_13_21_07_APA40_LN_RMS_slot0123on_14_10_bl200"
pattern =  "Rawdata_01_15_2021_13_32_14_APA40_LN_RMS_slot0123on_14_30_bl200"
#pattern =  "Rawdata_01_15_2021_13_37_03_APA40_LN_RMS_slot0123on_14_20_bl200"
#pattern =  "Rawdata_01_15_2021_13_39_25_APA40_LN_RMS_slot0123on_14_10_bl200"
pattern =  "Rawdata_01_15_2021_13_49_38_APA40_LN_CHK_slot0123on_14_10_bl900_ascidac08"
pattern =  "Rawdata_01_15_2021_13_55_05_APA40_LN_CHK_slot0123on_14_10_bl900_ascidac08"
pattern =  "Rawdata_01_15_2021_13_59_09_APA40_LN_CHK_slot0123on_14_10_bl200_ascidac08"
pattern =  "Rawdata_01_15_2021_14_07_56_APA40_LN_CHK_slot0123on_14_10_bl200_ascidac12"
pattern =  "Rawdata_01_15_2021_14_16_48_APA40_LN_RMS_slot0123on_14_10_bl200"
pattern =  "Rawdata_01_15_2021_14_19_35_APA40_LN_RMS_slot0123on_14_05_bl200"
pattern =  "Rawdata_01_15_2021_14_21_58_APA40_LN_RMS_slot0123on_14_20_bl200"
pattern =  "Rawdata_01_15_2021_14_24_55_APA40_LN_RMS_slot0123on_14_30_bl200"
pattern =  "Rawdata_12_28_2020_10_32_49_CHK_LN_CM08_AM07_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_25_2021_14_05_36_CHK_LN_CM08_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_25_2021_14_35_59_CHK_LN_CM07_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_25_2021_14_27_56_CHK_RT_CM07_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_07_54_22_CEbox_7_22_CM13_AM09"
pattern =  "Rawdata_01_26_2021_07_59_52_CEbox_7_6_CM11_AM04"
pattern =  "Rawdata_01_26_2021_08_03_50_CEbox_7_21_CM09_AM05"
pattern =  "Rawdata_01_26_2021_08_06_43_CEbox_7_16_CM12_AM10"
pattern =  "Rawdata_01_26_2021_09_49_50_CHK_RT_CM03_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_09_57_30_CHK_RT_CM03_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_10_00_30_CHK_LN_CM03_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_10_02_20_CHK_LN_CM03_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_10_03_56_CHK_LN_CM03_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_10_09_50_CHK_LN_CM03_AM06_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_01_26_2021_10_58_26_CEbox_7_16_CM03_AM06"
pattern =  "Rawdata_12_29_2020_08_06_24_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_05_bl900_bufoff_asicdac12"
pattern =  "Rawdata_12_29_2020_08_05_46_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_05_bl900_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_08_05_07_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_05_bl900_bufoff_asicdac04"
pattern =  "Rawdata_12_29_2020_07_54_31_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_20_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_07_53_32_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_20_bl200_bufoff_asicdac12"
pattern =  "Rawdata_12_29_2020_07_49_18_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_05_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_07_51_20_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac08"
pattern =  "Rawdata_12_29_2020_07_52_02_CALI_LN_CM12_AM10_ToyTPC04L21R_150pF_14_10_bl200_bufoff_asicdac12"
pattern =  "Rawdata_12_28_2020_16_21_22_CALI_RT_CM12_AM10_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac12"
pattern =  "Rawdata_12_28_2020_16_20_02_CALI_RT_CM12_AM10_NoToyTPC_0pF_14_10_bl200_bufoff_asicdac08"
pattern =  "CALI_LN_CM12_AM10_ToyTPC04L21R_150pF"
pattern =  "RMS_LN_CM12_AM10_ToyTPC04L21R_150pF"



for afile in files:
    if (pattern in afile)  and (".bin" in afile):
        fn = fdir + afile
        print(fn)
        fembno = int( afile[afile.find("FEMB")+4] )
        asicno = int( afile[afile.find("ASIC")+4] )
        fsize = (os.path.getsize(fn))
        slice_n = 100000
        tmp1 = afile.find(pattern)
        tmp2 = afile.find("_FEMB")
        hdf = fdir + afile[tmp1:tmp2] + ".h5"
        with h5py.File(hdf, "a") as f:
            with open(fn, "rb") as fp:
                for i in range((fsize//slice_n)-2):
                    if i == 0:
                        Rawdata = fp.read(slice_n)
                    else:
                        Rawdata = fp.read(slice_n)
                        Rawdata = data_rest + Rawdata

                    data_rest, chn_data= COV.raw_conv_feedloc(Rawdata)

                    if i == 0:
                        dset = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
                        for j in range(16):
                            dset[j] = f.create_dataset('CH{}'.format(fembno*128 + asicno*16 + j), (len(chn_data[j]),), maxshape=(None,), dtype='u2', chunks=True)
                            dset[j][:] = chn_data[j]
                    else:
                        for j in range(16):
                            ll = len(chn_data[j])
                            dset[j].resize(dset[j].shape[0]+ll, axis=0)
                            dset[j][-ll:] = chn_data[j]



#        fn = fdir + afile
#        fsize = (os.path.getsize(fn))
#        print (fsize)
#        with open(fn, "rb") as fp:
#            Rawdata = fp.read(fsize)
#            data_rest, chn_data= COV.raw_conv_feedloc(Rawdata)

#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches
#import matplotlib.mlab as mlab
#
#
#
#N = 500
#x = np.arange(N)*0.5
#for i in range(0,16,1):
#    y = chn_data[i][0:N]
#    plt.plot(x,y,label="{}".format(i))
##plt.plot(x,y,c = 'r')
##y = chn_data[15][0:N]
##plt.plot(x,y,c = 'b')
#plt.legend()
#plt.show()
#plt.close()

#        fn = fdir + afile
#        print(fn)
#        fsize = (os.path.getsize(fn))
#        slice_n = 10000000
#        hdf = fn[0:-4] + ".h5"
#        with h5py.File(hdf, "a") as f:
#            with open(fn, "rb") as fp:
#                for i in range((fsize//slice_n)-10):
#                #for i in range(3):
#                    if i == 0:
#                        Rawdata = fp.read(slice_n)
#                    else:
#                        Rawdata = fp.read(slice_n)
#                        Rawdata = data_rest + Rawdata
#
#                    data_rest, chn_data= COV.raw_conv_feedloc(Rawdata, fn)
#
#                    if i == 0:
#                        dset = f.create_dataset('CH0', (len(chn_data[0]),), maxshape=(None,), dtype='u2', chunks=True)
#                        dset[:] = chn_data[0]
#                        dset1 = f.create_dataset('CH1', (len(chn_data[1]),), maxshape=(None,), dtype='u2', chunks=True)
#                        dset1[:] = chn_data[1]
#                        dset13 = f.create_dataset('CH13', (len(chn_data[13]),), maxshape=(None,), dtype='u2', chunks=True)
#                        dset13[:] = chn_data[13]
#                    else:
#                        ll = len(chn_data[0])
#                        dset.resize(dset.shape[0]+ll, axis=0)
#                        dset[-ll:] = chn_data[0]
#                        dset1.resize(dset1.shape[0]+ll, axis=0)
#                        dset1[-ll:] = chn_data[1]
#                        dset13.resize(dset13.shape[0]+ll, axis=0)
#                        dset13[-ll:] = chn_data[13]
                #if i>2:
                #   break
   #break

#COV = RAW_CONV ()
#fdir = "D:/nEXO/Rawdata/"
#for root, dirs, files in os.walk(fdir):
#    break
#
#chn0 =[]
#chn1 =[]
#chn13 =[]
#
#for afile in files:
#    if ("92V_46V" in afile) and ("3900" in afile) and ("Rawdata_11_25" in afile) and (".bin" in afile ):
#        fn = fdir + afile
#        fsize = (os.path.getsize(fn))
#        slice_n = 10000000
#
#        with open(fn, "rb") as fp:
#            for i in range((fsize//slice_n)-10):
#                if i == 0:
#                    Rawdata = fp.read(slice_n)
#
#                else:
#                    Rawdata = fp.read(slice_n)
#                    Rawdata = data_rest + Rawdata
#                data_rest, chn_data= COV.raw_conv_feedloc(Rawdata, fn)
#                chn0 = chn0 + chn_data[0]
#                chn1 = chn1 + chn_data[1]
#                chn13 = chn13 + chn_data[13]
#                print (len(chn0))
#                if i>2:
#                    break
#
#
#fp = "D:/nEXO/Rawdata/Rawdata_11_25_2020_16_31_05_LED3900mV_14mVfC_1us_92V_46V.h5"
#f = h5py.File(fp, 'r')
#print (list(f.keys()))
#dset =f["CH0"]
#print (len(dset))
#for i in range(len(chn0)):
#    if chn0[i] != dset[i]:
#        print(chn0[i], dset[i], i)
#print (dset[0:100])
#print (chn0[0:100])
#dset1 =f["CH1"]
#print (dset1[0:100])
#dset13 =f["CH13"]
#print (dset13[0:100])
#import os
#import h5py
#import numpy as np
#path = "D:/nEXO/tmp/a.h5"
##f = h5py.File(path, 'r')
##print (list(f.keys()))
##dset =f[list(f.keys())[0]]
####print ((f.keys()))
###print ((dset.shape))
###print (len(dset))
##print ((dset[0:100]))
###print ((dset[100000:100100]))
##print ((dset[110000:110100]))
#
##os.remove(path)
#
##with h5py.File(path, "w") as f:
##    dset = f.create_dataset("mydataset", (100,), dtype='i')
##    dset = f.create_dataset('voltage284', (10**5,), maxshape=(None,),
##                            dtype='i8', chunks=(10**4,))
##dset = f.create_dataset('voltage284', (10**5,), maxshape=(None,),
##     dtype='u2', chunks=(10**4,))
#
#with h5py.File(path, "r") as f:
#    dset=f[list(f.keys())[0]]
#    print (dset.shape())
#with h5py.File(path, "a") as f:
#    a = (np.random.random(dset.shape))*10//1        
#    dset[:] = a
#    print (a[0:100])
#    print(dset.shape)
#    print(dset[0:100])
#    print(type(dset[0]))
#    # (100000,)
#
#    for i in range(3):
#        dset.resize(dset.shape[0]+10**4, axis=0)   
#        dset[-10**4:] = np.random.random(10**4)
#        dset[-10**4:] = np.random.random(10**4)
#        print(dset.shape)
#        # (110000,)
#        # (120000,)
#        # (130000,)



#fn = """D:/nEXO/Rawdata/Rawdata_11_25_2020_15_30_11_acc.bin"""
#with open(fn, "rb") as fp:
#    Rawdata = fp.read()

#COV.raw_conv_feedloc(Rawdata, fn)



#
#            if ( acc_flg == False ) :
#                j = j + 1
#
#        if ( len(k) != 0 ):
#            print ("raw_convertor.py: There are defective packages start at %d"%k[0] )
#        if j != 0 :
#            print ("raw_convertor.py: drop %d packages"%(j) )
#
#        tmpa = pkg_index[0]
#        tmpb = pkg_index[-1]
#        data_a = ((dataNtuple[tmpa+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpa+1]&0xFFFFFFFF)
#        data_b = ((dataNtuple[tmpb+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpb+1]&0xFFFFFFFF)
#        if ( data_b > data_a ):
#            pkg_sum = data_b - data_a + 1
#        else:
#            pkg_sum = (0x100000000 + data_b) - data_a + 1
#        missed_pkgs = 0
#        for i in range(len(pkg_index)-1):
#            tmpa = pkg_index[i]
#            tmpb = pkg_index[i+1]
#            data_a = ((dataNtuple[tmpa+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpa+1]&0xFFFFFFFF)
#            data_b = ((dataNtuple[tmpb+0]<<16)&0xFFFFFFFF) + (dataNtuple[tmpb+1]&0xFFFFFFFF)
#            if ( data_b > data_a ):
#                add1 = data_b - data_a
#            else:
#                add1 = (0x100000000 + data_b) - data_a
#            missed_pkgs = missed_pkgs + add1 -1
#
#        if (missed_pkgs > 0 ):
#            print ("raw_convertor.py: missing udp pkgs = %d, total pkgs = %d "%(missed_pkgs, pkg_sum) )
#            print ("raw_convertor.py: missing %.8f%% udp packages"%(100.0*missed_pkgs/pkg_sum) )
#        else:
#            pass
#
#        smps_num = 0
#        for onepkg_index in pkg_index:
#            onepkgdata = dataNtuple[onepkg_index : onepkg_index + pkg_len]
#            i = 8
#            peak_len = 100
#            while i < len(onepkgdata) :
#                if (onepkgdata[i] == 0xface ) or (onepkgdata[i] == 0xfeed ):
#                    chn_data[7].append( ((onepkgdata[i+1] & 0X0FFF)<<0 ))
#                    chn_data[6].append( ((onepkgdata[i+2] & 0X00FF)<<4)+ ((onepkgdata[i+1] & 0XF000) >> 12))
#                    chn_data[5].append( ((onepkgdata[i+3] & 0X000F)<<8) +((onepkgdata[i+2] & 0XFF00) >> 8 ))
#                    chn_data[4].append( ((onepkgdata[i+3] & 0XFFF0)>>4 ))
#
#                    chn_data[3].append( (onepkgdata[i+3+1] & 0X0FFF)<<0 )
#                    chn_data[2].append( ((onepkgdata[i+3+2] & 0X00FF)<<4) + ((onepkgdata[i+3+1] & 0XF000) >> 12))
#                    chn_data[1].append( ((onepkgdata[i+3+3] & 0X000F)<<8) + ((onepkgdata[i+3+2] & 0XFF00) >> 8 ))
#                    chn_data[0].append( ((onepkgdata[i+3+3] & 0XFFF0)>>4) )
#
#                    chn_data[15].append( ((onepkgdata[i+6+1] & 0X0FFF)<<0 ))
#                    chn_data[14].append( ((onepkgdata[i+6+2] & 0X00FF)<<4 )+ ((onepkgdata[i+6+1] & 0XF000) >> 12))
#                    chn_data[13].append( ((onepkgdata[i+6+3] & 0X000F)<<8 )+ ((onepkgdata[i+6+2] & 0XFF00) >> 8 ))
#                    chn_data[12].append( ((onepkgdata[i+6+3] & 0XFFF0)>>4 ))
#
#                    chn_data[11].append( ((onepkgdata[i+9+1] & 0X0FFF)<<0 ))
#                    chn_data[10].append( ((onepkgdata[i+9+2] & 0X00FF)<<4 )+ ((onepkgdata[i+9+1] & 0XF000) >> 12))
#                    chn_data[9].append(  ((onepkgdata[i+9+3] & 0X000F)<<8 )+ ((onepkgdata[i+9+2] & 0XFF00) >> 8 ))
#                    chn_data[8].append(  ((onepkgdata[i+9+3] & 0XFFF0)>>4 ))
#                    if (onepkgdata[i] == 0xfeed ):
#                        feed_loc.append(smps_num)
#                    smps_num = smps_num + 1
#                else:
#                    pass
#                i = i + 13
#        for chn in [0, 1, 15]:
#            fchn = fn[0:-4] + "_chn{}".format(chn) + ".csv"
#            with open(fchn, 'w+') as fw:
#                for x in chn_data[chn]:
#                    fw.write("{},\n".format(x))

#        return chn_data, feed_loc

#    def raw_conv(self, raw_data):
#        chn_data, feed_loc = self.raw_conv_feedloc(raw_data)
#        return chn_data
#
#    def raw_conv_peak(self, raw_data):
#        chn_data, feed_loc = self.raw_conv_feedloc(raw_data)
#        if ( len(feed_loc)  ) > 2 :
#            chn_peakp=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
#            chn_peakn=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
#            for tmp in range(len(feed_loc)-1):
#                for chn in range(16):
#                    chn_peakp[chn].append ( np.max(chn_data[chn][feed_loc[ tmp]:feed_loc[tmp]+100 ]) )
#                    chn_peakn[chn].append ( np.min(chn_data[chn][feed_loc[ tmp]:feed_loc[tmp]+100 ]) )
#        else:
#            chn_peakp = None
#            chn_peakn = None
#        return  chn_data, feed_loc, chn_peakp, chn_peakn
#

#fn = '/Users/shanshangao/Documents/tmp/nEXO/Rawdata_10_02_2020_16_39_15_test_photon_47mVfC_1us.bin'
##fn = '/Users/shanshangao/Documents/tmp/nEXO/Rawdata_10_02_2020_16_48_11_test_ASICDAC0x13_47mVfC_1us.bin'
##fn = '/Users/shanshangao/Documents/tmp/nEXO/Rawdata_10_02_2020_16_41_46_test_dark_47mVfC_1us.bin'
#
#with open(fn, "rb") as fp:
#    Rawdata = fp.read()
#
#chn_data = COV.raw_conv(Rawdata)
#print (len(chn_data[0]))
#
##chn = 0
#for chn in [0, 1, 15]:
#    fchn = fn[0:-4] + "_chn{}".format(chn) + ".csv"
#    with open(fchn, 'w+') as fw:
#        for x in chn_data[chn]:
#            fw.write("{},\n".format(x))

#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#import matplotlib.patches as mpatches
#import matplotlib.mlab as mlab
#
#
#
#N = 100000
#x = np.arange(N)*0.5
#y = chn_data[1][0:N]
#plt.plot(x,y,c = 'r')
#y = chn_data[15][0:N]
#plt.plot(x,y,c = 'b')
#plt.show()
#plt.close()




