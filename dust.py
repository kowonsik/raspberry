# -*- coding: utf-8*-

import os
import sys
import urllib2
import time

import json
import requests

tsdb_url = "http://125.7.128.53:4242/api/put"

def getWebpage(url, referer=''):
    debug = 0
    if debug:
        return file(url.split('/')[-1], 'rt').read()
    else:
        opener = urllib2.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'),
            ('Referer', referer),
        ]
        return opener.open(url).read()

def getDataPage():
    return getWebpage('http://www.airkorea.or.kr/index')
    #url 가져오기
    
def normailize(s):
    return s.replace('<td>','').replace('</td>','').replace(' ','')
    #불필요한 코드 제거
def printUsing():
    print sys.argv[0], '<output file name>'

def getDatetime(buffers):
    return buffers.split('<p class="now_time">')[1].split('<strong>')[1].split('</strong>')[0]
    #url 소스에서 날짜 부분 추출
def getDatablocks(buffers):
    a = buffers.split('<tbody id="mt_mmc2_10007">')[1]
    b = a.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','')
    r = ''
    for line in b.split('<td>'):
       if len(line) < 30:
           line = line.strip()
           r = r+line+' '
       else:
           line = line.strip()
           r = r+line+'\n'
    return r.split('\n')[1:-1]
    #url 소스에서 데이터 부분 추출

def index():
    if len(sys.argv) <> 1:
        printUsing()
    pnt = "%s \n" % getDatetime(getDataPage())
    pnt2 = getDatablocks(getDataPage())
    pnt3 = ""

    for i in pnt2:
        pnt3+=i
        pnt3+="\n"
    return pnt3


ex_flag = 1 
k = 0

tsdb_url = "http://125.7.128.53:4242/api/put"

while 1:
	t = time.localtime()
	
	if t.tm_min != 5:
		ex_flag = 1 
		pass
	else : 	
		if ex_flag == 1 : 
			ex_flag = 0
			dust = index()
			print str(dust)

			dust = dust.split("\n") 
	
			try :
				for k in range(0, len(dust)-1):
					dust_arr = dust[k].split(" ")
					dust_val = dust_arr[1].strip()
					time.sleep(1)
		
					if k==0 :
						data = {
							"metric": "dust.seoul",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==1:
						data = {
							"metric": "dust.busan",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==2:
						data = {
							"metric": "dust.daegu",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==3:
						data = {
							"metric": "dust.incheon",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==4:
						data = {
							"metric": "dust.gwangju",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==5:
						data = {
							"metric": "dust.daejeon",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==6:
						data = {
							"metric": "dust.ulsan",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==7:
						data = {
							"metric": "dust.gyeonggi",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==8:
						data = {
							"metric": "dust.gangwon",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==9:
						data = {
							"metric": "dust.chungbook",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==10:
						data = {
							"metric": "dust.chungnam",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==11:
						data = {
							"metric": "dust.jeonbook",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==12:
						data = {
							"metric": "dust.jeonnam",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==13:
						data = {
							"metric": "dust.kyeongbook",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==14:
						data = {
							"metric": "dust.kyeongnam",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
					elif k==15:
						data = {
							"metric": "dust.jeju",
							"timestamp": time.time(),
							"value": dust_val,
							"tags": {	
								"host": "mypc"
							}
						}

						ret = requests.post(tsdb_url, data=json.dumps(data))
			except:
				print "error"
				pass



