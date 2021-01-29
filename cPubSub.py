#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 19:48:39 2021

@author: nicolas
"""

import zmq
import json
import time

class cPublish:
    
    def __init__(self,port):
        self.port=port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)

    def pubList(self,topic,list):
        messageDataJ=json.dumps(list)
        msg=self.serialize(topic,messageDataJ)
        msg=msg.encode()
        self.socket.send(msg)
        
    def serialize(self,topic, msg):
        """ json encode the message and prepend the topic """
        return topic + ' ' + json.dumps(msg)

class cSubscribe:

    def __init__(self,ip,port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect ("tcp://%s:%s" % (ip,port))


    def setFilter(self,topic):
        topicFilter = topic.encode()
        self.socket.setsockopt(zmq.SUBSCRIBE, topicFilter)


    def getList(self):
        msgByte= self.socket.recv()
        topic, messageData = self.deserialize(msgByte.decode("utf-8") )
        return messageData

    def deserialize(self,topicmsg):
        """ Inverse of mogrify() """
        json0 = topicmsg.find('"')
        topic = topicmsg[0:json0].strip()
        msg = json.loads(topicmsg[json0+1:-1])
        return topic, msg 

