#!/usr/bin/python
from serialManager import SerialManager
from driveManager import DriveManager
from bridge import Bridge
import time
HDD_TEMP = 40
class OdroidController:
    def __init__(self):
        self.conn = SerialManager(9600)
        self.bridge = Bridge(self.conn)
        self.dm = DriveManager(self.bridge)
    
    

if __name__ == "__main__":
    oc = OdroidController()
    while True:
        hdd, cpu = oc.dm.watchTemp()
        if hdd>=HDD_TEMP and not oc.dm.fan:
            oc.dm.powerFan(1)
        if hdd<=(HDD_TEMP-2) and oc.dm.fan:
            oc.dm.powerFan(0)
        time.sleep(5)