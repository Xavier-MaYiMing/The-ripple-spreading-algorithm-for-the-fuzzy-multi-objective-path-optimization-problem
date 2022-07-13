#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/14 20:49
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : fuzzy_distance.py
# @Statement : the ranking of fuzzy numbers
import math


def dis3(a, b):
    """
    calculate the fuzzy distance between two triangular fuzzy numbers a and b
    :param a:
    :param b:
    :return:
    """
    result = 0
    for i in range(3):
        result += (a[i]-b[i]) ** 2
    result += (a[2] - b[2]) ** 2
    result += (a[0] - b[0]) * (a[1] - b[1])
    result += (a[1] - b[1]) * (a[2] - b[2])
    return math.sqrt(result / 6)


def dis4(a, b):
    """
    calculate the fuzzy distance between two trapezoidal fuzzy numbers a and b
    :param a:
    :param b:
    :return:
    """
    result = 0
    for i in range(4):
        result += (a[i] - b[i]) ** 2
    result += (a[0] - b[0]) * (a[1] - b[1])
    result += (a[2] - b[2]) * (a[3] - b[3])
    return math.sqrt(result / 6)


def graded3(a):
    """
    calculate the graded mean value of the triangular fuzzy number a
    :param a:
    :param b:
    :return:
    """
    return (a[0] + 4 * a[1] + a[2]) / 6


def graded4(a):
    """
    calculate the graded mean value of the trapezoidal fuzzy number a
    :param a:
    :param b:
    :return:
    """
    return (a[0] + 2 * a[1] + 2 * a[2] + a[3]) / 6
