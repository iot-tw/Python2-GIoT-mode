#!/usr/bin/env python
# coding=utf-8
try:
    import serial
except:
    print 'Missing package dependency for pySerial'
    raise
ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/tty.usbmodem1411'
ser.open()
while True:
    print ser.readline()
