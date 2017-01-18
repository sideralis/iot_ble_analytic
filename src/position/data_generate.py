'''
Created on Dec 28, 2016

@author: gautier
'''

from math import sqrt
import datetime

class MyRSSI(object):
    def __init__(self, id, rssi):
        self.id = id
        self.rssi = rssi

class MyDevice(object):
    
    def __init__(self, id):
        self.id = id
        self.rssi4devices = []
        
    def addrssi(self, id_rssi):
        self.rssi4devices.append(id_rssi)
        
        
class MyData(object):

    first_date = None
    first_id = None
    
    def __init__(self):
        self.time = [None] * 1000
        self.index = 0
        self.time.append([])

    def add(self, devices):
        self.time[self.index].append(devices)
        
    def next(self):
        self.time.append([])
        self.index = self.index + 1
        
    def getDist(self, id_from, id_to, t):
        d = []
        for dev_from in self.time[t]:
            if dev_from.id == id_from:
                for dev_to in dev_from.rssi4devices:
                    if dev_to.id == id_to:
                        d.append(dev_to.rssi)            
            if dev_from.id == id_to:
                for dev_to in dev_from.rssi4devices:
                    if dev_to.id == id_from:
                        d.append(dev_to.rssi)            
        return d
    
    def display(self):
        if (self.index >= 1):
            t = self.index-1
            print(t)
            for e in self.time[t]:
                print(e.id)
                for f in e.rssi4devices:
                    print(" {} {}".format(f.id, f.rssi))
            
            
            
    def process(self, fromid, toid, rssi, date_time):
        #extract time
        if self.first_date == None:
            self.first_date = date_time
            
        offset = date_time - self.first_date
        offset_in_sec = offset.total_seconds()
        temps = int(offset_in_sec / 5)
        self.index = temps
        #print("Debug {} {} {} {}".format(temps,fromid,toid,rssi))
        
        if (self.time[temps] == None):
            # No yet device for this time so we add the first one   
            #print("Debug: adding {}".format(fromid))   
            if (self.first_id == None):
                self.first_id = fromid    
            myDevice = MyDevice(fromid)
            myRSSI = MyRSSI(toid, rssi)
            myDevice.addrssi(myRSSI)
            self.time[temps] = []
            self.time[temps].append(myDevice)
        else:
            #print("Debug: some devices exist")
            # We have already a least one device, check if we should modify it or add it as a new one
            for e in self.time[temps]:
                #print("Debug: checking {}".format(e.id))
                e_found = False
                if e.id == fromid:
                    # device found, is the rssi already known ?
                    #print("Debug: device found")
                    e_found = True
                    f_found = False
                    for f in e.rssi4devices:
                        #print("Debug: checking to {}".format(f.id))
                        if f.id == toid:
                            #print("Debug: to found")
                            f_found = True
                            #print("INFO: rewriting rssi!")
                            f.rssi = rssi
                            break
                    if f_found == False:
                        #print("Debug: to not found, adding {}".format(toid))
                        myRSSI = MyRSSI(toid, rssi)
                        e.addrssi(myRSSI)
                    break
            if e_found == False:
                #print("Debug: device not found, adding {}".format(fromid))
                myDevice = MyDevice(fromid)
                myRSSI = MyRSSI(toid, rssi)
                myDevice.addrssi(myRSSI)
                if (fromid == self.first_id):
                    self.time[temps].insert(0, myDevice)
                else:
                    self.time[temps].append(myDevice)

            
class MyPosition(object):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    
    
dist = {
        0: {1:1, 2:sqrt(10)},
        1: {0:1, 2:3},
        2: {0:sqrt(10), 1:3}
        }        
        
         
        
def main():
    
    allMyData = MyData()
    for t in xrange(100):
        for i in xrange(len(dist)):
            myDevice = MyDevice("11:11:11:11:11:{}{}".format(i, i))
            for j in xrange(len(dist)):
                if j == i:
                    continue
                myRSSI = MyRSSI("11:11:11:11:11:{}{}".format(j, j), dist[i][j])
                myDevice.addrssi(myRSSI)
            allMyData.add(myDevice) 
        allMyData.next()
               

        
        
        
        
