#! /usr/bin/python
# -*- coding: utf8 -*-
# dummy 就是不用模組也可驗證MQTT 連線的狀況，credentials 範例裏的 IP, account 是會固定吐出MQTT 資訊的。
__author__ = "Marty Chao"
__version__ = "1.0.4"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change Log 1.0.3 , support paho-mqtt v1.2
# Change Log 1.0.4 , 優化顯示訊息

import paho.mqtt.client as mqtt
import json
HostName = "52.193.146.103"
PortNumber= "80"
Topic = "client/200000017/200000017-GIOT-MAKER"
UserName = "200000017"
Password = "44554652"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print("Topic:"+ msg.topic)
    json_data = msg.payload
    print(json_data)
    sensor_data = json.loads(json_data)['recv']
    #sensor_value = sensor_data.decode("hex")
    date_value = sensor_data.split("T")[0]
    time_value = sensor_data.split("T")[1]
    print("date:"+date_value+", time:"+time_value)

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

