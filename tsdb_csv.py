#!/usr/bin/python

import csv
import urllib2
import time
import sys
from datetime import datetime, timedelta


def load_data(metric, start, end):
	
	def dataParser(s):
		s = s.split("{")
		i = 0
		j = len(s)

		if j > 2:
			s = s[3].replace("}","")
			s = s.replace("]","")
		else:
			return '0:0,0:0'
		return s
	
	#url = 'http://125.7.128.53:4242/api/query?start=2015/05/01-00:00:00&end=2015/06/01-09:46:13&m=sum:F1_R2_BLOCK_41_Cycle_Time'
	#url = 'http://125.7.128.53:4242/api/query?start=%s&end=%s&m=sum:%s' % (start, end, metric)
	url = 'http://127.0.0.1:4242/api/query?start=%s&end=%s&m=sum:%s' % (start, end, metric)

	try:
		u = urllib2.urlopen(url)
	except:
		pass

	data = u.read()
	packets = dataParser(data)
	res = {}
	i = 0

	for l in packets.split(','):
		k, v = l.split(':')
		k = eval(k)
		v = eval(v)
		res[k] = v

	return res


METRICS = {}
volubility = len(sys.argv)


if volubility is 1 :
	print "  Example> python tsdb_csv.py {metric}       {from}     {to}"
	print "         > python tsdb_csv.py F1_R2_BLOCK_41 2015/06/01 2015/06/02"
	print "         > python tsdb_csv.py F2_R2_BLOCK_41 2015/06/01 2015/06/02"
	print "         > python tsdb_csv.py F1_R2_BLOCK_50 2015/06/01 2015/06/02"
	print "         > python tsdb_csv.py F2_R2_BLOCK_50 2015/06/01 2015/06/02"
	exit()

if volubility > 3:
	in_metric = sys.argv[1]
	in_start = sys.argv[2] + '-00:00:00'
	in_end = sys.argv[3] + '-00:00:00'

	#csv_name = sys.argv[1].replace('/','-') + "_" + sys.argv[2] + "-" + sys.argv[3] + '.csv'
	csv_start = sys.argv[2].replace('/','-')
	csv_end = sys.argv[3].replace('/','-')
	
	csv_name = in_metric + '-'+ csv_start + '_' + csv_end + '.csv' 

	print "  sys.argv[%d],pckType = %s" % (1, in_metric)
	print "  sys.argv[%d],pckType = %s" % (2, in_start)
	print "  sys.argv[%d],pckType = %s" % (3, in_end)


#metric_41 = 'F2_R2_BLOCK_41' 

#METRIC_41 = 'F1_R2_BLOCK_41' 
#startTime = '2015/06/01-09:55:00' 
#endTime = '2015/06/01-10:55:00' 

#startTime = '185m-ago' # 3h 5m
#endTime = '5m-ago' # 5m

#METRICS['etype1'] = load_data('gyu_RC1_thl.temperature', 820, '2015/06/01-09:55:00', '2015/06/01-09:56:00')
#METRICS['etype2'] = load_data('gyu_RC1_thl.temperature', 830, '2015/06/01-09:55:00', '2015/06/01-09:56:00')


if in_metric == 'F1_R2_BLOCK_41' or in_metric == 'F2_R2_BLOCK_41' :
	METRICS['Snum'] = load_data(in_metric + '_Snum', in_start, in_end)
	METRICS['CycleTime'] = load_data(in_metric + '_Cycle_Time', in_start, in_end )
	METRICS['MakeTime'] = load_data(in_metric + '_Make_Time', in_start, in_end)
	METRICS['RotTime'] = load_data(in_metric + '_Rot_Time', in_start, in_end)
	METRICS['MakeLoc'] = load_data(in_metric + '_Make_Loc', in_start, in_end)
	METRICS['VpPosi'] = load_data(in_metric + '_Vp_Posi', in_start, in_end)
	METRICS['VcPosi'] = load_data(in_metric + '_Vc_Posi', in_start, in_end)
	METRICS['Remain'] = load_data(in_metric + '_Remain', in_start, in_end)
	METRICS['MakePres'] = load_data(in_metric + '_Make_Pres', in_start, in_end)
	METRICS['VpSwPres'] = load_data(in_metric + '_Vp_Sw_pres', in_start, in_end)
	METRICS['BackPres'] = load_data(in_metric + '_Back_Pres', in_start, in_end)
	METRICS['MoldInPres'] = load_data(in_metric + '_Mold_In_Pres',in_start, in_end)

elif in_metric == 'F1_R2_BLOCK_50' or in_metric == 'F2_R2_BLOCK_50' :
	METRICS['Snum'] = load_data(in_metric + '_Snum', in_start, in_end)
	METRICS['NHTemp'] = load_data(in_metric + '_NH_Temp', in_start, in_end)
	METRICS['H1Temp'] = load_data(in_metric + '_H1_Temp', in_start, in_end)
	METRICS['H2Temp'] = load_data(in_metric + '_H2_Temp', in_start, in_end)
	METRICS['H3Temp'] = load_data(in_metric + '_H3_Temp', in_start, in_end)
	METRICS['H4Temp'] = load_data(in_metric + '_H4_Temp', in_start, in_end)
	METRICS['MoldTemp1'] = load_data(in_metric + '_Mold_Temp1', in_start, in_end)
	METRICS['MoldTemp2'] = load_data(in_metric + '_Mold_Temp2', in_start, in_end)
	METRICS['GasTemp'] = load_data(in_metric + '_Gas_Temp', in_start, in_end)
	METRICS['LNHTemp'] = load_data(in_metric + '_LNH_Temp', in_start, in_end)
	METRICS['HopperTemp'] = load_data(in_metric + '_Hopper_Temp', in_start, in_end)
	METRICS['HVTemp'] = load_data(in_metric + '_HV_Temp', in_start, in_end)
	METRICS['ReservedTemp1'] = load_data(in_metric + '_Reserved_Temp1', in_start, in_end)
	METRICS['ReservedTemp2'] = load_data(in_metric + '_Reserved_Temp2', in_start, in_end)
else :
	print " no metics "
	exit()


with open(csv_name, 'w') as csvfile:
	fieldnames = ['time'] + sorted(METRICS.keys())
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	all_times = []
	for metricName in METRICS.keys():
		times = METRICS[metricName].keys()
		#val = METRICS[metricName].values()
		all_times += times
	all_times = sorted(list(set(all_times)))
	
	for t in all_times:
		ctx = {}
		csv_t = datetime.fromtimestamp(float(t)).strftime('%Y/%m/%d-%H:%M:%S')
		ctx['time'] = csv_t
		
		for metricName in METRICS.keys():
			if t in METRICS[metricName]:
				ctx[metricName] = METRICS[metricName][t]
		writer.writerow(ctx)
