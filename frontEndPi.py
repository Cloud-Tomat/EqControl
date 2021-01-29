#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 20:50:42 2021

@author: nicolas
"""
import cPubSub
import numpy as np
import matplotlib.pyplot as plt


SIDERAL_SPEED=15.041

plt.ion()
speedTh=0.6444027869097377/1000*1.05 #pix/ms
scaleFactor=15.04/(speedTh*1000) #Arcsec/pix


sub=cPubSub.cSubscribe("192.168.0.49",5557)
sub.setFilter("result")
results=None
while (True):
    data=sub.getList()

    if (results is None):
        results=[data]
    else:
        print(data)
        results.append(data)
        results=results[-500:]

    if (not results is None):
        toGraph=np.array(results)
        x=toGraph[:,0]/1000.0
        y=toGraph[:,1]
        err=[(y[i]-speedTh*x[i]*1000)*scaleFactor for i in range(len(y))]        
        plt.plot(x,err)
        #plt.plot(x)
        plt.draw()
        plt.pause(0.001)
        plt.clf()



if False:
    outputRoot=str(datetime.now()).replace(":","-")+"_Eq_calib_"
    outputFile=outputPath+outputRoot+"raw_results.csv"
  
    
    print ("saving to "+outputFile)

    np.savetxt(outputFile,  
               results, 
               delimiter =",",  
               fmt ='% s',
               header="time,dist,angle,speed",
               comments="") 