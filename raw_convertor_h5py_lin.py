# -*- coding: utf-8 -*-
"""
File Name: init_femb.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description:
Created Time: 7/15/2016 11:47:39 AM
Last modified: 10/31/2021 8:02:58 AM
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
        data_err = False 
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
                data_err = True
                break

        return data_rest, chn_data, data_err

    def __init__(self):
        self.jumbo_flag = False

COV = RAW_CONV ()
#fdir = "D:/CM_FEMB_P3/Rawdata/"
#fdir = "D:/CM_FEMB_P2/Rawdata040921/"
fdir = "D:/Monolithic_FEMB/Rawdata3/"
for root, dirs, files in os.walk(fdir):
    break

#pattern = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1430_RMS"
#pattern = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_CHK_ADAC0x28"
#pattern = "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1410_CHK_ADAC0x20_S16ON"

ps = [
#       "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_S16ON_xtalk_chip3che",
#       "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1430_S16ON_xtalk_chip3chf",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEON_500pA_200BL1420_S16ON_lin1mV100mVoft_chip3ch1",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch5",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch6",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch7",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch8",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3ch9",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3cha",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3chb",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3chc",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3chd",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3che",
#        "RT_000pF_BRD01_CDP3_ADCP2DIFF_FEP5DIFF_500pA_200BL1420_S16ON_lin_chip3chf",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHd",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHe",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHf",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHa",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHb",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHf",
#        "RT_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CHd",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH2",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH3",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH4",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH5",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH6",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH7",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH9",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHa",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHb",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHc",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHd",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHe",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CHf",


        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip3CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip0CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip0CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip0CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip0CH9",
#
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip1CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip1CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip1CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip1CH9",
#
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip2CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip2CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip2CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip2CH9",
#
#
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip4CH9",
#
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip5CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip5CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip5CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip5CH9",
#
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip6CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip6CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip6CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip6CH9",
#
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip7CH0",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip7CH1",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip7CH8",
#        "LN_000pF_BRD01_CDP3_ADCP2SEOFF_FEP5SEOFF_500pA_200BL1420_S16ON_lin_chip7CH9",

      ]

for pattern in ps:
    for afile in files:
        if (pattern in afile)  and (".bin" in afile) and ("mV.bin" not in afile):
            fn = fdir + afile
            print(fn)
            fembno = int( afile[afile.find("FEMB")+4] )
            asicno = int( afile[afile.find("ASIC")+4] )
            #amp= int( afile[afile.find("AMP")+3: afile.find("AMP")+6] )
            amp= (int( afile[afile.find("AMP")+3: afile.find("AMP")+6] )) * 10 + int( afile[afile.find("AMP")+8] )
            fsize = (os.path.getsize(fn))
            slice_n = 100000
            tmp1 = afile.find(pattern)
            tmp2 = afile.find("_FEMB")
            hdf = fdir + afile[tmp1:tmp2] + "_mV.h5"
            #if asicno <= 5:
            #if True:
            if amp != 1000:
                with h5py.File(hdf, "a") as f:
                    with open(fn, "rb") as fp:
                        for i in range((fsize//slice_n)-2):
                            if i == 0:
                                Rawdata = fp.read(slice_n)
                            else:
                                Rawdata = fp.read(slice_n)
                                Rawdata = data_rest + Rawdata
    
                            data_rest, chn_data, data_err= COV.raw_conv_feedloc(Rawdata)
    
                            if not data_err:
                                if i == 0:
                                    dset = [ [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
                                    for j in range(16):
                                        dset[j] = f.create_dataset('CH{:03d}AMP{:03d}'.format(fembno*128 + asicno*16 + j, amp), (len(chn_data[j]),), maxshape=(None,), dtype='u2', chunks=True)
                                        dset[j][:] = chn_data[j]
                                else:
                                    for j in range(16):
                                        ll = len(chn_data[j])
                                        dset[j].resize(dset[j].shape[0]+ll, axis=0)
                                        dset[j][-ll:] = chn_data[j]
                            else:
                                break



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




