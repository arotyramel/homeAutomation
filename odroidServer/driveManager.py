#!/usr/bin/env python
import subprocess
import datetime
import time
import serial
TIMEOUT = 120 #sec
from post_threading import Post
class DriveManager():
	def __init__(self,bridge):
		self.post = Post(self)
		self.driveState = True
		self.relay = True
		self.fan = False
		self.bridge = bridge
		self.hddTempSensor = False
		self.lastHDDTemp = None
			
	def getLastAccess(self):
		offset = time.timezone
		cmd = ["sudo","tail" ,"-n", "1","/var/log/nginx/access.log"]
		res = subprocess.check_output(cmd,startupinfo=None,stderr=subprocess.STDOUT)
		dt =  res.split("[")[1].split("]")[0][:-9]
		dt = datetime.datetime.strptime(dt,"%d/%b/%Y:%H:%M")
		now =  datetime.datetime.now()
		return (now - dt).total_seconds()
	
	def unmountDrive(self):
		try:
			cmd = ["sh","/home/odroid/homeAutomation/umountHDD.sh"]
			subprocess.call(cmd)
			self.driveState = False
		except:
			print "could not unmount drive"
		
	def mountDrive(self):
		try:
			cmd = ["sh","/home/odroid/homeAutomation/mountHDD.sh"]
			subprocess.call(cmd)
			self.driveState = True
		except:
			print "could not mount drive"

	def powerHDD(self,state):
		self.relay = state
		self.bridge.digitalWrite(4, not state)
		
	def powerFan(self,state):
		self.fan = state
		self.bridge.digitalWrite(7, not state)
		
	def getHDDTemp(self):
		if not self.hddTempSensor:
			self.bridge.digitalWrite(14, 1)
		res = self.bridge.analogRead(1)
		if not res is None and len(res)>=3:
			res = (float(res[2])*0.004882813-0.5)*100 
		else:
			print "could not get HDD temp"
			res = -1
			
		if res < 0:
			return -1
		else:
			if self.lastHDDTemp is None:
				self.lastHDDTemp = res
			else:
				self.lastHDDTemp = self.lastHDDTemp*0.9+res*0.1
			return self.lastHDDTemp
		
	def getCPUTemp(self):
		cmd = ["cat","/sys/devices/virtual/thermal/thermal_zone0/temp"]
		try:
			res = int(subprocess.check_output(cmd,startupinfo=None,stderr=subprocess.STDOUT))/1000
		except:
			print "could not get cpu temp"
			res = -1
		return res
	
	def watchHDDActivity(self,loop=0):
		while True:
			
			last_access = self.getLastAccess()
			#manage mounting
			if last_access > TIMEOUT: #no access
				if self.driveState:
					self.unmountDrive()
				else:
					if last_access > 2*TIMEOUT and self.relay:
						self.powerHDD(0) #cut power
				
			else:
				if not self.relay:
					self.powerHDD(1) # supply power to hdd
					time.sleep(10)
					continue
					
				if not self.driveState:
					self.mountDrive()
					self.driveState = True
				
			print "Drive State", dm.driveState,  "Relay", dm.relay, "Last Access", last_access
			
			if not loop:
				return
			time.sleep(10)

	def watchTemp(self,loop=0):
		while True:
			hddTemp = self.getHDDTemp()
			cpuTemp = self.getCPUTemp()
			print ("HDD: %s"%hddTemp)
			print ("CPU: %s"%cpuTemp)
			if not loop:
				return [hddTemp,cpuTemp]
			time.sleep(10)

if __name__=="__main__":
	dm = DriveManager()
	while True:
		time.sleep(10)
		last_access = dm.getLastAccess()
		#manage mounting
		if last_access > TIMEOUT: #no access
			if dm.driveState:
				dm.unmountDrive()
			else:
				if last_access > 2*TIMEOUT and not dm.relay:
					dm.triggerRelay(1) #cut power
			
		else:
			if dm.relay:
				dm.triggerRelay(0) # supply power to hdd
				continue
				
			if not dm.driveState:
				dm.mountDrive()
				dm.driveState = True
			
		print "Drive State", dm.driveState,  "Relay", dm.relay, "Last Access", last_access

	