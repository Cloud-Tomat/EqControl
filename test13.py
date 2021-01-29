#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:12:05 2020

@author: nicolas
"""

SIDERAL_SPEED=15.041
VIDEO=0

import numpy as np 
import cv2 
import math as math


from datetime import datetime
import time

import select
import sys


import threading

import cFrameBuffer
import cServo
import cPubSub
import cCapture
import cTools

terminate=False
path="/mnt/data/sandbox/eq/s1/"

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False



def interactive():
    global Kp,Kd,terminate,rstFrameBuf,rstServo,rstTime,rstCap,servo
    while not terminate:
        command = input(">")
        exec(command, globals())
        #print("Kp=%2.3f\tKd=%2.3f"%(Kp,Kd))


def ProcessDirectory(path,outputPath):
    global results
    global terminate
    global rstFrameBuf,rstServo,rstTime,rstCap
    global servo
    
    results=None
    terminate=False

    #----------
    #Init Serial
    if True:
        ser = cTools.cRobustSerial()
        ser.open()
    else:
        ser=None
    #-----------
    pub=cPubSub.cPublish(5557)
    
    #-----------
    #Init video

    cap = cv2.VideoCapture(VIDEO)
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
    
    capture=cCapture.cCapture(VIDEO)
    capture.startThread()
    
#----------

    time1, frame1 = capture.getFrame()
    frameBuffer=cFrameBuffer.cFrameBuffer(time,frame1)
    rstFrameBuf=False
    rstServo=False
    rstTime=False
    rstCap=False
    dist=0.0
    distOffset=0.0
    lastTime=0
    lastUpdate=0
    lastDist=0
    
    avgSpeed=0.0
    
    while(not heardEnter()):
        time2,frame2=capture.getFrame()
        #print("%3.3f\t%3.3f"%(time2-lastTime,time2-lastUpdate))
        lastTime=time2
        dist,angle,speed=frameBuffer.update(time2,frame2)
        avgSpeed=0.2*speed+0.8*avgSpeed
        #print(avgSpeed)
        if (dist==lastDist):
            calcDist=dist+avgSpeed*(time2-lastUpdate)
        else:
            calcDist=dist
            lastDist=dist
            lastUpdate=time2
        #calcDist=dist
        #print("%3.3f\t%3.3f"%(dist,calcDist))
        if True: #(dist!=lastDist):
            result=[time2-time1,calcDist,angle,speed,servo.command]
            #result=[time2-time1,dist+distOffset,angle,speed]
            servo.addResult(result)
            pub.pubList("result",result)


    terminate=True


if __name__ == '__main__':
    ProcessDirectory("","/mnt/data/sandbox/eqEncoder/video/")
