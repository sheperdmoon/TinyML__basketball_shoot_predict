import random

import numpy

file_name = input("请输入文本名称\n")
file1 = 'data/' + file_name + '.txt'
# file1_5 = 'data/' + file_name + 'clean.txt'
file2 = 'data/' + file_name + '-30.txt'
# file_w = open(file1_5, 'w')
file_w = open(file2, 'w')
now = []
data_now = []
with open(file1) as lines:
    for line in lines:
        if len(line) >= 2:
            if line[len(line) - 2] == '-':
                if len(now) != 0:
                    data_now.append(now)
                    for i in range(5):
                        # 生成同样维度的随机数组,大小为-5 - 5
                        a = [[(random.random() - 0.5) * 10 for j in range(len(now[0]))] for i in range(len(now))]
                        # 用np.matrix 进行矩阵相加
                        a = numpy.matrix(a)
                        b = numpy.matrix(now)
                        c = a + b
                        # 将新得到的数据附加到data_now中
                        data_now.append(numpy.matrix.tolist(c))
                now = []
                continue
            data = line.split(',')
            now.append([float(i) for i in data[0:3]])
    data_now.append(now)
    for i in range(5):
        # 生成同样维度的随机数组,大小为-5 - 5
        a = [[(random.random() - 0.5) * 10 for j in range(len(now[0]))] for i in range(len(now))]
        # 用np.matrix 进行矩阵相加
        a = numpy.matrix(a)
        b = numpy.matrix(now)
        c = a + b
        # 将新得到的数据附加到data_now中
        data_now.append(numpy.matrix.tolist(c))
# 将data_now（30*70*3） 写入新的文本文件
for one_data in data_now:
    file_w.write(" -,-,-\n")
    for one_line in one_data:
        file_w.write(','.join([str(round(i,2)) for i in one_line])+'\n')
    file_w.write('\n')

