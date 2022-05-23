#!/usr/bin/python
import random

path = "./data/1-mxd.txt"
file = open(path, 'r')
strings = []
for string in file.readlines():
    if len(string.split(',')) == 3:
        strings.append(string.strip('\n'))
file.close()

i = 0
begin = 0
shoots = []
for string in strings:
    tmp = string.split(',')
    if i == len(strings) - 1:
        shoots.append(strings[begin:i])
        break
    if tmp[1] == '-' and i != 0:
        shoots.append(strings[begin:i])
        begin = i
    i += 1

WALKER = 0.1
answer = []
for i in range(len(shoots) * 6):
    shoot = shoots[i % 5]
    for string in shoot:
        tmp = string.split(',')
        if tmp[1] != '-':
            x = float(tmp[0])
            y = float(tmp[1])
            z = float(tmp[2])
            tx = x + random.uniform(-x * WALKER, x * WALKER)
            ty = y + random.uniform(-y * WALKER, y * WALKER)
            tz = z + random.uniform(-z * WALKER, z * WALKER)
            answer.append(",".join([str(round(tx, 2)), str(round(ty, 2)), str(round(tz, 2))]))
        else:
            answer.append(string)

for string in answer:
    print(string)
