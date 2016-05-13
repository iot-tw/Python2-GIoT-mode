# server_python
Access GIoT MQTT Server Side example on python
## 範例程式說明
## Lab 0 初始 
Lab00_MQTT_dummy_test.sh 連python 都不用直接用 mosquitto_sub 客戶端連線測試 GIoT 的MQTT Server

Lab00_MQTT_dummy_test.py dummy 就是不用模組也可驗證MQTT 連線的狀況，credentials 範例裏的 IP, account 是會固定吐出MQTT 資訊的。
## Lab 1 第一章 先把資料抓下來
Lab01_MQTT_sub.py 搭配 LAB01 Arduino 的上傳資料 AT_DTX Raw Data
## Lab 2 溼度，溫度 還有LED
Lab02_HumidityTemperatureLEDs.py # 這是一個樹莓派的範例，用LED 燈號表示溫度高低。
## Lab 3 可變電阻代替 溫溼度計
Lab03_VariableResistor_sub.py # 這是用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。
LAB02 的代碼內容仍然保留。
## Lab 4 除了可變電阻再加上一個按鈕
Lab04_VariableResistor_Button_sub.py # LAB03中 用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。仍保留
增加一個按鈕，連續按壓5秒以上，發送一個 button down 事件通知。
