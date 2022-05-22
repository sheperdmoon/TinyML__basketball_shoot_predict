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
"""Load data from the specified paths and format them for training."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import numpy as np
import tensorflow as tf

from data_augmentation import augment_data

LABEL_NAME = "gesture"
DATA_NAME = "accel_ms2_xyz"


class DataLoader(object):
    """Loads data and prepares for training."""

    def __init__(self, train_data_path, valid_data_path, test_data_path,
                 seq_length):
        self.dim = 3
        self.seq_length = seq_length
        self.label2id = {"lyl": 0, "xzy": 1, "xmh": 2, "ljr": 3, "mxd": 4, "negative": 5}  # TODO[8] 修改手势标签
        self.train_data, self.train_label, self.train_len = self.get_data_file(
            train_data_path, "train")
        self.valid_data, self.valid_label, self.valid_len = self.get_data_file(
            valid_data_path, "valid")
        self.test_data, self.test_label, self.test_len = self.get_data_file(
            test_data_path, "test")

    def get_data_file(self, data_path, data_type):  # 这边的data，其实就是输入的数据了，没有其他label，就单纯的128*3
        """Get train, valid and test data from files."""
        data = []
        label = []
        with open(data_path, "r") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):  # pylint: disable=unused-variable
                dic = json.loads(line)
                data.append(dic[DATA_NAME])
                label.append(dic[LABEL_NAME])
        if data_type == "train":
            data, label = augment_data(data, label)  # 数据增强的地方 只对train数据有效
        length = len(label)
        print(data_type + "_data_length:" + str(length))
        return data, label, length

    def pad(self, data, seq_length, dim):
        """Get neighbour padding."""
        # TODO [n] 噪声水平可以修改，毕竟投篮的最高值可以到达4000，魔杖可能堪堪2000
        noise_level = 20
        padded_data = []
        # Before- Neighbour padding
        #print(seq_length, " ", dim)
        #print(data[0])
        #print(len(data))
        tmp_data = (np.random.rand(seq_length, dim) - 0.5) * noise_level + data[0]

        tmp_data[(seq_length -
                  min(len(data), seq_length)):] = data[:min(len(data), seq_length)]
        padded_data.append(tmp_data)
        # After- Neighbour padding
        tmp_data = (np.random.rand(seq_length, dim) - 0.5) * noise_level + data[-1]
        tmp_data[:min(len(data), seq_length)] = data[:min(len(data), seq_length)]
        padded_data.append(tmp_data)
        return padded_data

    def format_support_func(self, padded_num, length, data, label):
        """Support function for format.(Helps format train, valid and test.)"""
        # Add 2 padding, initialize data and label
        length *= padded_num  # TODO[10] 为什么要这样做？其实就是将数据前移跟后移
        features = np.zeros((length, self.seq_length, self.dim))
        labels = np.zeros(length)
        # Get padding for train, valid and test
        for idx, (data, label) in enumerate(zip(data, label)):
            if data == []:
                print(label)
                continue
            padded_data = self.pad(data, self.seq_length, self.dim)
            for num in range(padded_num):
                features[padded_num * idx + num] = padded_data[num]
                labels[padded_num * idx + num] = self.label2id[label]
        # Turn into tf.data.Dataset
        dataset = tf.data.Dataset.from_tensor_slices(
            (features, labels.astype("int32")))  # TODO[11] 这边把标签也写入数据中
        return length, dataset

    def format(self):
        """Format data(including padding, etc.) and get the dataset for the model."""
        padded_num = 2
        self.train_len, self.train_data = self.format_support_func(
            padded_num, self.train_len, self.train_data, self.train_label)
        self.valid_len, self.valid_data = self.format_support_func(
            padded_num, self.valid_len, self.valid_data, self.valid_label)
        self.test_len, self.test_data = self.format_support_func(
            padded_num, self.test_len, self.test_data, self.test_label)
