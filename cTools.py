#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 18:49:58 2021

@author: nicolas
"""

import serial
import time


class cRobustSerial:
    def __init__(self):
        self.ser=serial.Serial()
        self.ser.baudrate=115200
        self.running=True

    def open(self):
        Success=False
        Port=0
        while (not Success and self.running):
            try:
                self.ser.port=('/dev/ttyACM%d'%Port)
                self.ser.open()
                Success=True
                print ("Success port %d"%Port)
            except:
                Port=(Port+1)%4
                time.sleep(0.3)


    def write(self,ToSend):
        try:
            self.ser.write(ToSend)
            #print (ToSend)
        except:
            print ("USB Fail try to reconnect")
            self.open()