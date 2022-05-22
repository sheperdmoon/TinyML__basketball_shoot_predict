#!/bin/python
import matplotlib.pyplot as plt
import numpy as np


class Data:
    DIMENSION = 3

    def __init__(self, string):
        self.data = []
        self.__parse_string(string)
        self.x, self.y, self.z = self.data

    def getData(self):
        return self.data

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def __parse_string(self, data):
        self.data = data.split(',')
        assert len(self.data) == Data.DIMENSION

    def __str__(self):
        return ",".join(self.data)


class Shoot:
    LENGTH = 100

    def __init__(self, strings):
        self.datas = []
        self.__parse_strings(strings)

    def __parse_strings(self, strings):
        for string in strings:
            self.datas.append(Data(string.strip('\n')))

    def getDatas(self):
        return self.datas

    def __str__(self):
        return "\n".join(map(str, self.datas))

    def drawX(self, ax):
        vertical = [float(data.getX()) for data in self.datas]
        # vertical = []
        # for data in self.datas:
        #     tmp = data.getX()
        #     tmp = float(tmp)
        #     vertical.append(tmp)
        horizontal = range(len(self.datas))
        ax.plot(horizontal, vertical)

    def drawY(self, ax):
        vertical = [float(data.getY()) for data in self.datas]
        horizontal = range(len(self.datas))
        ax.plot(horizontal, vertical)

    def drawZ(self, ax):
        vertical = [float(data.getZ()) for data in self.datas]
        horizontal = range(len(self.datas))
        ax.plot(horizontal, vertical)

    def getX(self, index):
        return float(self.datas[index].getX())

    def getY(self, index):
        return float(self.datas[index].getY())

    def getZ(self, index):
        return float(self.datas[index].getZ())


class People:
    WINDOW_LENGTH = 100

    def __init__(self, files):
        self.files = files
        self.shoots = []
        self.strings = []
        self.__parse_files()

    def __parse_files(self):
        for file in self.files:
            f = open(file, 'r')
            self.strings += [string for string in f.readlines() if (len(string.split(',')) == 3 and string.split(',')[1] != "-")]
            f.close()
        length = len(self.strings)
        print(length)
        for i in range(length // People.WINDOW_LENGTH):
            self.shoots.append(Shoot(self.strings[i * People.WINDOW_LENGTH:(i + 1) * People.WINDOW_LENGTH]))

    def drawX(self):
        fig, ax = plt.subplots()
        for shoot in self.shoots:
            shoot.drawX(ax)
        ax.set_ylabel('accelaration')
        ax.set_title('x dimension')
        # ax.legend()
        plt.show()

    def drawY(self):
        fig, ax = plt.subplots()
        for shoot in self.shoots:
            shoot.drawY(ax)
        ax.set_ylabel('accelaration')
        ax.set_title('y dimension')
        # ax.legend()
        plt.show()

    def drawZ(self):
        fig, ax = plt.subplots()
        for shoot in self.shoots:
            shoot.drawZ(ax)
        ax.set_ylabel('accelaration')
        ax.set_title('z dimension')
        # ax.legend()
        plt.show()

    def drawMeanX(self):
        vertical = []
        for i in range(People.WINDOW_LENGTH):
            meanx = np.mean([shoot.getX(i) for shoot in self.shoots])
            vertical.append(meanx)
        plt.plot(range(People.WINDOW_LENGTH), vertical)
        plt.show()


files = ["./data/2-xzy.txt"]
people = People(files)
people.drawX()
# people.drawY()
# people.drawZ()
people.drawMeanX()
