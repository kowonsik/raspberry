#!/usr/bin/python
import os
import sys
import struct
import time
import binascii
import traceback
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.application import internet, service


class BridgeProtocol(Protocol):
    def LOG(self, text):
        print("[%s] %s" % (self.peerID, text))
        sys.stdout.flush()

    def connectionMade(self):
        self.peerID = str(self.transport.getPeer())
        #self.LOG("connection established.")
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.__buffer = ""

    def connectionLost(self, reason):
        #self.LOG("connection lost.")
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):

        #    self.LOG("processing:" + s)
	try:
		data = data.replace('[','')
		data = data.replace(']','')
		metric, time, value = data.split(",",3)

		time = int(time)
		value = float(value)

		print "%s %d %f" %(metric,time, value) 

        #        self.factory.writePoint(nodeid, time, watt)
	except Exception, e:
                self.LOG("exception!!")
                traceback.print_exc()

        sys.stdout.flush()


class BridgeProtocolFactory(Factory):
    protocol = BridgeProtocol

    def startFactory(self):
        Factory.startFactory(self)
        self.numProtocols = 0
        #self.__db = influxdb.InfluxDBClient('localhost', 8086, 'sese', 'sese', 'kmeg')
'''
    def writePoint(self, nodeID, timestamp, value):
        data = [{
                    "points": [[timestamp, value]],
                    "name": "raw.watt.%s" % nodeID,
                    "columns": ["time", "value"]
                }]
        self.__db.write_points_with_precision(data, 's')
'''

if __name__ == '__main__':
	while(1):
    		reactor.listenTCP(7878, BridgeProtocolFactory())
    		reactor.run()

