#! /usr/bin/python
# -*- coding: utf8 -*-
''' Public MQTT Broker 的DL的script。GIoT MQTT 2017.8.3 開始支持DL
使用台北市府物聯網，宜蘭縣府，新竹市府的PoC 環境都支援了'''
__author__ = "Marty Chao"
__version__ = "1.0.1"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
import paho.mqtt.client as mqtt
import socket
import random
from optparse import OptionParser
import time
HostName = "52.193.146.103"
PortNumber = 80
Topic = "client/200000020/200000020-GIOT-MAKER/dl"
UserName = "200000020"
Password = "18923571"
macAddr = "04000476"
now_time = time.strftime("%Hc%Mc%S")
usage = "usage: %prog [options] [data]\n \
    e.g.: '%prog --data \"12345678901\" will downlink to module 04000476 by Localhost Broker,Class A confirmed"
parser = OptionParser(usage)
parser.add_option("-d", "--data", action="store", dest="data",
                  default=now_time,
                  help="for sending HEX data, Default is Current Time")
parser.add_option("-c", "--class", action="store", dest="classtype",
                  default="A",
                  help="[A|a|C|c] for Class Mode.  Default is Class A\n \
                Lowercase is unconfimed message,Uppercase is confirmed\n")
parser.add_option("-i", "--ip", action="store", dest="host",
                  default="localhost",
                  help="IP for which MQTT Broker. Default is localhost")
parser.add_option("-g", "--gid", action="store", dest="GID",
                  help="GID for DL GW. Default is 00001c497b431fcd")
parser.add_option("-m", "--mac", action="store", dest="MAC",
                  default="04000476",
                  help="setting DL target Moudle MAC")
(options, args) = parser.parse_args()
data = options.data
mid = "".join(map(lambda t: format(t, "02X"), [random.randrange(256)
              for x in range(16)]))
GID = options.GID
MAC = options.MAC
# topic = "GIOT-GW/DL/" + GID
if options.classtype == "a":
    txpara = '"2"'
elif options.classtype == "A":
    txpara = '"6"'
elif options.classtype == "c":
    txpara = '"22"'
elif options.classtype == "oc":
    txpara = '34'
elif options.classtype == "C":
    txpara = '"26"'
elif options.classtype == "B":
    print("Not Support yet.")
else:
    txpara = "6"
msg = '{"correlationId":"' + mid + '",' \
    + '"dldata":{' \
    + '"macAddr":"' + MAC + '",' \
    + '"data":"' + data + '",' \
    + '"extra":{' \
    + '"port":2, "txpara":' + txpara
if options.GID:
    msg = msg + ',"gwid":"' + GID + '"}}}'
else:
    msg = msg + '}}}'
print ("Broker:"+HostName+" Topic:"+Topic+" Class Mode:"+options.classtype)
print (msg)
client = mqtt.Client(protocol=mqtt.MQTTv31)
try:
    client.username_pw_set(UserName, Password)
    client.connect(HostName,PortNumber, 60)
except socket.error as e:
    print ("Can't Connect to " + HostName)
    print ("May check your internet connect?")

client.publish(Topic, msg)
client.disconnect()
