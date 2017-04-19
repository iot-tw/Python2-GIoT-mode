#! /usr/bin/python
# -*- coding: utf8 -*-
__author__ = "Marty Chao"
__version__ = "1.0.2"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.2, support paho-mqtt 1.2

import paho.mqtt.client as mqtt
import json
HostName = "52.193.146.103"
PortNumber = 80
Topic = "client/200000020/200000020-GIOT-MAKER"
UserName = "200000020"
Password = "18923571"
macAddr = "050000c9"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
    sensor_data = json.loads(json_data)['data']
    sensor_value = sensor_data.decode("hex")
    gwid_data = json.loads(json_data)['extra']['gwid']
    sensor_macAddr = json.loads(json_data)['macAddr']
    if sensor_macAddr == macAddr:
        print('ID: ' + macAddr)
        print('AT ASCII value: ' + sensor_value)
    print(json_data)


client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)
client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
