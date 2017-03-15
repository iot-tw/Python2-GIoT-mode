#! /usr/bin/python
# -*- coding: utf8 -*-
''' Local MQTT Broker 的DL的script,前提是要有自己的GIoT Gateway。
使用台北市府物聯網，宜蘭縣府，新竹市府的PoC 環境目前不支持DL。'''
import paho.mqtt.client as mqtt
import socket
import random
from optparse import OptionParser
import time
now_time = time.strftime("%Hc%Mc%S")
usage = "usage: %prog [options] [data]\n \
    options: -d for sending data\n \
             -c [A|B|C] for Class Mode.  Default is Class A\n \
             -i IP for which MQTT Broker. Default is localhost\n \
             -g GID for DL GW. Default is 00001c497b431fcd\n \
             -m MAC for DL Node. Default is 04000476 \n \
    e.g.: '%prog --data \"12345678901\" will downlink to modules"
parser = OptionParser(usage)
parser.add_option("-d", "--data", action="store", dest="data",
                  default=now_time,
                  help="sending data")
parser.add_option("-c", "--class", action="store", dest="classtype",
                  default="A",
                  help="sending data")
parser.add_option("-i", "--ip", action="store", dest="host",
                  default="localhost",
                  help="setting Broker IP")
parser.add_option("-g", "--gid", action="store", dest="GID",
                  default="00001c497b431fcd",
                  help="setting ODU/IDU GID")
parser.add_option("-m", "--mac", action="store", dest="MAC",
                  default="04000476",
                  help="setting DL target Moudle MAC")
(options, args) = parser.parse_args()
if options.data:
    data = options.data
mid = "".join(map(lambda t: format(t, "02X"), [random.randrange(256)
              for x in range(16)]))
# This is  GID example
# GID = "00001c497b431fcd"
# GID = "1C497B4321AA"
GID = options.GID
# MAC = "04000476"
MAC = options.MAC
topic = "GIOT-GW/DL/" + GID
# txpara = "22" is Class C, txpara=6 is class A
txpara = "6"
if options.classtype == "A":
    txpara = "6"
elif options.classtype == "C":
    txpara = '"22"'
elif options.classtype == "B":
    print("Not Support yet.")
msg = '[{"macAddr":"00000000' + MAC + '",' \
    + '"data":"' + data + '",' \
    + '"id":"' + mid + '",' \
    + '"extra":{"port":2, "txpara":'+txpara+'}}]'
print ("Broker:"+options.host+" Topic:"+topic+" Class Mode:"+options.classtype)
print (msg)
client = mqtt.Client()
try:
    client.connect(options.host, 1883, 60)
except socket.error as e:
    print ("Can't Connect to " + options.host)
    print ("May use -i to specify broker server?")

client.publish(topic, msg)
client.disconnect()
