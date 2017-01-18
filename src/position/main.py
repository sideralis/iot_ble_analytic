'''
Created on Dec 29, 2016

@author: gautier
'''

import paho.mqtt.client as mqtt
import json
from data_generate import MyData, MyPosition
from math import acos, sin, cos, pi
from datetime import datetime
import matplotlib.pyplot as plt
from time import sleep

allMyData = MyData()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("campusid/edison/rssi")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #allMyData.process(msg.payload)
    parsed_json = json.loads(str(msg.payload))
    my_time = datetime.strptime(parsed_json["date"],'%Y-%m-%dT%H:%M:%SZ')
    allMyData.process(parsed_json["from"], parsed_json["to"], parsed_json["rssi"], my_time)
        
def calculate():
    
    #allMyData.display()
    getposition()
    #plt.axis([-256, 256, -256, 256])
    #hl.set_xdata([e.x for e in mypos])   
    #hl.set_ydata([e.y for e in mypos]) 
    #plt.draw()  
 
    

def getposition():
    mypos = None
    # let's calculate
    if allMyData.index >= 1:
        t = allMyData.index-1
    
        print("temps = {}".format(t))   
        
        mydevices = allMyData.time[t]
        
        mypos = []
        
        # Position first device
        myposition = MyPosition(mydevices[0].id, 0, 0)
        mypos.append(myposition)
        
        device = mydevices[0].rssi4devices
        for i in xrange(len(device)):
            # Now calculate distance to all remaining devices 
            if i == 0:
                # second device is always north of first device
                distance = allMyData.getDist(mydevices[0].id, device[0].id, t)
                if (len(distance) != 0):
                    d = sum(distance)/float(len(distance))
                    myposition = MyPosition(device[0].id, 0, d)
                    mypos.append(myposition)
            else:                
                #  On cherche phy
                #  le point 1 a pour coordonnee polaire dist[0][1], pi/2
                #  le point 2 a pour coordonnee polaire dist[0][2], phy
                #  le point 0 etant au centre (0,0)
                #  l'equation d'un cercle etant
                # r(theta) x r(theta) - 2 x r(theta) x r0 x cos(theta-phy) + r0 x r0 = a x a
                #  Sachant que le point 1 se trouve sur le cercle de rayon dist[1][2] ayant pour centre le point 2
                #  ce qui veut dire que
                #  r(theta) = dist[0][1] pour theta = pi/2
                #  a = dist[1][2]
                #  r0 = dist[0][2]
                #  ce qui se simplifie dans notre cas en:
                # cos(theta-phy) = (r(theta) x r(theta) + r0 x r0 - dist[1][2] x dist[1][2]) / (2 x r(theta) x r0)
                # cos(pi/2-phy) = (dist[0][1] x dist[0][1] + dist[0][2] x dist[0][2] - dist[1][2] x dist[1][2]) / ( 2 x dist[0][1] x dist[0][2])
                
                d01 = allMyData.getDist(mydevices[0].id, device[0].id, t)
                d02 = allMyData.getDist(mydevices[0].id, device[1].id, t)
                d12 = allMyData.getDist(device[0].id, device[1].id, t)
                if ( (len(d01) !=0) and (len(d02) !=0) and (len(d12) !=0)):
                    d01 = sum(d01)/float(len(d01))
                    d02 = sum(d02)/float(len(d02))
                    d12 = sum(d12)/float(len(d12))
                    angle = acos((d01 * d01 + d02 * d02 - d12 * d12) / (2 * d01 * d02))
                    phy = pi / 2 - angle
                    myposition = MyPosition(device[i].id, device[i].rssi * cos(phy), device[i].rssi * sin(phy))
                    mypos.append(myposition)
               
     
    return mypos   

def main():
    # open a plot
    plt.ion()
    hl, = plt.plot([0],[0],'ro')
    plt.axis([-256, 256, -256, 256])
    plt.pause(0.001)
    plt.show()
    #plt.draw()
    
    # Subscribe to MQTT messages
    print("Subscribing to messages")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("iot.eclipse.org", 1883, 60)
    client.loop_start()
    sleep(1)

    print("Calculating positions")
    while True:
        pos = getposition()
        if pos is not None:
            print ('Updating plot')
            for e in pos:
                print("  device={} x={} y={}".format(e.id, e.x, e.y))  
            #hl.set_xdata([e.x for e in pos[0:3]])   
            #plt.pause(0.001)
            #hl.set_ydata([e.y for e in pos][0:3]) 
            #plt.pause(0.001)
            hl, = plt.plot([e.x for e in pos],[e.y for e in pos],'ro')
            plt.pause(0.001)
            plt.draw()  
        sleep(2)
    
 
    print("end")
    
    
if __name__ == '__main__':
    main()