#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:12:05 2020

@author: nicolas
"""

SIDERAL_SPEED=15.041

import numpy as np 
import cv2 
import math as math

import exifread
from datetime import datetime
import time

import select
import sys

import serial
import threading

import cFrameBuffer
import cServo
import cPubSub


terminate=False
path="/mnt/data/sandbox/eq/s1/"

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False




def capFrame(cap):
    execTime=0
    i=0
    while(execTime<0.03):
        i+=1
        e1 = cv2.getTickCount()
        cap.grab()
        e2 = cv2.getTickCount()
        execTime= ((e2 - e1)/ cv2.getTickFrequency())
    #print("%d\t%4.4f"%(i,execTime))
    
    msecCounter = cap.get(cv2.CAP_PROP_POS_MSEC)
    ret,frame = cap.retrieve()    
    return msecCounter,frame




def cap

def interactive():
    global Kp,Kd,terminate,rstFrameBuf,rstServo,rstTime,rstCap
    while not terminate:
        command = input(">")
        exec(command, globals())
        #print("Kp=%2.3f\tKd=%2.3f"%(Kp,Kd))


def ProcessDirectory(path,outputPath):
    global results
    global terminate
    global rstFrameBuf,rstServo,rstTime,rstCap
    
    results=None
    terminate=False

    #----------
    #Init Serial
    if True:
        ser = serial.Serial('/dev/ttyACM0',115200)
    #-----------
    pub=cPubSub.cPublish(5557)
    
    #-----------
    #Init video

    cap = cv2.VideoCapture(1)
    #Minimul buffer size to get the most recent frame from catpure
    cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    print(cap.get(cv2.CAP_PROP_BUFFERSIZE))

    #Max resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    #-----------
    

    
    
#-----------
#Start thread
    interactiveThread = threading.Thread(target=interactive)
    interactiveThread.start()

    servo=cServo.cServo(ser)
    servo.startServoThread()
#----------

    time1, frame1 = capFrame(cap)
    frameBuffer=cFrameBuffer.cFrameBuffer(time,frame1)
    rstFrameBuf=False
    rstServo=False
    rstTime=False
    rstCap=False
    dist=0.0
    distOffset=0.0
    lastTime=0
    while(not heardEnter()):

        if rstFrameBuf or rstServo or rstTime or rstCap:
            if rstFrameBuf:
                print("rstFameBuf")
                distOffset=distOffset+dist
                frameBuffer=cFrameBuffer.cFrameBuffer(time2,frame2)
                rstFrameBuf=False
                print(distOffset)
            if rstServo:
                print("rstServo")
                servo.terminate=True
                time.sleep(2)
                servo=cServo.cServo(ser)
                servo.startServoThread()
                rstServo=False
            if rstTime:
                print("rstTime")
                time1=time2
                dist=0
                distOffset=0
                rstFrameBuf=True
                rstServo=True                
                rstTime=False
            if rstCap:
                print("rstCap")
                cap.release()
                cap = cv2.VideoCapture(1)
                #Minimul buffer size to get the most recent frame from catpure
                cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
                print(cap.get(cv2.CAP_PROP_BUFFERSIZE))
            
                #Max resolution
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                rstCap=False
                rstTime=True
        else:
            time2p=cv2.getTickCount()/cv2.getTickFrequency()*1000
            time2,frame2=capFrame(cap)
            print(time2-lastTime)
            lastTime=time2
            dist,angle,speed=frameBuffer.update(time2,frame2)
            result=[time2-time1,dist+distOffset,angle,speed]
            servo.addResult(result)
            pub.pubList("result",result)


    terminate=True


if __name__ == '__main__':
    ProcessDirectory("","/mnt/data/sandbox/eqEncoder/video/")
