#!/usr/bin/python
import serial
from post_threading import Post
import time

class SerialManager():
    def __init__(self,baud=9600,port=None,):
        self.post = Post(self)
        self.port = port
        self.baud = baud
        self.conn_down = True
        
        self.initConnection(baud,port)
        
    def openSerialPort(self,baud,port):
        try:
            self.ser = serial.Serial('/dev/ttyUSB'+str(port), baud)
            self.ser.flushInput()
            self.ser.flush()
            self.conn_down = False
            return True
        except Exception, e:
            if "[Errno 2]" in str(e):
                return False
            else:
                print "Problem accessing the device",e
                exit(1)   
        
    def initConnection(self,baud,port):
        
        if port is None:
            for i in xrange(4):
                if self.openSerialPort(baud,i):
                    break
        else:
            self.openSerialPort(baud,port)
        
        if self.conn_down:
            print "could not establish connection"
            exit(1)
            return
        
        self.post.readFeedback()
    
    def setReadCallback(self,cb):
        self.cb = cb    
    
    def readFeedback(self):
        while not self.conn_down:
            res = self.ser.readline()
            self.cb(res)
            
    def send(self,data):
        if self.conn_down:
            return False
        else:
            try:
                self.ser.write(data)
                self.ser.flush()
                return True
            except:
                self.conn_down = True
                time.sleep(1)
                self.initConnection( self.baud,self.port)
                return False
            