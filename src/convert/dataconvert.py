'''
Created on Jan 16, 2017

@author: gautier
'''

import paho.mqtt.client as mqtt
import json
from datetime import datetime

from data import AllId
import sys

allId = AllId()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("campusid/edison/rssi")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("{}".format(str(msg.payload)))
    parsed_json = json.loads(str(msg.payload))
    my_time = datetime.strptime(parsed_json["date"],'%Y-%m-%dT%H:%M:%SZ')
    allId.parse(parsed_json["from"], parsed_json["to"], parsed_json["rssi"], my_time)

def read_entries():
    for ligne in open(r'rssi_data.txt'):
        #print(ligne)
        parsed_json = json.loads(ligne)
        my_time = datetime.strptime(parsed_json["date"],'%Y-%m-%dT%H:%M:%SZ')
        allId.parse(parsed_json["from"], parsed_json["to"], parsed_json["rssi"], my_time)
        

def main():
    read_entries()
    sys.exit()
    
    print("Subscribing to messages")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("iot.eclipse.org", 1883, 60)
    client.loop_start()
    while True:
        pass
    
if __name__ == '__main__':
    main()