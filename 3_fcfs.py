import csv
import queue
min_arrival = []
with open('data/20170121.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if row[0] == 'from':
			continue
		flight = row[0:10]
		flight.append(max(int(row[6])-30*60,int(row[5])+int(row[9])))
		min_arrival.append(flight)

min_arrival.sort(key=lambda x:x[10])
n = len(min_arrival)
ptr = 0
q = []
log = []
last = -1
for t in range(1484928000,1484928000+86400):
	while ptr < n:
		if min_arrival[ptr][10] == t:
			q.append(min_arrival[ptr])
			q.sort(key = lambda x:x[4])
			ptr += 1
		else:
			break
	if t % 60 == 0:
		if len(q) > 0:
			cur = q[0]
			q.pop(0)
			delta = ""
			if last != -1:
				delta = str(t - last)
			cur[6] = t
			cur[7] = delta
			cur[10] = t - int(cur[5])
			cur.append(max(0,t - int(cur[4])))
			log.append(cur)
			last = t
		if len(q) > 0:
			cur = q[0]
			q.pop(0)
			delta = ""
			if last != -1:
				delta = str(t - last)
			cur[6] = t
			cur[7] = delta
			cur[10] = t - int(cur[5])
			cur.append(max(0,t - int(cur[4])))
			log.append(cur)
			last = t
for x in log:
	print(",".join([str(y) for y in x]))