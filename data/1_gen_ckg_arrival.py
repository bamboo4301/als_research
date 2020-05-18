import csv
from datetime import datetime
cnt = {}
weather = {}
with open('航班起降.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if row[6].isnumeric():
			x = datetime.fromtimestamp(int(row[6])).strftime('%Y-%m-%d')
			if row[1] == 'CKG':
				if x in cnt:
					cnt[x] += 1
				else:
					cnt[x] = 1
with open('天气.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if row[0].replace('"', '') == "重庆":
			weather[row[4].replace('"', '')] = row[1].replace('"', '')
for key in cnt:
	if key in weather:
		print("{},{},{}".format(key,cnt[key],weather[key]))