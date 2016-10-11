# 如何在Server 上讀取GIoT 的MQTT 資料？
Access GIoT MQTT Server Side example on python
按着四個LAB 完成模擬 數值與On-Off 資料的接受。需配合 arduino 項目的LAB 操作
## 範例程式說明
## Lab 0 初始 沒有模組時用下面兩程式先測試跟雲的連接，連帳號沒有也行。
Lab00_MQTT_dummy_test.sh 連python 都不用直接用 mosquitto_sub 客戶端連線測試 GIoT 的MQTT Server

Lab00_MQTT_dummy_test.py dummy 就是不用模組也可驗證MQTT 連線的狀況，credentials 範例裏的 IP, account 是會固定吐出MQTT 資訊的。
## Lab 1 第一章 先把資料抓下來
Lab01_MQTT_sub.py 搭配 LAB01 Arduino 的上傳資料 AT_DTX Raw Data
## Lab 2 溼度，溫度 還有LED
Lab02_HumidityTemperatureLEDs.py # 這是一個樹莓派的範例，用LED 燈號表示溫度高低。
## Lab 3 用可變電阻代替 溫溼度計
Lab03_VariableResistor_sub.py # 這是用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。

LAB02 的代碼內容仍然保留。
## Lab 4 除了可變電阻再加上一個按鈕
Lab04_VariableResistor_Button_sub.py # LAB03中 用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。仍保留

增加一個按鈕，連續按壓5秒以上，發送一個 button down 事件通知。
## Lab 4 利用樹莓派 16x2 RGB LCD 顯示可變電阻數值
Lab04_VR_Button_LCD_sub.py 
