# -*- coding: utf-8 -*-
"""
File Name: cls_udp.py
Author: GSS
Mail: gao.hillhill@gmail.com
Description: 
Created Time: 3/20/2019 4:52:43 PM
Last modified: 4/29/2022 2:50:39 PM
"""

import socket
import time
import struct

class TCPSocket:
    def __init__(self, sock=None):
        super().__init__()
        self.host = "192.168.121.1"
        self.port = 32010
        self.SYSKEY=0xdeadbeef
        self.link_cs = 0 #femb0 = 0, femb1=2, femb2=4, femb3 = 8
        self.longcable=0

    def create(self):
        sock = None
        if sock is None:
            try:
                self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            except socket.error:
                print('Failed to create socket')
                sys.exit()
        else:
            self.sock = sock

    def connect(self):
        while True:
            try:
                self.sock.connect((self.host, self.port))
                break
            except OSError as err:
                print ("connect:", err)
                self.close()
                print ("Wait 5 seconds")
                time.sleep(5)
                self.create()

    def close(self):
        while True:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError as err:
                print ("shutdown:", err)
            try:
                self.sock.close()
                break
            except OSError as err:
                print ("close:", err)

    def tcpsend(self, msg):
        sent = self.sock.send(msg)
#        print (sent)
        #while totalsent < MSGLEN:
        #    sent = self.sock.send(msg[totalsent:])
        #    if sent == 0:
        #        raise RuntimeError("socket connection broken")
        #    totalsent = totalsent + sent
#
    def tcpreceive(self, length = 4096):
        chunks = []
        bytes_recd = 0
        self.sock.settimeout(1.0)
        try:
            chunk = self.sock.recv(length)
        #except socket.timeout:
        except :
            input ("Warning: Please source ./FEMB_start in Putty, and click any button.")
            return None
        self.sock.settimeout(None)
        return chunk
#        while bytes_recd < MSGLEN:
#            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
#            if chunk == b'':
#                raise RuntimeError("socket connection broken")
#            chunks.append(chunk)
#            bytes_recd = bytes_recd + len(chunk)
#        return b''.join(chunks)


    def tcp_poke(self, addr = 0x0, data = 0x0):
        self.create()
        self.connect()
        cmd = 3 
        aux = 0x0000 
        SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
        cmd_B    = cmd.to_bytes(2, byteorder = 'big')
        aux_B    = aux.to_bytes(2, byteorder = 'big')
        addr_B   = addr.to_bytes(4, byteorder = 'big')
        data_B   = data.to_bytes(4, byteorder = 'big')
        msg_send = SYSKEY_B + cmd_B + aux_B + addr_B + data_B
        self.tcpsend(msg_send)
        self.close()

    def tcp_peek(self, addr = 0x0):
        while True:
            self.create()
            self.connect()
            SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
            rd_cmd = 4
            rd_cmd_B    = rd_cmd.to_bytes(2, byteorder = 'big')
            rd_aux = 0
            rd_aux_B    = rd_aux.to_bytes(2, byteorder = 'big')
            rd_addr = addr
            rd_addr_B   = rd_addr.to_bytes(4, byteorder = 'big')
            rd_data = 0
            rd_data_B   = rd_data.to_bytes(4, byteorder = 'big')
            rd_msg_req = SYSKEY_B + rd_cmd_B + rd_aux_B + rd_addr_B + rd_data_B
            self.tcpsend(rd_msg_req)
            chunk = self.tcpreceive()
            self.close()
            if chunk != None:
                data = int.from_bytes(chunk[4*3:4*4], byteorder='big')
                return data 


    def tcp_cmd_io(self, cmd = 0x0000, aux=0x0000, addr = 0x0, data = 0x0):
        self.create()
        self.connect()
        SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
        cmd_B    = cmd.to_bytes(2, byteorder = 'big')
        aux_B    = aux.to_bytes(2, byteorder = 'big')
        addr_B   = addr.to_bytes(4, byteorder = 'big')
        data_B   = data.to_bytes(4, byteorder = 'big')
        msg_send = SYSKEY_B + cmd_B + aux_B + addr_B + data_B
        self.tcpsend(msg_send)
        self.close()

    def wib_ver(self):
        while True:
            self.create()
            self.connect()
            SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
            rd_cmd = 0x0
            rd_cmd_B    = rd_cmd.to_bytes(2, byteorder = 'big')
            rd_aux = 0
            rd_aux_B    = rd_aux.to_bytes(2, byteorder = 'big')
            rd_addr = 0
            rd_addr_B   = rd_addr.to_bytes(4, byteorder = 'big')
            rd_data = 0
            rd_data_B   = rd_data.to_bytes(4, byteorder = 'big')
            rd_msg_req = SYSKEY_B + rd_cmd_B + rd_aux_B + rd_addr_B + rd_data_B
            self.tcpsend(rd_msg_req)
            chunk = self.tcpreceive()
            self.close()
            if chunk != None:
                ch_len = len(chunk)//2
                tmp = struct.unpack_from(">%dH"%(ch_len), chunk)
                hw_ver = tmp[6]
                fw_ver = tmp[7]

                if self.longcable: 
                    print ("Long cable is in use...")
                    self.tcp_poke(addr=0x08, data=self.longcable)
                    if (self.tcp_peek(addr=0x08) == self.longcable):
                        pass
                    else:
                        print("Configuration for long cable is error, please check, exit anyway.")
                        exit()
                else:
                    print ("Short cable is in use...")
                    self.tcp_poke(addr=0x08, data=self.longcable)
                    if self.tcp_peek(addr=0x08) == self.longcable:
                        pass
                    else:
                        print("Configuration for short cable is error, please check, exit anyway.")
                        exit()

                return hw_ver, fw_ver 

    def tcp_rd_blk(self, cmd = 0x0000, aux=0x0000, addr = 0x0, data = 0x0):
        while True:
            self.tcp_cmd_io( cmd, aux, addr, data)
            self.create()
            self.connect()
            SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
            rd_cmd = 0x11
            rd_cmd_B    = rd_cmd.to_bytes(2, byteorder = 'big')
            rd_aux = 0
            rd_aux_B    = rd_aux.to_bytes(2, byteorder = 'big')
            rd_addr = 0
            rd_addr_B   = rd_addr.to_bytes(4, byteorder = 'big')
            rd_data = 0
            rd_data_B   = rd_data.to_bytes(4, byteorder = 'big')
            rd_msg_req = SYSKEY_B + rd_cmd_B + rd_aux_B + rd_addr_B + rd_data_B
            self.tcpsend(rd_msg_req)
            chunk = self.tcpreceive()
            self.close()
            if chunk != None:
                return chunk

    def femb_cd_fc(self,  fc_cmd = 0x0):
        self.create()
        self.connect()
        cmd = 0x14
        addr = 0
        aux = self.link_cs 
        SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
        cmd_B    = cmd.to_bytes(2, byteorder = 'big')
        aux_B    = aux.to_bytes(2, byteorder = 'big')
        addr_B   = addr.to_bytes(4, byteorder = 'big')
        data = fc_cmd 
        data_B   = data.to_bytes(4, byteorder = 'big')
        msg_send = SYSKEY_B + cmd_B + aux_B + addr_B + data_B
        self.tcpsend(msg_send)
        self.close()

    def femb_cd_wr(self, c_id = 2, c_page = 0, c_addr = 0x0, c_data = 0x0):
        self.create()
        self.connect()
        cmd = 0x12
        addr = 0
        aux = self.link_cs 
        SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
        cmd_B    = cmd.to_bytes(2, byteorder = 'big')
        aux_B    = aux.to_bytes(2, byteorder = 'big')
        addr_B   = addr.to_bytes(4, byteorder = 'big')
        data = ((c_id&0xff)<<24) + ((c_page&0xff)<<16) + ((c_addr&0xff)<<8)+ (c_data&0xff)
        data_B   = data.to_bytes(4, byteorder = 'big')
        msg_send = SYSKEY_B + cmd_B + aux_B + addr_B + data_B
        self.tcpsend(msg_send)
        self.close()

    def femb_cd_rd(self, c_id = 2, c_page = 0, c_addr = 0x0):
        #print (link_cs)
        while True:
            self.create()
            self.connect()
            SYSKEY_B = self.SYSKEY.to_bytes(4, byteorder = 'big')
            rd_cmd = 0x13 
            rd_cmd_B    = rd_cmd.to_bytes(2, byteorder = 'big')
            rd_aux = self.link_cs
            rd_aux_B    = rd_aux.to_bytes(2, byteorder = 'big')
            rd_addr = 0
            rd_addr_B   = rd_addr.to_bytes(4, byteorder = 'big')
            rd_data = ((c_id&0xff)<<24) + ((c_page&0xff)<<16) + ((c_addr&0xff)<<8)+ (0&0xff)
            rd_data_B   = rd_data.to_bytes(4, byteorder = 'big')
            rd_msg_req = SYSKEY_B + rd_cmd_B + rd_aux_B + rd_addr_B + rd_data_B
            self.tcpsend(rd_msg_req)
            chunk = self.tcpreceive()
            self.close()
            if chunk != None:
                data = int.from_bytes(chunk[4*3:4*4], byteorder='big')
                c_data = (data>>16)&0x0ff
                ack_err = ((data>>24)&0x02)>>1
                busy = ((data>>24)&0x01)
                return c_data, ack_err, busy 

#a = TCPSocket()
#i = 0
#while True:
#    a.tcp_peek(addr = i%100)
#    i = i +1
#    if i%100 == 0:
#        print (i)
##    if i> 15000:
##        exit()
