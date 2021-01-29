#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:11:46 2021

@author: nicolas
"""

import time
import threading
import numpy as np

class cServo:
    
    def __init__(self,serialPort):
        if (serialPort is None):
            print("No Serial Port : Simulation")
            self.simu=True
        else:
            self.simu=False
            self.ser=serialPort
            time.sleep(3)
            self.sendCommand(1)

        
        #PID params 
        self.Kp=1        #3   #8
        self.Kd=50        #500   #5000
        self.Ki=0.1
        
        #Target Speed
        self.speedTh=0.6444027869097377/1000*1.05
        
        #Speed from speedTh/speedfactor to speedTh*SpeedFactor
        self.speedFactor=2
        
        #depth of analysis
        self.limit=5

        #Servo loop time in ms
        self.timeStep=1000
        
        #Terminate servo thread
        self.terminate=False
        
        #result of move calc between frames
        self.results=None
        
        self.lastTime=0
        self.realTime=time.time()
        
        self.prevCommand=1.0
        self.command=1
        self.filter=0.7
        self.saturation=2
        self.erreur=0
        self.integrale=0


    def sendCommand(self,command):
        if (not self.simu):
            cmdTxt=bytes("%5.2f#"%(command), 'utf-8')
            self.ser.write(cmdTxt)

    def startServoThread(self):
        servoThread = threading.Thread(target=self.servo)
        servoThread.start()

    def servo(self):
        while not self.terminate:
            if (not self.results is None):
                while (self.results[-1,0]-self.lastTime)<self.timeStep and not self.terminate:
                    time.sleep(0.001)
                self.update()
            else:
                    time.sleep(0.001)                
        self.sendCommand(1)

    def addResult(self,result):
        if (self.results is None):
            self.results=np.array([result])
        else:
            self.results=np.vstack((self.results,result))

    def speedEstimator(self,results,command):
        z = np.polyfit(results[:,0],results[:,1], 1)
        p = np.poly1d(z)
        speed=p(1)-p(0)
        #print (self.speedTh*self.prevCommand*1000/1.26872012613875,",",speed*1000,",",np.mean(results[:,3])*1000)
        self.prevCommand=command


    def update(self):
        self.lastTime=self.results[-1,0]
        results=np.copy(self.results)
        self.results=None
        #print(len(results), results[-1,1]-results[0,1])
        #print ((time.time()-self.realTime)*1000)
        self.realTime=time.time()
 
        
        x=results[:,0]
        y=results[:,1]
        v=results[:,3]
           
        dt=np.mean(x)
        lastPos=np.mean(y)
        speed=np.mean(v)
            
        #Position error
        erreurP=lastPos-dt*self.speedTh
        
        #Derivative of pos error estimate
        erreurH=[y[i]-x[i]*self.speedTh for i in range(len(x))]
        z = np.polyfit(x,erreurH, 1)
        p = np.poly1d(z)
        erreurD=p(1)-p(0)

        self.integrale=self.integrale+erreurP

        self.erreur=self.erreur*self.filter+ (1-self.filter)*( self.Kp*erreurP +self.Kd*erreurD)+self.Ki*self.integrale




        if (self.erreur<-self.saturation): self.erreur=-self.saturation
        if (self.erreur>self.saturation): self.erreur=self.saturation
        
        
            
        command=(1+abs(self.erreur)/self.limit)*self.speedFactor/2
        self.speedEstimator(results, command)

        if (self.erreur>0) : command=1/command
        self.command=command
        self.sendCommand(command)


                    
                
