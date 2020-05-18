from math import exp
from random import random
from readCSV import read_data
import sys

steps = 5000
batch_size = 10
states = (24 + 1) * 60
sys.setrecursionlimit(states * 200)
average_value = []

gamma = 0.5
minLandingInterval = 2

landingRequests = []
planArrival = []
originDelay = []

valueTable = [[0.0] * states, [0.0] * states]
optimalValueTable = []
actionCount = [[0] * states, [0] * states]
runways = [[], []]
waitPlanes = []
requestIndex = 0


def load_data():
    global landingRequests, planArrival, originDelay
    data = read_data()
    landingRequests = data[0]
    planArrival = data[1]
    originDelay = data[2]


def init(state):
    global states, requestIndex, runways, valueTable
    requestIndex = 0
    runways[0].clear()
    runways[1].clear()
    waitPlanes.clear()
    optimalValueTable.append(valueTable)
    valueTable = [[0.0] * states, [0.0] * states]
    value_per_episode(state)


def value_per_episode(state):
    if state % 10 == 0:
        average = 0.0
        tempValueTable = [[0.0] * states, [0.0] * states]
        for i in range(0, 2):
            for j in range(0, states):
                tmp = 0
                for k in range(0, len(optimalValueTable)):
                    tmp += optimalValueTable[k][i][j]
                if actionCount[i][j] > 0:
                    tempValueTable[i][j] = tmp / actionCount[i][j]
        for i in range(0, len(tempValueTable)):
            average += max(tempValueTable[0][i], tempValueTable[1][i])
        print("Episode: %d" % state)
        print("reward per episode: %f" % average)
        average_value.append(average)


def monte_carlo():
    global optimalValueTable
    result = [[0.0] * states, [0.0] * states]
    for i in range(0, 2):
        for j in range(0, states):
            tmp = 0
            for k in range(0, len(optimalValueTable)):
                tmp += optimalValueTable[k][i][j]
            if actionCount[i][j] > 0:
                result[i][j] = tmp / actionCount[i][j]
    optimalValueTable = result


# environment
def check_planes(state):
    global requestIndex
    while requestIndex < len(landingRequests) and landingRequests[requestIndex] == state:
        waitPlanes.append([landingRequests[requestIndex], planArrival[requestIndex]])
        requestIndex += 1


# policy
def pi(state, planes_to_land):
    if len(planes_to_land) > 0:
        if len(runways[0]) == 0:
            runways[0].append(state)
            return [0.5, 0.5, 0, 0]
        elif len(runways[1]) == 0:
            runways[1].append(state)
            return [0.5, 0.5, 1, 0]
        interval0 = min(6, state - runways[0][-1])
        interval1 = min(6, state - runways[1][-1])
        if interval0 >= minLandingInterval and interval0 >= interval1:
            runways[0].append(state)
            return [0.5, 0.5, 0, interval0]
        elif interval1 >= minLandingInterval and interval0 < interval1:
            runways[1].append(state)
            return [0.5, 0.5, 1, interval1]
    return [1, 0, 0, 0]


# state value function
def v(state):
    check_planes(state)
    policy = pi(state, waitPlanes)
    if state == states:
        if policy[1] == 0:
            return 0
        else:
            return q(state, 1, policy[3])
    if policy[1] == 0:
        actionCount[0][state] += 1
        valueTable[0][state] += q(state, 0, 0)
        return valueTable[0][state]
    else:
        # Quick Monte Carlo
        # if actionCount[0][state] < actionCount[1][state]:
        # Standard Monte Carlo
        rand = random()
        if rand > 0.5:
            actionCount[0][state] += 1
            valueTable[0][state] += q(state, 0, policy[3])
            return valueTable[0][state]
        else:
            actionCount[1][state] += 1
            runways[policy[2]].append(state)
            waitPlanes.pop(0)
            valueTable[1][state] += q(state, 1, policy[3])
            return valueTable[1][state]


# action value function
def q(state, action, interval):
    delay = 0
    n = len(waitPlanes)
    if n != 0:
        delay = state - waitPlanes[0][1]
    if state == states:
        return -delay * exp(n)
    elif action == 0:
        return 4 - interval ** 2 + gamma * v(state + 1)
    else:
        return -delay * exp(n) + gamma * v(state + 1)


# optimal policy
def optimal_pi(state, planes_to_land):
    if len(planes_to_land) > 0 and optimalValueTable[0][state] <= optimalValueTable[1][state]:
        if len(runways[0]) == 0:
            runways[0].append(state)
            return [0, 1, 0, 0]
        elif len(runways[1]) == 0:
            runways[1].append(state)
            return [0, 1, 1, 0]
        interval0 = min(6, state - runways[0][-1])
        interval1 = min(6, state - runways[1][-1])
        if interval0 >= minLandingInterval and interval0 >= interval1:
            runways[0].append(state)
            return [0, 1, 0, interval0]
        elif interval1 >= minLandingInterval and interval0 < interval1:
            runways[1].append(state)
            return [0, 1, 1, interval1]
    return [1, 0, 0, 0]


def agent():
    global requestIndex
    requestIndex = 0
    sum_delay = 0
    sum_interval = 0
    runways[0].clear()
    runways[1].clear()
    waitPlanes.clear()
    arrival = []

    for i in range(0, len(optimalValueTable[0])):
        check_planes(i)
        policy = optimal_pi(i, waitPlanes)
        if policy[1] == 1:
            if i > waitPlanes[0][1]:
                sum_delay += i - waitPlanes[0][1]
            sum_interval += policy[3]
            waitPlanes.pop(0)
            arrival.append(i)
    print("origin sum of delay: %d" % (sum(originDelay)))
    print("trained sum of delay: %d" % sum_delay)
    print("trained sum of interval: %d" % sum_interval)
    print(average_value)


def train_agent(train_steps):
    for i in range(0, train_steps):
        v(0)
        init(i)


if __name__ == '__main__':
    load_data()
    train_agent(steps)
    monte_carlo()
    agent()
