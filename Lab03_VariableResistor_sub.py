#! /usr/bin/python
# -*- coding: utf8 -*-
# 這是用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。
# LAB02 的代碼仍保留 comment 起來。
__author__ = "Marty Chao"
__version__ = "1.0.3"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
#Changelog 1.0.3 移除credentials 機制


import paho.mqtt.client as mqtt
import json
GIOT = "52.193.146.103"
SELF = "192.168.88.198"
HostName = GIOT
PortNumber= 80
Topic = "client/200000020/200000020-GIOT-MAKER"
UserName = "200000020"
Password = "18923571"
macAddr = "050000c9"
if HostName != "52.193.146.103":
    PortNumber = 1883
    Topic = "GIOT-GW/UL/1C497B499010"
    UserName = "admin"
    Password = "admin"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    if HostName == "52.193.146.103":
        json_data = json.loads(msg.payload)
        sensor_time = json_data['recv']
        sensor_gwip = json_data['extra']['gwip']
        sensor_snr = json_data['extra']['snr']
    else:
        json_data = json.loads(msg.payload)[0]
        sensor_time = json_data['time']
        sensor_gwip = json_data['gwip']
        sensor_snr = json_data['snr']
    #print(json_data)
    sensor_data = json_data['data']
    #print sensor_data
    sensor_macAddr = json_data['macAddr'][-8:]
    if sensor_macAddr == macAddr:
        sensor_value = str(int(float(sensor_data.decode("hex"))/33333*100))
        print('value: ' + sensor_value +'% Time: '+ sensor_time + " GWIP:" + sensor_gwip + " SNR:" + str(sensor_snr))

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

