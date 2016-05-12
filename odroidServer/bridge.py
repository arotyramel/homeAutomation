#!/usr/bin/python
import serial
import time

from sets import Set
HIGH = 1
LOW = 0
# digitalWrite 0
# digitalRead 1
# analogWrite 2
# analogRead 3
import os
class Bridge():
    def __init__(self,conn):
        
        self.feedback = Set()
        self.conn = conn
        self.conn.setReadCallback(self.cleanFeedback)
        

    def cleanFeedback(self,res):
        if res[0] != ">":
            print "response",res
            return
        res = tuple([x.rstrip() for x in res.split(";")][1:])
        self.feedback.add(res)
        
    def waitFeedback(self,msg):
        msg = tuple(msg.split(";")[1:])
        found = False
        answer=None
        for feedback in self.feedback:         
            if msg==feedback[:len(msg)]:
                found = True
                answer= feedback
                break
        if not found:
            return None
#         print "found answer"
        self.feedback.remove(answer)
        return answer
        
    def send(self, data, resend=0):
        if resend>3:
            print "no response after sending information 3 times"
            return None
        
        if len(data)>0:
            msg  = ">"+data+"\r"
            if self.conn.send(msg):
                res = self.waitFeedback(data)
                if res is None: 
                    return self.send(data,resend+1)
                else:
                    return res
            else:
                print "Could not send data"
                return None
        
    def digitalWrite(self,pin,value):
        msg = ";0;"+str(pin)+";"+str(int(value))
        return self.send(msg)
        
    def digitalRead(self,pin):
        msg = ";1;"+str(pin)
        return self.send(msg)
        
    def analogWrite(self,pin,value):
        return self.send(";2;"+str(pin)+";"+str(int(value)))
        
    def analogRead(self,pin):
        return self.send(";3;"+str(pin))

   
if __name__ == "__main__":
    b = Bridge(0)
    print "bridge started"
#     print "writeD",b.digitalWrite(14,1)
#     print "readD", b.digitalRead(13)[3]
    
    
    
    while True:
        time.sleep(1)
        value =  b.analogRead(15)[2]
#         print "raw value", value
        print "temp", (float(value)*0.004882813-0.5)*100
        continue
        r = int(b.digitalRead(13)[2])
        print "res",r
        if r:
            b.digitalWrite(13,0)
        else:
            b.digitalWrite(13,1)
#   
#         print "---------------"
#         print "---------------"
# #         
    