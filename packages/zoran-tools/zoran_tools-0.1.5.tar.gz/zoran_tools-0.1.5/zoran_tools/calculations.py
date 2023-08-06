"""
平时写的一些小计算程序放在这里
"""

import math

import matplotlib.pyplot as plt
import numpy as np


def calculate_distance(p1, p2, unit=None):
    """
    calculates the distance using Haversine formula
    使用半正失公式计算地球上两点的距离
    比函数distance要快, 同样计算100万次约比distance函数快2秒
    """

    # get the coordinates
    lat1, lon1 = p1[-1], p1[-2]
    lat2, lon2 = p2[-1], p2[-2]

    # convert to radians
    deltalat_radians = math.radians(lat2 - lat1)
    deltalon_radians = math.radians(lon2 - lon1)

    lat1_radians = math.radians(lat1)
    lat2_radians = math.radians(lat2)

    # apply the formula
    hav = math.sin(deltalat_radians / 2.0) ** 2 + \
          math.sin(deltalon_radians / 2.0) ** 2 * \
          math.cos(lat1_radians) * \
          math.cos(lat2_radians)

    if unit == 'm':
        r = 6371
        dist = 2 * r * math.asin(math.sqrt(hav))
        return int(dist * 1000)
    elif unit == 'km':
        r = 6371  # 地球半径, 以公里计
        dist = 2 * r * math.asin(math.sqrt(hav))
        return float('%.2f' % dist)
    elif unit == 'mile':
        r = 3959  # 地球半径, 以英里计
        dist = 2 * r * math.asin(math.sqrt(hav))
        return float('%.2f' % dist)
    else:
        raise ValueError


class Net(object):
    """
    一个栅栏对象, 即由几个点组成的
    """
    def __init__(self, points, name='net'):
        self.name = name
        self.points = [dict(x=point[0], y=point[1]) for point in points]
        if self.points[0] != self.points[-1]:
            self.points.append(self.points[0])

        self.maxx = max([p[0] for p in points])

        self.lines = [(s, e) for s, e in zip(self.points[:-1], self.points[1:])]
        self.xs = [point['x'] for point in self.points]
        self.ys = [point['y'] for point in self.points]

    @staticmethod
    def intersect(A, B, P, Q):
        """
         判断两条线段AB和PQ是否相交（接触默认为不是相交）
         :param A: dict, 线段AB的起点
         :param B: dict, 线段AB的终点
         :param P: dict, 目标点, 要判断其是否在网格中, PQ的起点
         :param Q: dict, 以P为起点, 水平作一条线段到网格边界(最大横坐标处), 终点为Q
         :return: 返回布尔值是或否
        """
        if (
                (A['y'] > P['y'] and B['y'] > P['y']) or  # AB两点都在PQ上侧
                (A['x'] < P['x'] and B['x'] < P['x']) or  # AB两点都在P左侧
                (A['y'] < P['y'] and B['y'] < P['y'])  # AB两个都在PQ下侧
        ):
            return False
        x = (P['y'] - A['y']) * (B['x'] - A['x']) / (B['y'] - A['y']) + A['x']
        if P['x'] < x <= Q['x']:  # 交点横坐标在PQ两之间
            print('有交点, 且交点在PQ之间', A, B)
            return True
        else:
            return False

    def point_in_net(self, P):
        Q = dict(x=self.maxx, y=P[1])
        P = dict(x=P[0], y=P[1])

        # 计算相交的次数, 如果点P在网格的线上, 认为点在网格内, 直接返回True
        count = 0
        for line in self.lines:
            A, B = line
            if Net.point_in_line(A, B, P):
                print('点在线上')
                return True
            if Net.intersect(A, B, P, Q):
                count += 1

        # 如果PQ与网格的点重合, 会算作相交两次, 所以重合了多少个点, 就要减去多少次
        for point in self.points:
            if point['y'] == P['y'] and (point['x'] - P['x']) * (point['x'] - Q['x']) <= 0:
                count -= 1
        if count % 2 == 1:
            return True
        else:
            return False

    @staticmethod
    def point_in_line(A, B, P):
        if A == P or B == P:
            return True
        if Net.slope(A, B) == Net.slope(A, P) and (A['x'] - P['x']) * (B['x'] - P['x']) < 0:
            return True
        return False

    @staticmethod
    def slope(A, B):
        if A['y'] == B['y']:
            return None
        elif A['x'] == B['x']:
            return 0
        else:
            return (A['y'] - B['y']) / (A['x'] - B['x'])

    def plot(self, P):
        plt.plot(self.xs, self.ys, 'r-o')
        plt.plot([P[0], self.maxx], [P[1], P[1]])
        if self.point_in_net(P):
            plt.title("点在网格中", fontproperties='SimHei')
            isin = True
        else:
            plt.title("点不在网格中", fontproperties='SimHei')
            isin = False
        plt.show()
        return isin


