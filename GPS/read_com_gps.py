#!/usr/bin/env python
# coding=utf-8
import serial
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM11'
ser.open()
while True:
    print ser.readline()
