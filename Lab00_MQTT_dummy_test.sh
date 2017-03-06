#! /bin/bash
# GIoT MQTT dummy test
# 連python 都不用直接用 mosquitto_sub 客戶端連線測試 GIoT 的MQTT Server
# 這shell script 需要安裝 mosquitto-clients
hostname=52.193.146.103
port=80
topic=client/200000017/200000017-GIOT-MAKER
username=200000017
password=44554652
client_id=200000017-generic-service
echo "Server=" $hostname":"$port
echo "topic=" $topic
echo "username/password=" $username "/" $password
echo "Client ID=" $client_id
mosquitto_sub  -h $hostname -p $port -t $topic -u $username -P $password -I $client_id
