import csv
fileName = "data/20170121_2.csv"


def read_data():
    landing_requests = []
    plan_arrival = []
    delay = []
    with open(fileName, "r") as f:
        next(f)
        csv_reader = csv.reader(f)
        for i in csv_reader:
            landing_requests.append(int(i[1])//60)
            plan_arrival.append(int(i[0])//60)
            delay.append(int(i[2])//60)
    return [landing_requests, plan_arrival, delay]
