# -*- coding: utf-8 -*-
"""
File Name: cls_udp.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:52:43 PM
Last modified: 5/5/2022 1:08:46 PM
"""

from tcp import TCPSocket
from fe_asic_reg_mapping import FE_ASIC_REG_MAPPING
import time
import struct
import numpy as np
import copy

class TCP_CFG(TCPSocket, FE_ASIC_REG_MAPPING ):
    def __init__(self):
        super().__init__()
        self.adcs_paras = [ # c_id, diff_en, sdc_en, vrefp, vrefn, vcmo, vcmi
                            [0x4, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0x5, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0x6, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0x7, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0x8, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0x9, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0xA, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                            [0xB, 0, 0, 0xDF, 0x33, 0x89, 0x67],
                          ]

    def wib_ww (self, addr = 0, data = 1): #data=1, disable HS DATA
        self.tcp_poke(addr, data)

    def wib_cntl_cs (self, lemo_en = False, reg_cntls = (0,0,0,0) ): 
        if lemo_en == True:
            self.tcp_poke(addr=0x16, data=0x00)
        else:
            wrdata = 0x01
            for i in range(4):
                wrdata = ((reg_cntls[i]&0x01)<<(i+4)) | wrdata
            self.tcp_poke(addr=0x16, data=wrdata)

    def cd_fc_rst (self ): 
        self.femb_cd_fc(fc_cmd = 0)
    def cd_fc_act (self ): 
        self.femb_cd_fc(fc_cmd = 1)
    def cd_fc_alert (self ): 
        self.femb_cd_fc(fc_cmd = 2)
    def cd_fc_edge (self ): 
        self.femb_cd_fc(fc_cmd = 3)
    def cd_fc_sync (self ): 
        self.femb_cd_fc(fc_cmd = 4)
    def cd_fc_cd_adc_sync (self ): 
        self.femb_cd_fc(fc_cmd = 5)

    def adc_sync_rst (self ): 
        self.femb_cd_wr(c_id=3, c_page=0, c_addr = 0x20, c_data = 5)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr = 0x20, c_data = 5)
        self.cd_fc_cd_adc_sync( ) 

    def femb_wr_chk (self,c_id, c_page, c_addr, c_data ): 
        self.femb_cd_wr(c_id, c_page, c_addr, c_data)
        c_rd = self.femb_cd_rd(c_id, c_page, c_addr)
        if c_data == c_rd[0]:
            pass
        else:
            print ("WR != RD. CHIP_ID=0x{:X}, PAGE=0x{:X}, ADDR=0x{:X}, WRDATA=0x{:X}, RD=0x{:X}".format(c_id, c_page, c_addr, c_data, c_rd[0]))

    def cd_8b10_p0r3_cfg (self ):
        self.femb_wr_chk (c_id=3, c_page=0, c_addr = 0x3, c_data = 0x3c)
        self.femb_wr_chk (c_id=2, c_page=0, c_addr = 0x3, c_data = 0x3c)

    def cd_lvds_current (self ):
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x11, c_data=0x07)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x11, c_data=0x07)
        self.femb_wr_chk (c_id=3, c_page=0, c_addr = 0x11, c_data = 0x07)
        self.femb_wr_chk (c_id=2, c_page=0, c_addr = 0x11, c_data = 0x07)


    def adc_cfg (self, adc_no):
        c_id    = self.adcs_paras[adc_no][0]
        diff_en = self.adcs_paras[adc_no][1] 
        sdc_en  = self.adcs_paras[adc_no][2] 
        vrefp   = self.adcs_paras[adc_no][3] 
        vrefn   = self.adcs_paras[adc_no][4]  
        vcmo    = self.adcs_paras[adc_no][5] 
        vcmi    = self.adcs_paras[adc_no][6] 
        self.femb_wr_chk(c_id,c_page=2, c_addr=1, c_data=0x0c) #start_data
        self.femb_wr_chk(c_id,c_page=1, c_addr=0x89, c_data=0x08) #offset_binary_output_data_format
        if diff_en == 0:
            self.femb_wr_chk(c_id,c_page=1, c_addr=0x84, c_data=0x3b) #SE input mode

        if sdc_en == 0:
            self.femb_wr_chk(c_id,c_page=1, c_addr=0x80, c_data=0x23) #SDC bypassed
        else:
            self.femb_wr_chk(c_id,c_page=1, c_addr=0x80, c_data=0x62) #SDC enabled

        self.femb_wr_chk(c_id,c_page=1, c_addr=0x98, c_data=vrefp) #vrefp self.femb_wr_chk(c_id,c_page=1, c_addr=0x99, c_data=vrefn) #vrefn
        self.femb_wr_chk(c_id,c_page=1, c_addr=0x9a, c_data=vcmo) #vrefn
        self.femb_wr_chk(c_id,c_page=1, c_addr=0x9b, c_data=vcmi) #vrefn

        ###auto calibration
        ##self.femb_wr_chk(c_id,c_page=1, c_addr=0x9f, c_data=0) 
        ##time.sleep(0.01)
        ##self.femb_wr_chk(c_id,c_page=1, c_addr=0x9f, c_data=0x03) 
        ##self.femb_wr_chk(c_id,c_page=1, c_addr=0x9f, c_data=0x03) 
        ##time.sleep(0.5)
        ##self.femb_wr_chk(c_id,c_page=1, c_addr=0x9f, c_data=0) 

    def fc_act_cal(self):
        self.femb_cd_wr(c_id=3, c_page=0, c_addr = 0x20, c_data = 1)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr = 0x20, c_data = 1)
        self.cd_fc_act ( ) 

    def fc_act_rst_larasic(self):
        self.femb_cd_wr(c_id=3, c_page=0, c_addr = 0x20, c_data = 6)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr = 0x20, c_data = 6)
        time.sleep(0.01)
        self.cd_fc_act ( ) 

    def fc_act_status(self):
        self.femb_cd_wr(c_id=3, c_page=0, c_addr = 0x20, c_data = 3)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr = 0x20, c_data = 3)
        time.sleep(0.01)
        self.cd_fc_act ( ) 
        sts_cd1 = self.femb_cd_rd(c_id=3, c_page=0, c_addr=0x24)
        sts_cd2 = self.femb_cd_rd(c_id=2, c_page=0, c_addr=0x24)
        return sts_cd1[0], sts_cd2[0]

    def fc_act_spi(self):
        self.femb_cd_wr(c_id=3, c_page=0, c_addr = 0x20, c_data = 8)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr = 0x20, c_data = 8)
        time.sleep(0.01)
        self.cd_fc_act ( ) 

    def fe_spi_prog(self):
#        self.link_cs = 0x0
        while True:
            for chip in range(8):
                for reg_id in range(16+2):
                    if (chip < 4):
                        self.femb_wr_chk(c_id=3, c_page=(chip%4+1), c_addr =(0x91-reg_id), c_data = self.regs_int8[chip][reg_id] )
                    else:
                        self.femb_wr_chk(c_id=2, c_page=(chip%4+1), c_addr =(0x91-reg_id), c_data = self.regs_int8[chip][reg_id] )

            time.sleep(0.01)
            self.fc_act_spi()
            sts_cd1, sts_cd2 = self.fc_act_status()
            if (sts_cd1&0xff == 0xff) and (sts_cd2&0xff == 0xff):
                break
#        self.femb_wr_chk(c_id=3, c_page=0, c_addr = 0x20, c_data = 8) # WIB
#        self.femb_wr_chk(c_id=2, c_page=0, c_addr = 0x20, c_data = 8) # WIB
#        time.sleep(0.01)
#        self.cd_fc_act ( ) 

    def cd_fe_cali(self, phase0x07=[0,0,0,0,0,0,0,0]):
        #default, 500sample per pulse, falling-edge to rising = 50 samples
        for i in range(8):
            self.femb_wr_chk(c_id=3-(i//4), c_page=1+(i%4), c_addr = 0x6, c_data = 0x30) #WIB
            self.femb_wr_chk(c_id=3-(i//4), c_page=1+(i%4), c_addr = 0x7, c_data = phase0x07[i]) #WIB
            self.femb_wr_chk(c_id=3-(i//4), c_page=1+(i%4), c_addr = 0x8, c_data = 0x38) #WIB
            self.femb_wr_chk(c_id=3-(i//4), c_page=1+(i%4), c_addr = 0x9, c_data = 0x80) #WIB
#        self.fc_act_cal()

#        self.femb_wr_chk(c_id=2, c_page=1, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=2, c_page=1, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=2, c_page=1, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=2, c_page=1, c_addr = 0x9, c_data = 0x80) #WIB
#        
#        self.femb_wr_chk(c_id=2, c_page=2, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=2, c_page=2, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=2, c_page=2, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=2, c_page=2, c_addr = 0x9, c_data = 0x80) #WIB
#
#        self.femb_wr_chk(c_id=2, c_page=3, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=2, c_page=3, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=2, c_page=3, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=2, c_page=3, c_addr = 0x9, c_data = 0x80) #WIB
#
#        self.femb_wr_chk(c_id=2, c_page=4, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=2, c_page=4, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=2, c_page=4, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=2, c_page=4, c_addr = 0x9, c_data = 0x80) #WIB
#
#        self.femb_wr_chk(c_id=3, c_page=1, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=3, c_page=1, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=3, c_page=1, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=3, c_page=1, c_addr = 0x9, c_data = 0x80) #WIB
#
#        self.femb_wr_chk(c_id=3, c_page=2, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=3, c_page=2, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=3, c_page=2, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=3, c_page=2, c_addr = 0x9, c_data = 0x80) #WIB
#
#        self.femb_wr_chk(c_id=3, c_page=3, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=3, c_page=3, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=3, c_page=3, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=3, c_page=3, c_addr = 0x9, c_data = 0x80) #WIB
#
#        self.femb_wr_chk(c_id=3, c_page=4, c_addr = 0x6, c_data = 0x30) #WIB
#        self.femb_wr_chk(c_id=3, c_page=4, c_addr = 0x7, c_data = 0x00) #WIB
#        self.femb_wr_chk(c_id=3, c_page=4, c_addr = 0x8, c_data = 0x38) #WIB
#        self.femb_wr_chk(c_id=3, c_page=4, c_addr = 0x9, c_data = 0x80) #WIB
#
#        #self.link_cs = 0x0


    def wib_mon_adc_read(self):
        self.tcp_poke(addr=0x11, data=0x01)
        time.sleep(0.01)
        self.tcp_poke(addr=0x11, data=0x00)

        adc0_1_v = self.tcp_peek(addr=0x13)
        adc0_v = ((adc0_1_v >>16)&0xffff)*2048/16384.0
        adc1_v = (adc0_1_v&0xffff)*2048/16384.0

        adc2_3_v = self.tcp_peek(addr=0x14)
        adc2_v = ((adc2_3_v >>16)&0xffff)*2048/16384.0
        adc3_v = (adc2_3_v&0xffff)*2048/16384.0

#        print (adc0_v, adc1_v, adc2_v, adc3_v)
        return adc0_v, adc1_v, adc2_v, adc3_v

    def wib_mon_adc_avg(self, femb_no=0, avg_n=10):
        tmp =[]
        for i in range(avg_n+2): #get rid of the first and second ADC data
            tmp1 = self.wib_mon_adc_read()[femb_no]
            if i>=2:
                tmp.append(tmp1)
        mon_mean =np.mean(tmp) 
        mon_std =np.std(tmp) 
        print ("WIB ADC monitor for FEMB{}: mean={}, std={}".format(femb_no, mon_mean, mon_std))
        return mon_mean, mon_std

    def femb_fedac_mon_cs(self, femb_no=0, ext_lemo=0, rst_fe=0, mon_chip=0, sgp=False, sg0=0, sg1=0,  vdac=0x20, avg_n=50 ):
        self.link_cs = 2*femb_no

        if (rst_fe != 0):
            self.set_fe_reset()

        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x0)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)

        fe_reg_tmp = copy.deepcopy(self.REGS)
        self.set_fe_reset()
        self.set_fe_board(sg0=sg0, sg1=sg1, sgp=sgp)
        self.set_fechip_global(chip=mon_chip&0x07, swdac=3, dac=vdac)
        for i in range (len(self.REGS)):
            self.REGS[i] = self.REGS[i] | fe_reg_tmp[i]
        self.set_fe_sync()
        self.fe_spi_prog()

        if ext_lemo == 0: #WIB on-board adc monitor
            time.sleep(1)
            vmon = self.wib_mon_adc_avg(femb_no=femb_no, avg_n=avg_n)
            self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x2)
            self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)
            return vmon 

#    def femb_mon_gnd_oft(self, femb_no=0, ext_lemo=0, avg_n=50 ):
#        if ext_lemo == 0: #WIB on-board adc monitor
#            self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x2)
#            self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)
#            time.sleep(1)
#            vmon = self.wib_mon_adc_avg(femb_no=femb_no, avg_n=avg_n)
#            self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x2)
#            self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)
#            return vmon

    def femb_fe_mon_cs(self, femb_no=0, ext_lemo=0, rst_fe=0, mon_type=2, mon_chip=0, mon_chipchn=0, snc=0,sg0=0, sg1=0, avg_n=50 ):
        self.link_cs = 2*femb_no

        if (rst_fe != 0):
            self.set_fe_reset()

        if (mon_type==2): #monitor bandgap 
            stb0=1
            stb1=1
            chn=0
        elif (mon_type==1): #monitor temperature
            stb0=1
            stb1=0
            chn=0
        else: #monitor analog
            stb0=0
            stb1=0
            chn=mon_chipchn

        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x0)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)

        fe_reg_tmp = copy.deepcopy(self.REGS)
        self.set_fe_reset()
        self.set_fechn_reg(chip=mon_chip&0x07, chn=chn, snc=snc, sg0=sg0, sg1=sg1, smn=1, sdf=1)
        self.set_fechip_global(chip=mon_chip&0x07, stb1=stb1, stb=stb0)
        for i in range (len(self.REGS)):
            self.REGS[i] = self.REGS[i] | fe_reg_tmp[i]
        self.set_fe_sync()
        self.fe_spi_prog()


        if ext_lemo == 0: #WIB on-board adc monitor
            time.sleep(0.5)
            vmon = self.wib_mon_adc_avg(femb_no=femb_no, avg_n=avg_n)
            self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x2)
            self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)
            return vmon 
            
    def femb_adc_mon_cs(self, femb_no=0, ext_lemo=0,adc_no=0, avg_n=10):
        self.link_cs = 2*femb_no

        adcs_addr=[0x08,0x09,0x0A,0x0B,0x04,0x05,0x06,0x07]  
        cd2_iobit432 = [6,4,5,7,3,1,0,2]
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x4) #ADC monitoring
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=cd2_iobit432[adc_no]<<2)

        if ext_lemo == 0: #WIB on-board adc monitor
            vmons = []
            for i in range(8):
                vrefp   = self.adcs_paras[i][3] 
                vrefn   = self.adcs_paras[i][4]  
                vcmo    = self.adcs_paras[i][5] 
                vcmi    = self.adcs_paras[i][6] 
                self.femb_wr_chk(c_id=adcs_addr[adc_no], c_page=1, c_addr=0x98, c_data=vrefp) #vrefp
                self.femb_wr_chk(c_id=adcs_addr[adc_no], c_page=1, c_addr=0x99, c_data=vrefn) #vrefn
                self.femb_wr_chk(c_id=adcs_addr[adc_no], c_page=1, c_addr=0x9a, c_data=vcmo) #vcmo
                self.femb_wr_chk(c_id=adcs_addr[adc_no], c_page=1, c_addr=0x9b, c_data=vcmi) #vcmi
                self.femb_cd_wr(c_id=adcs_addr[adc_no], c_page=1, c_addr=0xaf, c_data=(i<<2)|0x01)
                time.sleep(1)
                vmon = self.wib_mon_adc_avg(femb_no=femb_no, avg_n=avg_n)
                vmons.append(vmon)
            self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x2)
            self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)
            return vmons, "CMOS Ref: VREFP=0x{:02x}, VREFN=0x{:02x}, VCMO=0x{:02x}, VCMI=0x{:02x}".format(vrefp, vrefn, vcmo, vcmi)

    def femb_cfg (self):
        self.wib_ww(addr=0, data=0x1)
        self.wib_cntl_cs(lemo_en = False, reg_cntls = (0,0,0,0) ) 
        print ("COLDATA CFG ongoing...")
        self.cd_fc_rst()
        time.sleep(0.05)
        self.cd_fc_rst()
        time.sleep(0.05)
        self.cd_lvds_current ()
        self.cd_8b10_p0r3_cfg()
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x27, c_data=0x1f)
        self.femb_cd_wr(c_id=3, c_page=0, c_addr=0x26, c_data=0x2) #tie LArASIC test pin to ground
        self.femb_cd_wr(c_id=2, c_page=0, c_addr=0x26, c_data=0x0)
        print ("COLDADC SYNC RESET...")
        self.adc_sync_rst()
        print ("COLDADC CFG ongoing...")
        self.adc_cfg( adc_no=0)
        self.adc_cfg( adc_no=1)
        self.adc_cfg( adc_no=2)
        self.adc_cfg( adc_no=3)
        self.adc_cfg( adc_no=4)
        self.adc_cfg( adc_no=5)
        self.adc_cfg( adc_no=6)
        self.adc_cfg( adc_no=7)

        self.fc_act_rst_larasic()
        time.sleep(0.1)
        print ("LArASIC CFG ongoing...")
        self.fe_spi_prog()
        time.sleep(0.01)
        self.wib_ww(addr=0, data=0x0)
        time.sleep(0.01)
        self.wib_ww(addr=0, data=0x1)
        self.wib_ww(addr=0, data=0x0)

    def femb_pwr_set (self,femb=0, pwr_on=1, v_fe=3.0, v_adc=3.5, v_cd=2.8 ):
        self.tcp_cmd_io(cmd=0x0E, aux=femb, addr=0x0, data=int(v_fe/1e-7) )
        self.tcp_cmd_io(cmd=0x0E, aux=femb, addr=0x3, data=int(0/1e-7) )
        self.tcp_cmd_io(cmd=0x0E, aux=femb, addr=0x2, data=int(v_adc/1e-7) )
        self.tcp_cmd_io(cmd=0x0E, aux=femb, addr=0x1, data=int(v_cd/1e-7) )
        self.tcp_cmd_io(cmd=0x0E, aux=femb, addr=0x4, data=int(0/1e-7) )
        self.tcp_cmd_io(cmd=0x0E, aux=femb, addr=0x5, data=int(0/1e-7) )
        if pwr_on != 0:
            self.tcp_cmd_io(cmd=0x0C, aux=femb, addr=0x0, data= 1)
            time.sleep(2)
            print ("FEMB{} is turned on.".format(femb))
        else:
            self.tcp_cmd_io(cmd=0x0C, aux=femb, addr=0x0, data= 0)

    def femb_pwr_rd (self,femb=0, avg_n=5 ):
        c_s = []
        v_s = []
        for avgi in range(avg_n+1):
            if (avgi>=1):
                rd = self.tcp_rd_blk(cmd=0x0F, aux=femb, addr = 0) 
                rd_len = len(rd)
                dataNtuple = struct.unpack_from(">%dB"%(rd_len),rd)
                d_even = dataNtuple[::2]
                d_odd = dataNtuple[1::2]
                nd = []
                for i in range(len(d_even)):
                    nd.append( (d_even[i]<<8) + d_odd[i])
                c_info = nd[3:3+7]
                c_info = ((np.array(c_info)&0x3fff)*1.9075E-5)/0.1
                c_info[2] = ((c_info[2]*0.1)/0.01)/1.238
                for i in range(len(c_info)):
                    if c_info[i] >= 3.12:
                        c_info[i] = 0
                v_info = nd[10:10+7]
                v_info = (np.array(v_info)&0x3fff)*0.00030518
                if (avgi==1):
                    c_s = c_info
                    v_s = v_info
                else:
                    c_s =c_s+ c_info
                    v_s =v_s+ v_info
        c_info = c_s/avg_n
        v_info = v_s/avg_n

        return (v_info[0], c_info[0]), (v_info[2], c_info[2]), (v_info[1], c_info[1]), (v_info[6], c_info[6])


