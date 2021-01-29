#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:07:41 2021

@author: nicolas
"""
import cv2 
import threading
import time

class cCapture:
    
    def __init__(self,port):
        self.port=port
        self.width=1280
        self.height=720
        self.frame=None
        self.timeStamp=None
        self.lock=False
        self.terminate=False
        self.read=False
        
        self.cap=cv2.VideoCapture(self.port)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
        
    def capFrame(self):
        execTime=0

        self.cap.grab()
        ret,frame = self.cap.retrieve()
        msecCounter = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        while (self.lock):
            pass
            #print("waiting Frame")
            #time.sleep(0.001)            
        self.frame=frame
        self.timeStamp=msecCounter
        self.read=False


    def capThread(self):
        while not self.terminate:
            self.capFrame()
    
    def startThread(self):
        servoThread = threading.Thread(target=self.capThread)
        servoThread.start()
    
    def getFrame(self):
        while (self.frame is None) or (self.read):
            time.sleep(0.001)

        self.lock=True
        frame=self.frame.copy()
        timeStamp=self.timeStamp
        self.read=True
        self.lock=False
        return timeStamp,frame