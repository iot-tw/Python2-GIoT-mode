#! /usr/bin/python
# -*- coding: utf8 -*-
# 抓取Local MQTT Broker 的UL 資料
__author__ = "Marty Chao"
__version__ = "1.0.1"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.1, support paho-mqtt 1.2

import paho.mqtt.client as mqtt
import json
import sys
import ConfigParser                                             # 匯入 配置檔 解析模塊
from os.path import expanduser
from optparse import OptionParser
#proc = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, shell=True)
#whoami_user = proc.communicate()[0].strip('\n')
#whoami_user = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, shell=True).communicate()[0].strip('\n')

usage = "usage: %prog [options] [host]\n\
  host: a MQTT broker IP \n\
  e.g.: '%prog --ip 192.168.1.1' will sub server and print data."

parser = OptionParser(usage)
parser.add_option("-d", "--display-lcd", action="store_true",
    help="print message to raspberry LCD")
parser.add_option("-l", "--long-detail", action="store_true",
    help="print detail JSON message")
parser.add_option("-t", "--topic", action="store",
    dest="topic", default="#",
    help="provide connection topic")
parser.add_option("-i", "--ip", action="store",
    dest="ip", default="localhost",
    help="sub from MQTT broker's IP ")
parser.add_option("-u", "--user", action="store",
    dest="username", default="admin",
    help="sub from MQTT broker's username ")
parser.add_option("-P", "--pw", action="store",
    dest="password", default="localhost",
    help="sub from MQTT broker's password ")
parser.add_option("-p", action="store",
    dest="port", default="1883",
    help="sub from MQTT broker's Port ")
(options, args) = parser.parse_args()
if options.display_lcd :
    import Adafruit_CharLCD as LCD
    lcd = LCD.Adafruit_CharLCDPlate()
# 處理 giot credentials 設定值
home = expanduser("~")
#default_value = "local"
#default_identity_file = home + "/.giot/credentials"
# credentials 範例 在家目錄下建立一個 .giot/crendentials 的檔案
# 可以分多個[setion]在 用ConfigParser()時，可以靈活調用
# [dummy]
# hostname = 52.193.146.103
# portnumber= 80
# topic = client/200000017/200000017-GIOT-MAKER
# username = 200000017
# password = 44554652
#config = ConfigParser.ConfigParser()
#config.read(default_identity_file)
if options.ip :
    HostName = str(options.ip)
else :
    HostName = "127.0.0.1"
#PortNumber= config.get(default_value, 'portnumber')
if options.topic :
    Topic = options.topic
else :
    Topic = "#"
#    Topic = config.get(default_value, 'topic')
#UserName = config.get(default_value, 'username')
#Password = config.get(default_value, 'password')
if options.port :
    PortNumber = options.port
else :
    PortNumber = "1883"
print ("MQTT broker is:" + HostName + ":" + PortNumber)
print ("MQTT Topic is:" + Topic )

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe(Topic)
    #client.subscribe("GIOT-GW/UL/1C497B4321AA")
    ###GIOT-GW/UL/xxxx [{"channel":923125000, "sf":10,
    ###"time":"2017-03-13T03:59:29", "gwip":"10.6.1.49",
    ###"gwid":"0000f835dde7de2e", "repeater":"00000000ffffffff",
    ###"systype":10, "rssi":-118.0, "snr":0.5, "snr_max":3.8, "snr_min":-4.5,
    ###"macAddr":"000000000a000158", "data":"015dff017b81ed0736767c",
    ###"frameCnt":26920, "fport":2}]
    #client.subscribe("GIOT-GW/UL/+")
    client.subscribe("#")
    #GIOT-GW/DL/1C497B499010 [{"macAddr":"0000000004000476","data":"5678","id":"998877ffff0001","extra":{"port":2, "txpara":6}}]
    #GIOT-GW/DL-report/1C497B499010 {"dataId":"16CBD520C19162013CD6436CB330565E", "resp":"2016-11-30T15:02:40Z", "status":-1}
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    json_data = msg.payload
    print(json_data)
    #print(msg.topic+" "+str(msg.payload))
    if msg.topic[:11]== "GIOT-GW/DL/":
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        sensor_id = json.loads(json_data)[0]['id']
        sensor_txpara = json.loads(json_data)[0]['extra']['txpara']

    elif msg.topic[:11]== "GIOT-GW/UL/":
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        sensor_value = sensor_data.decode("hex")
        gwid_data = json.loads(json_data)[0]['gwid']
        sensor_snr = json.loads(json_data)[0]['snr']
        sensor_rssi = json.loads(json_data)[0]['rssi']
        sensor_count = json.loads(json_data)[0]['frameCnt']
    else:
        #print (msg.topic+" "+str(msg.payload))
        sensor_mac = '0000000000000000'
        sensor_data = '0000000000000000'
    if   "0a" == str(sensor_mac)[8:10] :
        sensor_type = 'Asset Tracker'
    elif "04" == str(sensor_mac)[8:10] :
        sensor_type = 'Module Taipei'
    elif "05" == str(sensor_mac)[8:10] :
        sensor_type = 'Module Taiwan'
    elif "00" == str(sensor_mac)[8:10] :
        sensor_type = 'Location Box '
    elif "0d" == str(sensor_mac)[8:10] :
        sensor_type = 'Parking Can  '
    elif "02" == str(sensor_mac)[8:10] :
        sensor_type = 'RS485 tranmit'
    else:
        sensor_type = 'Unknow Module'
    if msg.topic[:11] == 'GIOT-GW/UL/':
        print('Type:' + sensor_type +'\tMac:'+ str(sensor_mac)[8:] \
              +'\tCount:' + str(sensor_count).rjust(6) \
              +'\tSNR:'+ str(sensor_snr).rjust(4) \
              +'\tRSSI:' + str(sensor_rssi).rjust(4) \
              +'\tGWID:' + str(gwid_data).rjust(8))
    elif msg.topic[:11] == 'GIOT-GW/DL/':
        print('Type:' + sensor_type +'\tMac:'+ str(sensor_mac)[8:]+ '\tMID:'+ str(sensor_id)+ '\tTXPara:' + str(sensor_txpara))
    else:
        print (msg.payload)
    if options.display_lcd :
        lcd.clear()
        lcd.message(str(sensor_mac)[8:]+'C:'+str(sensor_count))
        lcd.message('\nS/RSSI'+ str(sensor_snr)+ '/' + str(sensor_rssi))

    #if gwid_data == "00001c497b48dc03" or gwid_data == "00001c497b48dc11":
    try:
        print('     Payload: ' + sensor_data + '\x1b[6;30;42m' +' HEX2ASCII: '+ '\x1b[0m' + sensor_data.decode("hex"))
    except UnicodeDecodeError:
        print('     Payload: ' + sensor_data )
    if options.long_detail :
        print(json_data)
    #hum_value = sensor_value.split("/")[0]
    #temp_value = sensor_value.split("/")[1]
    #print("Hum:"+hum_value+", Temp:"+temp_value)

client = mqtt.Client(protocol=mqtt.MQTTv31)
#client = mqtt.Client()
try:
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(options.username, options.password)
# 這裏第三個參數可以調整，每個多少時間檢查MQTT 連線狀態，通常60秒已經算短的了，爲了實驗，可以用60秒。
# 2-5分鐘都算合理，google 的 GCM 都28分鐘檢查一次了，在實際量產部署時，要重新考慮這個值，頻寬及Server Load 不是免費啊。
    try:
        client.connect(HostName, PortNumber, 60)
    except :
        print ('Can not connect to Broker')
        print ('Specify a IP address with option -i.')
	sys.exit()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
    client.loop_forever()
except KeyboardInterrupt:
   sys.stdout.flush()
   print("W: interrupt received, stopping...")
#   pass
