# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:15:50 2021

@author: dell
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 15:56:47 2021


"""

import sys
import time
import pyvisa as visa
from pyvisa import VisaIOError
from datetime import datetime

class TDM_CTL:
    def status_chk(self, cmd_str):
        sta_chk = self.tdm.query("SYST:ERR?")
        if (str(sta_chk[0:2]) == "+0" ):
            pass
        else:
            print (sta_chk)
            while 1:
                print ("tdm Error! Exit Manually")
                time.sleep(50)
                cmd_str = "SYST:COMM:LAN:KEEP 1000E+03"
                self.tdm.write(cmd_str)
                self.status_chk(cmd_str)
    def tdm_init(self):
        rm = visa.ResourceManager()
        rm_list = rm.list_resources()
        try:
            rm_list.index(self.ADDR)
            print ("Teledyne T3DMM6-5 DMM (%s) is locacted"%self.ADDR)
        except ValueError:
            print ("Teledyne T3DMM6-5 DMM (%s) is not found, Please check!"%self.ADDR)
            print ("Exit anyway!")
            sys.exit()
        try:
            tdm = rm.open_resource(self.ADDR)
            init_chk = tdm.query("SYST:ERR?")
            if (str(init_chk[0:2]) == "+0" ):
                pass
            else:
                print (init_chk)
                print ("Init TDM Error! Exit anyway")
                sys.exit()
        except VisaIOError:
            print ("Teledyne Initialize--> Exact system name not found")
            print ("Exit anyway!")
            sys.exit()
        self.tdm = tdm
       
    def tdm_on(self):
        #cmd_str = 'SYST:LFR F{}Hz'.format(sysflt)
        #self.tdm.write(cmd_str)
        #self.status_chk(cmd_str)

        cmd_str = "CONF:VOLT:DC 20"
        self.tdm.write(cmd_str)
        self.status_chk(cmd_str)
        cmd_str = "VOLT:DC:NPLC 100"
        self.tdm.write(cmd_str)
        self.status_chk(cmd_str)

       
    def tdm_reset(self):
        cmd_str = "*RST"
        self.tdm.write(cmd_str)
       
    def tdm_abort(self):
        cmd_str = "ABOR"
        self.tdm.write(cmd_str)
       
    def tdm_meas(self):
        timestampe =  datetime.now().strftime('%m%d%Y_%H%M%S')
        cmd_str = "MEAS:VOLT:DC? 20"
        m_volt = float(self.tdm.query(cmd_str))
        self.status_chk(cmd_str)
        #print "{}, smu ChN{}, Volt={}, Curr={}".format(timestampe, chn, m_volt, m_curr)

        return  timestampe, m_volt

    #__INIT__#
    def __init__(self):
        self.ADDR = u'USB0::0xF4EC::0xEE38::T0105C20190045::0::INSTR'
        self.tdm = None
#a = TDM_CTL()
#a.tdm_init()    
        #USB\VID_F4EC&PID_EE38\T0105C20190045