import sys
import os
import serial
import RPi.GPIO as GPIO
import time
import struct
import binascii
import traceback
import fcntl, socket, struct

from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort
from twisted.internet import reactor

co2_val = 0

# HW setup, GPIO
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

def getHwAddr(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
	return ':'.join(['%02x' %ord(char) for char in info[18:24]])


macAddr = getHwAddr('eth0')
macAddr = macAddr.replace(':','.')

print macAddr

class BridgeProtocol(Protocol):
	def LOG(self, text):
		print ("%s" % text)
		sys.stdout.flush()

	def connectionMade(self):
		self.LOG("connection established.")
		self.__buffer = ""

	def connectionLost(self, reason):
		self.LOG("connection lost.")

	def findMessage(self, data):
		pass

	def processMessage(self, data):
		pass

	def dataReceived(self, data):
		try:
			co2_val =  data[0]+data[1]+data[2]+data[3]+data[4]+data[5] 
			co2_val = float(co2_val)
			
			if co2_val < 1000:
				GPIO.output(18, True)	
				GPIO.output(23, False)	
				GPIO.output(24, False)	
				GPIO.output(25, False)	
			elif co2_val < 1300:
				GPIO.output(18, True)	
				GPIO.output(23, True)	
				GPIO.output(24, False)	
				GPIO.output(25, False)	
			elif co2_val < 1500:
				GPIO.output(18, True)	
				GPIO.output(23, True)	
				GPIO.output(24, True)	
				GPIO.output(25, False)	
			else:	
				GPIO.output(18, True)	
				GPIO.output(23, True)	
				GPIO.output(24, True)	
				GPIO.output(25, Ture)	

			print "co2 : " + str(co2_val) + " ppm  " 
			os.system("echo [%s,%d,%f] | nc 125.7.128.53 7878" % (macAddr+"_co2", time.time(), co2_val))
		except:
		       	pass 
			sys.stdout.flush()


if __name__ == '__main__':
	SerialPort(BridgeProtocol(), "/dev/ttyAMA0", reactor, baudrate=38400)
	reactor.run()
