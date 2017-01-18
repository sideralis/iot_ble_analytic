'''
Created on Jan 17, 2017

@author: gautier
'''


class ToId(object):
    def __init__(self, toID, rssi):
        self.rssi = {}
        self.rssi[toID] = [rssi,1]

                 
    def addTo(self, toID, rssi):
        # Add toID object if it does not exists
        # or update existing one
        if toID in self.rssi:
            self.rssi[toID][0] += rssi          # Accumulate rssi to do a mean later on
            self.rssi[toID][1] += 1             # Store number of accumulation
        else:
            self.rssi[toID] = [rssi,1]

    
class AllId(object):
    def __init__(self):
        self.temps = None
        self.fromID = {}      # A dict of {fromid: {toid:rssi, toid: rssi, ...}, fromid: {toid:rssi, toid: rssi, ...}, ... }
    
    def output(self):
        print ("{")
        for kfrom, vfrom in self.fromID.iteritems():
            print ('    "id": "{}",'.format(kfrom))
            print ('    "around": [')
            for kto, vto in vfrom.rssi.iteritems():
                print ('        {')
                print ('        "to": "{}",'.format(kto))
                print ('        "rssi": {}'.format(vto[0]/vto[1]))
                print ('        },')
            print ('    ],')
        print ("}")

    def parse(self, fromid, toid, rssi, temps):
        # Special case first measurement received
        if self.temps is None:
            self.temps = temps

        # Calculate number of second elpqsed since begin of this 5 seconds slice
        offset = temps - self.temps
        offset_in_sec = offset.total_seconds()
       
        # Did we move to  next slice? 
        if offset_in_sec >= 5:
            # Yes, then print result
            self.output()
            # and restart from 0
            self.temps = temps
            self.fromID = {}
            
        # Now add the new measurement
        if fromid in self.fromID:
            self.fromID[fromid].addTo(toid, rssi)
        else:
            self.fromID[fromid] = ToId(toid, rssi)                 
        
    
    