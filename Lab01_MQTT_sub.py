#! /usr/bin/python
# -*- coding: utf8 -*-
# 搭配 LAB01 Arduino 的上傳資料 AT_DTX Raw Data
__author__ = "Marty Chao"
__version__ = "1.0.1"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"

import paho.mqtt.client as mqtt
import json
import ConfigParser                                             # 匯入 配置檔 解析模塊
from os.path import expanduser
# 處理 giot credentials 設定值
home = expanduser("~")
default_value = "default"
default_identity_file = home + "/.giot/credentials"
# credentials 範例 在家目錄下建立一個 .giot/crendentials 的檔案
# 可以分多個[setion]在 用ConfigParser()時，可以靈活調用
# [dummy]
# hostname = 52.193.146.103
# portnumber= 80
# topic = client/200000017/200000017-GIOT-MAKER
# username = 200000017
# password = 44554652
config = ConfigParser.ConfigParser()
config.read(default_identity_file)
HostName = config.get(default_value, 'hostname')
PortNumber= config.get(default_value, 'portnumber')
Topic = config.get(default_value, 'topic')
UserName = config.get(default_value, 'username')
Password = config.get(default_value, 'password')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
    #print(json_data)
    sensor_data = json.loads(json_data)['data']
    # 處理MQTT 抓下來的 資料json 中的 data 欄位，用hex decode 回來
    sensor_value = sensor_data.decode("hex")
    # 抓取json 中的 gwid 這是表示通過那個AP 送進來的
    gwid_data = json.loads(json_data)['extra']['gwid']
    # 過濾某一個特定GIoT AP 送進來的 MQTT 資料，其他的不要
    # 每個 Indoor AP, OutDoor AP 都有兩個gwid,所以要抓兩個進來,如果不考慮過濾可以註釋掉
    if gwid_data == "00001c497b48dc03" or gwid_data == "00001c497b48dc11":
    	print('AT raw value: ' + sensor_value)
	print(json_data)
    # 列印出從MQTT 抓來的資料，這裏是用“/" 做爲 溼度與溫度兩個資料的區分
    #hum_value = sensor_value.split("/")[0]
    #temp_value = sensor_value.split("/")[1]
    #print("Hum:"+hum_value+", Temp:"+temp_value)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)
# 這裏第三個參數可以調整，每個多少時間檢查MQTT 連線狀態，通常60秒已經算短的了，爲了實驗，可以用60秒。
# 2-5分鐘都算合理，google 的 GCM 都28分鐘檢查一次了，在實際量產部署時，要重新考慮這個值，頻寬及Server Load 不是免費啊。
client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
