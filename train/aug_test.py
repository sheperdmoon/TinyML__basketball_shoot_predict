# Lint as: python3
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=g-bad-import-order
"""Data augmentation that will be used in data_load.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

import numpy as np
from matplotlib import pyplot as plt

from data_prepare import write_data, prepare_original_data


def draw(title, _x, _y):
    # 画图代码
    # print(data.head()) #可以先看看表的前几行，看有没有载入对
    plt.plot(_x, _y)  # 连线图,若要散点图将此句改为：plt.scatter(x,y) #散点图
    plt.grid(alpha=0.5, linestyle='-.')  # 网格线，更好看
    plt.title(title, fontsize=14)  # 画总标题 fontsize为字体，下同
    plt.xlabel("x", fontsize=14)  # 画横坐标
    plt.ylabel("y", fontsize=14)  # 画纵坐标
    plt.savefig(title + '.jpg', dpi=300)  # 可以存到本地，高清大图。路径默认为当前路径，dpi可理解为清晰度


def time_wrapping(molecule, denominator, data):
    """Generate (molecule/denominator)x speed data."""
    tmp_data = [[0 for i in range(len(data[0]))]
                for j in range((int(len(data) / molecule) - 1) * denominator)]
    for i in range(int(len(data) / molecule) - 1):
        for j in range(len(data[i])):
            for k in range(denominator):
                tmp_data[denominator * i +
                         k][j] = (data[molecule * i + k][j] * (denominator - k) +
                                  data[molecule * i + k + 1][j] * k) / denominator
    return tmp_data


def augment_data(original_data,title):
    """Perform data augmentation."""
    new_data = []
    aug_data = []
    for data in (original_data):  # pylint: disable=unused-variable
        # Original data
        new_data.append(data)
        aug_data.append(data)
        # Sequence shift
        for num in range(5):  # pylint: disable=unused-variable
            new_data.append((np.array(data, dtype=np.float32) +
                             (random.random() - 0.5) * 200).tolist())
            aug_data.append((np.array(data, dtype=np.float32) +
                             (random.random() - 0.5) * 200).tolist())

        # Random noise
        tmp_data = [[0 for i in range(len(data[0]))] for j in range(len(data))]
        for num in range(5):
            for i in range(len(tmp_data)):
                for j in range(len(tmp_data[i])):
                    tmp_data[i][j] = data[i][j] + 5 * random.random()
            new_data.append(tmp_data)
        # Time warping
        fractions = [(3, 2), (5, 3), (2, 3), (3, 4), (9, 5), (6, 5), (4, 5)]
        for molecule, denominator in fractions:
            new_data.append(time_wrapping(molecule, denominator, data))

        # Movement amplification
        for molecule, denominator in fractions:
            new_data.append(
                (np.array(data, dtype=np.float32) * molecule / denominator).tolist())

    for item1 in aug_data[0:7]:
        xlist = []
        for item2 in item1:
            xlist.append(item2[0])
        x_alias = list(range(1, len(xlist) + 1))
        draw("check_augment_x_ss"+title, x_alias, xlist)



now = []
data_now = []
with open("xzy/output_xzy_xuzy.txt") as lines:
    for line in lines:
        if len(line) >= 2:
            if line[len(line) - 2] == '-':
                if len(now) != 0:
                    data_now.append(now)
                now = []
                continue
            data = line.split(',')
            now.append([float(i) for i in data])
if len(now) != 0:
    data_now.append(now)
augment_data(data_now,"xzy")
