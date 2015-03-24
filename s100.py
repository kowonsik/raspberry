##this code for S100, ELT CO2 sensor
## Please see details for the CO2 sensor : http://goo.gl/NtRdqZ

import serial,os,time
import sys
import RPi.GPIO as GPIO
import logging 

debug_print = 0

# level = 0, init, no LED
# level = 1, 0~1000 ppm, blue LED
# level = 2, 1000~1200 ppm, green LED
# level = 3, 1200~1500 ppm, red LED
# level = 4, 1500~1700 ppm, red LED, blue LED
# level = 5, 1700~2000 ppm, red LED, Green LED
# level = 6, 2000 ppm ~, red LED, Green LED, blue LED
level = 0
ppm = 0
# check length, alignment of incoming packet string
def syncfind():
	index = 0
	alignment = 0
	while 1:
		in_byte = serial_in_device.read(1)
# packet[8] should be 'm'
# end of packet is packet[10]
		if in_byte is 'm' :
			#print 'idx =', index, in_byte
			alignment = 8
		if alignment is 10 : 
			alignment = 1
			index = 0
			break
		elif alignment > 0 :
			alignment += 1
		index += 1

logging.basicConfig(filename='/home/pi/test.log',level=logging.DEBUG)
logging.info("Start------------------------------- ")

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
logging.info('---->>>> GPIO all set ')

try:
	serial_in_device = serial.Serial('/dev/ttyAMA0',38400)
except serial.SerialException, e:
	GPIO.output(18, False)
	GPIO.output(23, False)
	GPIO.output(24, False)
	GPIO.output(25, False)

print '---->>>> start measuring CO2 '

########start here
syncfind()

while 1:
	try:
		in_byte = serial_in_device.read(11)
	except serial.SerialException, e:
		GPIO.output(18, False)
		GPIO.output(23, False)
		GPIO.output(24, False)
		GPIO.output(25, False)
	if not (len(in_byte) is 11) : 
		print "try next loop"
		continue
	if not (in_byte[8] is 'm'):
		break
	if ('ppm' in in_byte):
		if debug_print :
			print '  got ppm packet'
			print '0', in_byte[0]
			print '1', in_byte[1]
			print '2', in_byte[2]
			print '3', in_byte[3]
			print '4', in_byte[4]
		logging.warning("warning -----")
		#logging.warning("in_byte[1] = %s", in_byte[1])
		if not (in_byte[1] is ' ') :
			ppm = (int(in_byte[1])) * 1000
		if not (in_byte[2] is ' ') :
			ppm += (int(in_byte[2])) * 100
		if not (in_byte[3] is ' ') :
			ppm += (int(in_byte[3])) * 10
		if not (in_byte[4] is ' ') :
			ppm += (int(in_byte[4])) 
		logline = 'CO2 Level is '+ str(ppm) + ' ppm'+ ' : ' 
		now = time.localtime()
		now_str = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
		logline += now_str
		print logline
		logging.warning("logline = %s", logline)
		logline = ""
	else :
		GPIO.output(24, False)
# level = 1, 0~1000 ppm, blue LED
# level = 2, 1000~1250 ppm, green LED
# level = 3, 1250~1500 ppm, red LED
# level = 4, 1500~1750 ppm, red LED, blue LED
# level = 5, 1750~2000 ppm, red LED, Green LED
# level = 6, 2000 ppm ~, red LED, Green LED, blue LED
	if ppm < 1000 :  
		GPIO.output(18, True)
		GPIO.output(23, False)
		GPIO.output(24, False)
		GPIO.output(25, False)
	elif ppm < 1250 :  
		GPIO.output(18, True)
		GPIO.output(23, True)
		GPIO.output(24, False)
		GPIO.output(25, False)
	elif ppm < 1500 :  
		GPIO.output(18, True)
		GPIO.output(23, True)
		GPIO.output(24, True)
		GPIO.output(25, False)
	elif ppm < 1750 :  
		GPIO.output(18, True)
		GPIO.output(23, True)
		GPIO.output(24, True)
		GPIO.output(25, True)
	ppm = 0
#raw_input('press enter to exit program')
syncfind()
GPIO.cleanup()


