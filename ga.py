import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plan_time = []  # 每架飞机计划降落时间
arrival_time = []  # 每架飞机到达上空的时间
total = 0


data = pd.read_csv("./data/20170121_1.csv", encoding='gbk')
data = np.array(data)
plan_time = data[0:, 4]
arrival_time = data[0:, 12]
total = len(plan_time)  # 基因个数（即飞机个数）

# 初始化原始种群基因
def ori_popular_gene(num):
    popular = []
    s = [x for x in range(1, total+1)]
    for i in range(num):
        random.shuffle(s)
        temp = s.copy()
        popular.append(temp)
    return popular


# 计算适应度函数
def get_fitness(popular_gene):
    fitness = []
    for gene in popular_gene:
        value = 0
        track_choice = []  # 每架飞机选择的跑道
        now_time = [arrival_time[gene[0]-1], arrival_time[gene[0]-1]]
        for i in gene:
            min_track = now_time.index(min(now_time))  # 选择最不拥挤的跑道
            track_choice.append(min_track)  # 记录当前飞机选择的跑道
            value += abs(max(arrival_time[i-1], now_time[min_track]) + 60 - plan_time[i-1])
            now_time[min_track] += max(arrival_time[i-1], now_time[min_track]) + 60
        fitness.append(1*100000000 / value)  # 与计划时间偏离越大，个体适应度越低
    return fitness

def get_delay(gene):
    delay = []
    now_time = [arrival_time[gene[0]-1], arrival_time[gene[0]-1]]
    for i in gene:
        min_track = now_time.index(min(now_time))
        delay.append(abs(max(arrival_time[i-1], now_time[min_track]) + 60 - plan_time[i-1]))
        now_time[min_track] = max(arrival_time[i-1], now_time[min_track]) + 60
    return delay


# 选择and交叉，选择用轮牌赌，交叉概率为0.7
def choice_ex(popular_gene):
    fitness = get_fitness(popular_gene)
    sum_fit_value = sum(fitness)
    # 各个个体被选择的概率
    probability = []
    for i in range(len(fitness)):
        probability.append(fitness[i] / sum_fit_value)
    # 概率分布
    probability_sum = []
    for i in range(len(fitness)):
        if i == 0:
            probability_sum.append(probability[i])
        else:
            probability_sum.append(probability_sum[i-1] + probability[i])
    # 选择
    popular_new = []
    for i in range(int(len(fitness)/2)):
        temp = []  # 选择父代
        for j in range(2):
            rand = random.uniform(0, 1)
            # 轮盘赌
            for k in range(len(fitness)):
                if k == 0:
                    if rand < probability_sum[k]:
                        temp.append(popular_gene[k])
                        break
                else:
                    if probability_sum[k - 1] <= rand <= probability_sum[k]:
                        temp.append(popular_gene[k])
                        break
        # 两点交叉，交叉率为0.7
        son1, son2 = ex(temp[0], temp[1])
        popular_new.append(son1)
        popular_new.append(son2)
    return popular_new


# 交叉操作
def ex(parent1, parent2):
    mod = [random.randint(0, 1) for i in range(0, total)]
    son1 = [0 for i in range(0, total)]
    son2 = [0 for i in range(0, total)]
    son_set_1 = set()
    son_set_2 = set()
    is_change = random.uniform(0, 1)
    if is_change < 0.7:
        for i in mod:
            if i == 1:
                son1[i] = parent1[i]
                son_set_1.add(parent1[i])
            else:
                son2[i] = parent2[i]
                son_set_2.add(parent2[i])
        for i in range(len(mod)):
            if son1[i] == 0:
                for j in range(len(parent2)):
                    if parent2[j] not in son_set_1:
                        son1[i] = parent2[j]
                        son_set_1.add(parent2[j])
                        break
            if son2[i] == 0:
                for j in range(len(parent1)):
                    if parent1[j] not in son_set_2:
                        son2[i] = parent1[j]
                        son_set_2.add(parent1[j])
                        break
    else:
        son1 = parent1
        son2 = parent2
    i = 0
    while i < total-1:
        if son1[i] - son1[i+1] > 6:
            t = son1[i]
            son1[i] = son1[i+1]
            son1[i+1] = t
        else:
            i += 1
    i = 0
    while i < total-1:
        if son2[i] - son2[i+1] > 6:
            t = son2[i]
            son2[i] = son2[i+1]
            son2[i+1] = t
        else:
            i += 1
    return son1, son2



# 变异.概率为0.01
def variation(popular_new):
    for i in range(len(popular_new)):
        is_variation = random.uniform(0, 1)
        if is_variation < 0.01:
            # 随机选定位置进行变异
            rand = random.randint(0, total-1)
            t = popular_new[i][rand]
            popular_new[i][rand] = popular_new[i][(rand+1) % total]
            popular_new[i][(rand+1) % total] = t
    return popular_new


if __name__ == '__main__':
    # 初始化原始种群, 一百个个体
    num = 100
    average = []
    current_best = []
    popular_new = ori_popular_gene(num)
    best = []
    for i in range(1000):  # 繁殖1000代
         popular_new = choice_ex(popular_new)
         popular_new = variation(popular_new)
         fitness = get_fitness(popular_new)
         sum_fitness = sum(fitness)
         average.append(sum_fitness/len(fitness))
         current_best.append(max(fitness))
         index = fitness.index(max(fitness))
         get_delay(popular_new[index])
         print(popular_new[index])  # 输出当前种群中的最优个体
         best = popular_new[index]
         get_delay(best)

