#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import os
import serial
import RPi.GPIO as GPIO
import time
import struct
import binascii
import traceback
import fcntl, socket, struct

import json
import requests 

from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort
from twisted.internet import reactor

url = "http://125.7.128.53:4242/api/put"

def getHwAddr(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
	return ':'.join(['%02x' %ord(char) for char in info[18:24]])

macAddr = getHwAddr('eth0')
macAddr = macAddr.replace(':','.')

co2_val = 0

# HW setup, GPIO

def setup():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
	GPIO.setup(23, GPIO.OUT)
	GPIO.setup(24, GPIO.OUT)
	GPIO.setup(25, GPIO.OUT)
	GPIO.output(18, False)
	GPIO.output(23, False)
	GPIO.output(24, False)
	GPIO.output(25, False)
	time.sleep(1)


class BridgeProtocol(Protocol):
	def LOG(self, text):
		print ("%s" % text)
		sys.stdout.flush()

	def dataReceived(self, data):

		if len(data)<4:
			return	
		try:
			#print "data 1 : " + data[1]	
			#print "data 2 : " + data[2]	
			#print "data 3 : " + data[3]	
			#print "data 4 : " + data[4]	

			co2_val =  data[1]+data[2]+data[3]+data[4] 
			ppm = float(co2_val)

			
			if ppm < 1000:
				GPIO.output(18, True)	
				GPIO.output(23, False)	
				GPIO.output(24, False)	
				GPIO.output(25, False)	
			elif ppm < 1300:
				GPIO.output(18, True)	
				GPIO.output(23, True)	
				GPIO.output(24, False)	
				GPIO.output(25, False)	
			elif ppm < 1500:
				GPIO.output(18, True)	
				GPIO.output(23, True)	
				GPIO.output(24, True)	
				GPIO.output(25, False)	
			else:	
				GPIO.output(18, True)	
				GPIO.output(23, True)	
				GPIO.output(24, True)	
				GPIO.output(25, True)	

			print "co2 : " + str(ppm) + " ppm" 

			data = {
				"metric": macAddr+"_co2",
				"timestamp": time.time(),
				"value": ppm,
				"tags": {
					"host": "raspberry"
				}
			}
			ret = requests.post(url, data=json.dumps(data))
			print ret.text
			time.sleep(5)
		except:
			print "error"
			pass
			sys.stdout.flush()


if __name__ == '__main__':
	setup()

	SerialPort(BridgeProtocol(), "/dev/ttyAMA0", reactor, baudrate=38400)
	reactor.run()
