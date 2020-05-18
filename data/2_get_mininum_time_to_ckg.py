import csv
from datetime import datetime
min_time = {}
with open('航班起降.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if row[6].isnumeric() and row[5].isnumeric():
			st = row[0]
			if row[1] == 'CKG' and int(row[6])-int(row[5]) > 0:
				if st in min_time:
					min_time[st] = min(min_time[st],int(row[6])-int(row[5]))
				else:
					min_time[st] = int(row[6]) - int(row[5])
unique_set = {}
all_flight = []
with open('航班起降.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if row[1] == 'CKG' and row[6].isnumeric() and row[5].isnumeric():
			datestr = datetime.fromtimestamp(max(int(row[6])-30*60,int(row[5])+min_time[row[0]])).strftime('%Y-%m-%d')
			if datestr == '2017-01-21':
				hash_str = "{}-{}-{}-{}".format(row[0],row[1],row[5],row[6])
				if not hash_str in unique_set:
					unique_set[hash_str] = 1
					all_flight.append(row)
all_flight.sort(key=lambda x:x[6])
print(",".join(["from","to","flight","st","ed","ast","aed","delta","status","time_need","time","delay"]))
last = -1
for flight in all_flight:
	delta = ""
	if last != -1:
		delta = int(flight[6]) - last
	out = flight[0:7]
	out.append(str(delta))#与上个降落航班的间隔时间
	out.append(flight[8])#是否正常航班
	out.append(str(min_time[flight[0]]))#历史最短时间
	out.append(str(int(flight[6]) - int(flight[5])))#本次空中用时
	out.append(str(max(0,int(flight[6]) - int(flight[4]))))#延误时间
	print(",".join(out))
	last = int(flight[6])