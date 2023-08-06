#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/7 15:02
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : decorator
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""

import time
import math
import utils.result as result
import utils.exception as exception
from datetime import datetime


def params_check(func):
    def wrapper(params):
        if 'vin' not in params:
            return result.ErrorResult(exception.NoVinError())
        if 'timestamp' not in params:
            return result.ErrorResult(exception.NoTimeStampError())
        params['timestamp'] = time.time()
        if 'uid' not in params:
            params['uid'] = None
        if 'ip' not in params:
            return result.ErrorResult(exception.NoIpError())
        return func(params)

    return wrapper


def formatTool(pois):
    if len(pois) > 1:
        pois_data = []
        for i in range(len(pois)):
            poidata = eval(
                str(pois[i]).replace("{}", "[]").replace(": []", ": ''").replace("'photos': ''",
                                                                                 "'photos': []").replace(
                    "'title': []", "'title': """))
            pois_data.append(poidata)
        return pois_data
    else:
        poidata = eval(
            str(pois).replace("{}", "[]").replace(": []", ": ''").replace("'photos': ''", "'photos': []").replace(
                "'title': []", "'title': """))
        return poidata


def date_sort(x):
    ls = list(x)
    # 用了冒泡排序来排序，其他方法效果一样
    for j in range(len(ls) - 1):
        for i in range(len(ls) - j - 1):
            lower = datetime.strptime(ls[i + 1]['time'], "%Y-%m-%d %H:%S:%M")
            upper = datetime.strptime(ls[i]['time'], "%Y-%m-%d %H:%S:%M")
            if lower > upper:
                ls[i], ls[i + 1] = ls[i + 1], ls[i]
    return ls


def get_distance_hav(poi_h, use_h, radius):
    EARTH_RADIUS = 6378.137
    Lng_A, Lat_A = poi_h.split(',')
    Lat_B, Lng_B = use_h.split(',')
    radlat1 = math.radians(float(Lat_A))
    radlat2 = math.radians(float(Lat_B))
    a = abs(radlat1 - radlat2)
    b = abs(math.radians(float(Lng_A)) - math.radians(float(Lng_B)))
    s = 2 * math.asin(
        math.sqrt(pow(math.sin(a / 2), 2) + math.cos(radlat1) * math.cos(radlat2) * pow(math.sin(b / 2), 2)))
    s = (round((s * EARTH_RADIUS) * 10000) / 10000) * 1000
    print(s)
    if s <= radius:
        distance_state = True
        return distance_state
    else:
        distance_state = False
        return distance_state


def distinct_search(poi_history, return_info):
    for i in range(len(poi_history)):
        poihistory = poi_history[i]['id']
        for f in range(len(return_info)):
            if f != len(return_info):
                if return_info[f]['id'] == poihistory:
                    del (return_info[f])
            else:
                break
    return poi_history, return_info


class Common():
    _show_num = 0

    @property
    def num(self):
        return self._show_num

    def five(self):
        _show_num = 5
        return _show_num

    def ten(self):
        _show_num = 10
        return _show_num

    def fifteen(self):
        _show_num = 15
        return _show_num

    def twenty(self):
        _show_num = 20
        return _show_num

