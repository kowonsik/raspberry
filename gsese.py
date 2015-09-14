#!/usr/bin/python
# sese.py
 
import socket
import os
import sys
import struct
import time


ETYPE_VALUE_MAX = 8000

#####
g_recent = {}

def checkValue( metric, tag, recentValues, currentValue ):
    if len( recentValues ) == 0:
        return True

    if recentValues[-1] > currentValue:
    	print >> sys.stderr, "CHECKVALUE) recentValues: " + recentValues
    	print >> sys.stderr, "CHECKVALUE) incoming value: " + currentValue 
    	
    	raw_input('press any key.' )
    	
        return False

    return True

def STDOUT( s ):
    global g_recent

    arr       = s.split()
    metric    = arr[0]
    timestamp = int( arr[1] )
    value     = float( arr[2] )
    tag       = arr[3]

    key = metric + ":" + tag
    if not g_recent.has_key( key ):
        g_recent[ key ] = []

    if checkValue( metric, tag, g_recent[key], value ): 
        print s

        g_recent[ key ] = g_recent[ key ][ -10: ]
        g_recent[ key ].append( [ timestamp, value ] )
        g_recent[ key ].sort()


    else:                       
        print >> sys.stderr, "***** invalid range::" + s


def bigEndian(s):
    res = 0
    while len(s):
        s2 = s[0:2]
        s = s[2:]

        res <<= 8
        res += eval( '0x' + s2 )

    return res
    
def littleEndian(s):
    res = 0
    while len(s):
        s2 = s[-2:]
        s = s[:-2]

        res <<= 8
        res += eval( '0x' + s2 )

    return res

def swapBytes(s):
    assert len(s) == 8, s
    res = s[2:4] + s[0:2] + s[6:8] + s[4:6]
    assert len(res) == 8, s + "->" + res 
    return res

def toFloat(s):
    assert len(s) == 8, s
    
    hex = '"' + '\\x' + s[0:2] + '\\x' + s[2:4] + '\\x' + s[4:6] + '\\x' + s[6:8] + '"'
    hex = eval( hex )
    res = struct.unpack( 'f', hex )[0]
    return res



def main():
    
    splug_acc_flag = 0
    etype_acc_flag = 0

    SERVER_ADDR = "222.239.78.8"
    SERVER_PORT = 8283   # 40001 samho  9293 hana 
    
    
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( ( SERVER_ADDR, SERVER_PORT ) )
    
    readBuffer = ""
    receivedLines = []
    sendLines = []
    
    while True:
        # provide buffer
        recv = sock.recv( 1024 )
        readBuffer += recv
    
        # consume buffer    
        l = readBuffer.split( ":" )
        
        if ( len(l) < 2 ):
            pass # nothing to do
        else:
            # dump
            #print >> sys.stderr, "*readBuffer='" + readBuffer + "'"

            #
            readBuffer = ""
    
            # check last
            e = l[-1]
            l = l[:-1]
            if e != "":
                readBuffer = e
                # dump
                #print >> sys.stderr, "+readBuffer='" + readBuffer + "'"
    
            # check first
            s = l[0]
            if s.startswith( "Welcome" ):
                s = s[ len( "Welcome"): ]
                l[0] = s
    
            #
            receivedLines += l
    
            # 
            #for s in l:
            #   print >> sys.stderr, "+line='" + s + "'"
    
        # make packets
        for s in receivedLines:
            try:
                #
                if len( s ) < 48:
                    print >> sys.stderr, "wrong data:" + s
                    #print >> sys.stderr, "dump receivedLines"
                    for ss in receivedLines:
                        print >> sys.stderr, ss

                assert len(s)>=48

                # common
                head = s[:20]
                type = s[20:24]
                serialID = s[24:36]
                nodeID = s[36:40]
                seq = s[40:44]
                battery = s[44:48]

		if type =="0063" :
                        pass
                elif type=="00D3" :
                        pass
                elif type=="00D4" :
                        pass
                elif type=="0072" :
                        pass
                elif type=="0070" :
                        pass
                elif type=="006D" :
                        pass
                elif type=="0064" :
                        pass
                elif type=="00D7" :
			print "00D7"
			print "rootech voltage"
                elif type=="00D8" :
			print "00D8"
			print "rootech current"
                else :
                        print s
                        print " "

                #print "%s nodeID=%s" %( type,bigEndian( nodeID )    )
            
                if type == "0063": # BASE
                    node_id = bigEndian(nodeID)
                    recv = bigEndian(s[48:52])
                    send = bigEndian(s[52:56])
                    t = int(time.time())
                    print "gyu_RC1_base.recv %d %f nodeid=%d" % ( t, recv, node_id )
                    print "gyu_RC1_base.send %d %f nodeid=%d" % ( t, send, node_id )
                    
                elif type == "0064" : # TH
                    node_id = bigEndian(nodeID)
                    temperature = bigEndian( s[48:52] )
                    humidity = bigEndian( s[52:56] )
                    light = bigEndian( s[56:60] )

                    # T
                    v1 = -39.6 + 0.01 * temperature
                    #v1 = -46.85 + 175.72 * float(temperature) / pow(2,16)
                    
                    # H
                    tmp = -4 + 0.0405 * humidity + (-0.0000028) * humidity * humidity
                    v2 = (v1 - 25) * (0.01 + 0.00008 * humidity) + tmp

                    # L
                    tmp = (light * 100) / 75
                    v3 = tmp * 10
                    
                    #
                    t = int(time.time())
                    tt = time.localtime()

                    if -30<v1<80 :
                            print "gyu_RC1_thl.temperature %d %f nodeid=%d" % (t, v1, node_id )
                            #print "gyu_RC1_thl.temperature %d %.2f nodeid=%d" % (t, v1*(-1), node_id )
                    if 0<v2<100:
                            print "gyu_RC1_thl.humidity %d %f nodeid=%d" % (t, v2, node_id )
                    if 0<v3<5000:
                            if tt.tm_hour < 5 :
			          if v3 > 1000 :
				        pass
                            elif tt.tm_hour > 20 : 
				  if v3 > 1000 :
				        pass
                            else :
                                  print "gyu_RC1_thl.light %d %f nodeid=%d" % (t, v3, node_id )
                    print "gyu_RC1_thl.batt %d %d nodeid=%d" % (t, bigEndian(battery), node_id )

                elif type == "0070" : # TH
                    node_id = bigEndian(nodeID)
                    temperature = bigEndian( s[48:52] )
                    humidity = bigEndian( s[52:56] )
                    light = bigEndian( s[56:60] )

                    # T
                    #v1 = -46.85 + 0.01 * temperature
                    
                    # H
                    tmp = -6 + 125 * humidity / 4095
                    v2 = tmp

                    # L
                    tmp = (light * 1.017)
                    v3 = tmp
                    
                    v1 = -46.85 + 175.72 * float(temperature) / pow(2,16)
                    #v2 = -6 + 125 * float(humidity) / pow(2,16)
                    #
                    t = int(time.time())
                    if -30<v1<80 :
                            print "gyu_RC1_thl.temperature %d %.2f nodeid=%d" % (t, v1*(-1), node_id )
                    if 0<v2<100:
                            print "gyu_RC1_thl.humidity %d %.2f nodeid=%d" % (t, v2, node_id )
                    if 0<v3<5000:
                            if tt.tm_hour < 5 :
				  if v3 > 1000 :
				        pass
                            elif tt.tm_hour > 19 : 
				  if v3 > 1000 :
				        pass
                            else :
                                  print "gyu_RC1_thl.light %d %f nodeid=%d" % (t, v3, node_id )
                    print "gyu_RC1_thl.batt %d %d nodeid=%d" % (t, bigEndian(battery), node_id )

                elif type == "0065":# PIR
                    t = int(time.time())
                    node_id = bigEndian(nodeID)
                    pir = bigEndian(s[48:52])
                    print "gyu_RC1_pir %d %f nodeid=%d" % (t, pir, node_id )
        
                elif type == "0066":# CO2
                    node_id = bigEndian(nodeID)
                    ppm = s[48:52]

                    tmp = float( bigEndian( ppm ) )
                    value = float( 1.5 * ( tmp  / 4086 ) * 2 * 1000 )

                    t = int(time.time())
                    if 200<value<2000:
                            print "gyu_RC1_co2.ppm %d %f nodeid=%d" % ( t, value, node_id )
        
                elif type == "006D" or type == "006d": # SPlug
                    node_id = bigEndian(nodeID)
                    #current = s[48:54]
                    #t_current = s[60:66]
                    rawData = s[54:60]
                    tmp = bigEndian( rawData )
                    if tmp > 15728640:
                        tmp = 0
                    else:
                        tmp = float( tmp / 4.127 / 10 )

                    watt = tmp
                    t = int(time.time())
                    if 0<=watt<3000:
                            print "gyu_RC1_splug.watt %d %f nodeid=%d" % ( t, watt, node_id )
        
                elif type == "0072": # SPlug2
                    node_id = bigEndian(nodeID)
                    #current = s[48:54]
                    #t_current = s[60:66]
                    rawData = s[48:56]
                    tmp = bigEndian( rawData )
                    tmp = float( tmp / 100 )
                    watt = tmp
                    
                    t_watt_rawData = s[56:64]
                    t_watt_tmp = bigEndian( t_watt_rawData )
                    t_watt_tmp = float( t_watt_tmp / 10000000.0 )
                    t_watt = t_watt_tmp
                    
                    t = int(time.time())
                    if 0<=watt<3000:
                            print "gyu_RC1_splug.watt %d %f nodeid=%d" % ( t, watt, node_id )

                    print "gyu_RC1_splug.t_watt %d %f nodeid=%d" % ( t, t_watt, node_id ) 
                    #STDOUT( "gyu_RC1_splug.t_watt %d %f nodeid=%d" % ( t, t_watt, node_id ) ) ######

                elif type == "00D3" or type == "00d3": # etype
                    node_id = bigEndian(nodeID)
                    # length check
                    if len( s ) < 72:
                        print >> sys.stderr, "ignore too short data for etype:" + s
                        continue

                    t_current = s[48:56]
                    current = s[64:72]
        
                    current = toFloat( swapBytes( current ) )
                    t_current = littleEndian( swapBytes( t_current ) )
                    nodeID = bigEndian( nodeID )

                    # check maximum value
                    if current > ETYPE_VALUE_MAX:
                            print >> sys.stderr, "overflow etype.current: %f, nodeID=%d" % ( current, nodeID )
                            pass
                    elif current <= 0:
                            print >> sys.stderr, "underflow etype.current: %f, nodeID=%d" % ( current, nodeID )
                            pass
                    else:
                            t = int(time.time())
                            if 0<current<30000:
                                    print "gyu_RC1_etype.current %d %f nodeid=%d" % ( t, current, nodeID )

                    if t_current > 50000000:
                            print >> sys.stderr, "overflow etype.current: %f, nodeID=%d" % ( current, nodeID )
                            pass
                    else:
                            t = int(time.time())
                            print "gyu_RC1_etype.t_current %d %d nodeid=%d" % ( t, t_current, nodeID )

                elif type == "0071":# CO2
                    node_id = bigEndian(nodeID)
                    ppm = s[48:52]

                    tmp = int( bigEndian( ppm ) )
                    value = tmp

                    t = int(time.time())
                    if 200<value<2000:
                            print "gyu_RC1_co2.ppm %d %f nodeid=%d" % (t, value, node_id )

                elif type == "00D4": 
                    node_id = bigEndian(nodeID)
                    temp = s[48:52]
                    humi = s[52:56]
                    co2 = s[56:60]

                    v1 = int( bigEndian( temp ))/10.0
                    v2 = int( bigEndian( humi ))/10.0
                    v3 = int( bigEndian( co2 ))/10.0

                    t = int(time.time())
                    #if 0<v1<40:
                    print "gyu_RC1_maxfor.th %d %f nodeid=%d" % (t, v1, node_id )
                    if 0<v2<100:
                            print "gyu_RC1_maxfor.humi %d %f nodeid=%d" % (t, v2, node_id )
                    if 200<v3<2000:
                            print "gyu_RC1_maxfor.co2 %d %f nodeid=%d" % (t, v3, node_id )

                elif type == "00D5" or type=="00d5": 
                    node_id = bigEndian(nodeID)
                    raw = s[56:64]

                    tmp = bigEndian( raw )
                    senion_current_power = tmp
                    t = int(time.time())

		elif type == "00D6" or type == "00d6": # rootech
                    node_id = bigEndian(nodeID)
                    # length check
                    if len( s ) < 72:
                        print >> sys.stderr, "ignore too short data for etype:" + s
                        continue

                    acc_1 = s[64:66]
                    acc_2 = s[66:68]
                    acc_3 = s[68:70]
                    acc_4 = s[70:72]

                    aaa = int(acc_1,16)*256*256*256
                    bbb = int(acc_2,16)*256*256
                    ccc = int(acc_3,16)*256
                    ddd = int(acc_4,16)

                    acc = aaa+bbb+ccc+ddd
                    #acc = ccc+ddd

		    ins_1 = s[48:50]
                    ins_2 = s[50:52]
                    ins_3 = s[52:54]
                    ins_4 = s[54:56]

                    ggg = int(ins_1,16)*256
                    hhh = int(ins_2,16)

                    ins = ggg + hhh

                    #current = toFloat( swapBytes( current ) )
                    nodeID = bigEndian( nodeID )

                    # check maximum value
                    if ins > ETYPE_VALUE_MAX:
                            print >> sys.stderr, "overflow etype.current: %f, nodeID=%d" % ( ins, nodeID )
                            pass
                    elif ins < 0:
                            print >> sys.stderr, "underflow etype.current: %f, nodeID=%d" % ( ins, nodeID )
                            pass

                    if acc > 10000000:
                            print >> sys.stderr, "overflow etype.current: %f, nodeID=%d" % ( ins, nodeID )
                            pass
                    else:
                            t = int(time.time())
                            if nodeID==2701:
                                    if acc > 5000:
                                            print "gyu_RC1_etype.t_current %d %d nodeid=%d" % ( t, acc, nodeID )
                                    if 0<=ins<5000:
                                            print "gyu_RC1_etype.current %d %d nodeid=%d" % ( t, ins, nodeID )
                            else:
                                    if acc > 5000:
                                            print "gyu_RC1_etype.t_current %d %d nodeid=%d" % ( t, acc, nodeID )
                                    if 0<=ins<5000:
                                            print "gyu_RC1_etype.current %d %d nodeid=%d" % ( t, ins, nodeID )

                elif type == "00D7" or type == "00d7": # voltage rootech
                    node_id = bigEndian(nodeID)
                    # length check
                    if len( s ) < 72:
                    	    print >> sys.stderr, "ignore too short data for etype:" + s
                            continue

                    vol3_1 = s[64:66]
                    vol3_2 = s[66:68]

                    vol3_1_i = int(vol3_1,16)*256
                    vol3_2_i = int(vol3_2,16)

                    voltage_c = vol3_1_i + vol3_2_i

                    vol2_1 = s[56:58]
                    vol2_2 = s[58:60]

                    vol2_1_i = int(vol2_1,16)*256
                    vol2_2_i = int(vol2_2,16)

                    voltage_b = vol2_1_i + vol2_2_i

                    vol1_1 = s[48:50]
                    vol1_2 = s[50:52]

                    vol1_1_i = int(vol1_1,16)*256
                    vol1_2_i = int(vol1_2,16)

                    voltage_a = vol1_1_i + vol1_2_i

                    #current = toFloat( swapBytes( current ) )
                    nodeID = bigEndian( nodeID )

                    print "IN ROOTECH VOLTAGE"

                    t = int(time.time())
                    print "gyu_RC1_etype.voltage_a %d %d nodeid=%d" % ( t, voltage_a, nodeID )
                    print "gyu_RC1_etype.voltage_b %d %d nodeid=%d" % ( t, voltage_b, nodeID )
                    print "gyu_RC1_etype.voltage_c %d %d nodeid=%d" % ( t, voltage_c, nodeID )

                elif type == "00D8" or type == "00d8": # voltage rootech
                    node_id = bigEndian(nodeID)
                    print "IN ROOTECH CUREENT" 
                    # length check
                    if len( s ) < 72:
                        print >> sys.stderr, "ignore too short data for etype:" + s
                        continue

                    cur3_1 = s[64:66]
                    cur3_2 = s[66:68]

                    cur3_1_i = int(cur3_1,16)*256
                    cur3_2_i = int(cur3_2,16)

                    current_c = cur3_1_i + cur3_2_i

                    cur2_1 = s[56:58]
                    cur2_2 = s[58:60]

                    cur2_1_i = int(cur2_1,16)*256
                    cur2_2_i = int(cur2_2,16)

                    current_b = cur2_1_i + cur2_2_i

                    cur1_1 = s[48:50]
                    cur1_2 = s[50:52]

                    cur1_1_i = int(cur1_1,16)*256
                    cur1_2_i = int(cur1_2,16)

                    current_a = cur1_1_i + cur1_2_i

                    nodeID = bigEndian( nodeID )

                    t = int(time.time())
                    print "gyu_RC1_etype.current_a %d %d nodeid=%d" % ( t, current_a, nodeID )
                    print "gyu_RC1_etype.current_b %d %d nodeid=%d" % ( t, current_b, nodeID )
                    print "gyu_RC1_etype.current_c %d %d nodeid=%d" % ( t, current_c, nodeID )

                elif type == "00FA" : # Talk
                    node_id = bigEndian(nodeID)
                    v1 = int(bigEndian(s[48:50]))
                    v2 = int(bigEndian(s[52:54]))
                    print "gyu_RC1_routing.send %d %f nodeid=%d" % (t, v1, node_id )
                    print "gyu_RC1_routing.recv %d %f nodeid=%d" % (t, v2, node_id )
                    #print str(node_id) +  " CHECK : Send " + str(v1) + "  : RECV " + str(v2)
                else:
                    print >> sys.stderr, "Invalid type:" + type
                    pass
            except:pass
    
        # clear
        receivedLines = []

        sys.stdout.flush()  
    
    
if __name__ == "__main__":
    main()
    

