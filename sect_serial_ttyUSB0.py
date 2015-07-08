#!/usr/bin/python

import time
import os
import sys
import serial


state = 0
packet =''
available = " "

def list_serial_ports():
    global availalbe 
    if os.name == 'posix' :
        for i in range(256):
            try:
                s = serial.Serial(i)
                available += str(i+1)+"   "
                s.close()
            except serial.SerialException:
                pass
    return available

def bigEndian(s):
	res = 0
	while len(s):
		s2 = s[0:2]
		s = s[2:]

		res <<=8
		res += eval('0x' + s2)
	return res

def littleEndian(s):
	res = 0
	while len(s):
		s2 = s[-2:]
		s = s[:-2]

		res <<= 8
		res += eval('0x' + s2)
	return res

def sese(s):

    head = s[:20]
    type = s[20:24]
        
    serialID = s[24:36]
    nodeID = s[36:40]
    seq = s[40:44]
        
    if type == "0064" : # TH
        temperature = bigEndian( s[48:52] ) 
        humidity = bigEndian( s[52:56] ) 
        light = bigEndian( s[56:60] ) 
        v1 = -39.6 + 0.01 * temperature 
        tmp = -4 + 0.0405 * humidity + (-0.0000028) * humidity * humidity 
        v2 = (v1 - 25) * (0.01 + 0.00008 * humidity) + tmp 
        tmp = (light * 100) / 75 
        v3 = tmp * 10 
        t = int(time.time()) 
        print "gyu_RC1_thl.temperature %d %f nodeid=%d" % ( t, v1, bigEndian( nodeID ) ) 
        print "gyu_RC1_thl.huumidity %d %f nodeid=%d" % ( t, v2, bigEndian( nodeID ) ) 
        print "gyu_RC1_thl.light %d %f nodeid=%d" % ( t, v3, bigEndian( nodeID ) ) 

    elif type == "0070" : # TH : Total Sensor
        temperature = bigEndian( s[48:52] ) 
        humidity = bigEndian( s[52:56] )
        light = bigEndian( s[56:60] )
        v1 = -46.85 + 0.01 * temperature
        tmp = -6 + 125 * humidity / 4095
        v2 = tmp
        tmp = (light * 1.017)
        v3 = tmp

        t = int(time.time())
        print "gyu_RC1_thl.temperature %d %f nodeid=%d" % ( t, v1, bigEndian( nodeID ) )
        print "gyu_RC1_thl.humidity %d %f nodeid=%d" % ( t, v2, bigEndian( nodeID ) )
        print "gyu_RC1_thl.light %d %f nodeid=%d" % ( t, v3, bigEndian( nodeID ) )

    elif type == "0065":
        pass
    elif type == "0066":
        ppm = s[48:52]

        t = int(time.time())
        tmp = float(bigEndian(ppm))
        value = float(1.5*(tmp/4086)*2*1000)

        print "gyu_RC1_co2.ppm %d %f nodeid=%d" % (t, value, bigEndian(nodeID))
        print ""

    elif type == "006D" or type == "006d":  #Splug

		rawData = s[54:60]
		tmp = bigEndian(rawData)
		if tmp > 15728640:
			tmp = 0
		else:
			tmp = float(tmp/4.127/10)

		watt = tmp
		t = int(time.time())
		print "gyu_RC1_splug.watt %d %f nodeid=%d" % (t, watt, bigEndian(nodeID))
		print ""

    elif type == "0072": #Splug2
		rawData = s[54:60]
		tmp = bigEndian(rawData)
		if tmp > 15728640:
			tmp=0
		else:
			tmp = float(tmp/4.127/10)

		watt = tmp
		t = int(time.time())
		print "gyu_RC1_splug.watt %d %f nodeid=%d" % (t, watt, bigEndian(nodeID))
		print ""
			
    elif type == "00D3" or type == "00d3":       #etype
		#if len(s) < 72:
		#	print >> sys.stderr, "ignore too short data for etype:" + s
		#	continue
			
		t_current = s[48:56]
		current = s[64:72]

		current = toFloat(swapBytes(current))
		t_current = littleEndian(swapBytes(t_current))
		nodeID = bigEndian(nodeID)

		if current > ETYPE_VALUE_MAX:
			print >> sys.stderr, "overflow etype.current: %f, nodeID=%d" %(current, nodeID)
		elif current <= 0:
			print >> sys.stderr, "underflow etype.current: %f, nodeID=%d" %(current, nodeID)
		else:
			t = int(time.time())
			print "gyu_RC1_etype.t_current %d %d nodeid=%d" % (t, t_current, nodeID)
			print "gyu_RC1_etype.current %d %f nodeid=%d" % (t, current, nodeID)
			
    elif type == "0071":
		ppm = s[48:52]

		t = int(time.time())
		tmp = int(bigEndian(ppm))
		value = tmp
		print "gyu_RC1_co2.ppm %d %f nodeid=%d" % (t, value, bigEndian(nodeID))
		print ""

    elif type == "0063":  # base
		recv = bigEndian(s[48:52])
		send = bigEndian(s[52:56])

		t = int(time.time())
		print "gyu_RC1_base.recv %d %f nodeid=%d" % (t, recv, bigEndian(nodeID))
		print "gyu_RC1_base.send %d %f nodeid=%d" % (t, send, bigEndian(nodeID))
		print ""
		print ""

    else:
		print >> sys.stderr, "Invalid type : " + type
		pass
			
if __name__ == '__main__':

	test = serial.Serial("/dev/ttyUSB0", 115200)
	tmpPkt = []
	flag =0

#	if list_serial_ports() !="":
#		port = list_serial_ports()
#		print port

	while 1:
		Data_in = test.read().encode('hex')

		if(Data_in == '7e'):
			if(flag == 2) :
				flag =0
				tmpPkt.append(Data_in)
				packet = ''.join(tmpPkt)
				sese(packet)
				tmpPkt = []
				sys.stdout.flush()
			else :
				flag = flag + 1
				tmpPkt.append(Data_in)
		else :
			if(flag == 1 and Data_in =='45') :
				flag =2
			tmpPkt.append(Data_in)

