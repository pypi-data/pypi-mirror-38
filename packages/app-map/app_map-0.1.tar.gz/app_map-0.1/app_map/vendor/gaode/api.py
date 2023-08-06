#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/11/27 13:24
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : gaode.
# @Contact : xiangwenzhuo@yeah.net
"""

import requests
import json
import config.vendor as vendor

key = vendor.gaode_key


class Common(object):
    def __init__(self):
        self._key = key
        self._output = 'JSON'
        self._param_public = {'key': self._key, 'output': self._output}
        self._param_private = {}
        self._url = 'http://restapi.amap.com'

    def get(self):
        param = self._param_public.copy()
        param.update(self._param_private)
        res = requests.get(self._url, param)
        return json.loads(res.content.decode('utf-8'))

    def update(self, param_dict):
        self._param_private = param_dict


class Geocode(Common):
    def __init__(self, param_dict):
        """
        地理编码
        :param param_dict: address
        optional param: city, batch
        """
        super(Geocode, self).__init__()
        self._url = 'http://restapi.amap.com/v3/geocode/geo'
        self._param_private = param_dict


class ReGeocode(Common):
    def __init__(self, param_dict):
        """
        逆地理编码
        :param param_dict: location
        optional param: poitype, radius, extensions, batch, roadlevel, homeorcorp
        """
        super(ReGeocode, self).__init__()
        self._url = 'http://restapi.amap.com/v3/geocode/regeo'
        self._param_private = param_dict


class Direction_Driving(Common):
    def __init__(self, param_dict):
        """
        驾车路径规划
        :param param_dict: origin, destination
        optional param: originid, destinationid, origintype, destinationtype, strategy, waypoints,
                        avoidpolygons, avoidroad, province, number
        """
        super(Direction_Driving, self).__init__()
        self._url = 'http://restapi.amap.com/v3/direction/driving'
        self._param_private = param_dict


class District(Common):
    def __init__(self, param_dict):
        """
        行政区域查询
        :param param_dict:
        optional param: keywords, subdistrict, page, offset, extensions, filter
        """
        super(District, self).__init__()
        self._url = 'http://restapi.amap.com/v3/config/district'
        self._param_private = param_dict


class Keywords_Search(Common):
    def __init__(self, param_dict):
        """POI关键字搜索
        :param param_dict: keywords
        optional param: city, citylimit, children, offset, page, building, floor, extensions
        """
        super(Keywords_Search, self).__init__()
        self._url = 'http://restapi.amap.com/v3/place/text'
        self._param_private = param_dict


class Surrounding_Search(Common):
    def __init__(self, param_dict):
        """周边POI搜索
        :param param_dict: location
        optional param: keywords, types, city, radius, sortrule, offset, page, extensions
        """
        super(Surrounding_Search, self).__init__()
        self._url = 'http://restapi.amap.com/v3/place/around'
        self._param_private = param_dict


class Polygon_Search(Common):
    def __init__(self, param_dict):
        """多边形POI搜索
        :param param_dict: polygon
        optional param: keywords, types, offset, page, extensions
        """
        super(Polygon_Search, self).__init__()
        self._url = 'http://restapi.amap.com/v3/place/polygon'
        self._param_private = param_dict


class ID_Search(Common):
    def __init__(self, param_dict):
        """ID查询搜索POI
        :param param_dict: id
        """
        super(ID_Search, self).__init__()
        self._url = 'http://restapi.amap.com/v3/place/detail'
        self._param_private = param_dict


class IP_Location(Common):
    def __init__(self, param_dict):
        """IP定位
        :param param_dict:
        """
        super(IP_Location, self).__init__()
        self._url = 'http://restapi.amap.com/v3/ip'
        self._param_private = param_dict


class Autograsp(Common):
    def __init__(self, param_dict):
        """抓路服务
        :param param_dict: key, carid, location, time, direction, speed
        """
        super(Autograsp, self).__init__()
        self._url = 'http://restapi.amap.com/v3/autograsp'
        self._param_private = param_dict


# class Batch(Common):
#   def __init__(self, param_dict):
#       """批量请求接口
#       :param param_dict:
#       """
#       super(Autograsp, self).__init__()
#       self._url = 'http://restapi.amap.com/v3/autograsp'
#       self._param_private = param_dict


class StaticMap(Common):
    def __init__(self, param_dict):
        """静态地图
        :param param_dict: location
        optional param: zoom, size, scale, markers, labels, paths, traffic
        """
        super(StaticMap, self).__init__()
        self._url = 'http://restapi.amap.com/v3/staticmap'
        self._param_private = param_dict


class Convert(Common):
    def __init__(self, param_dict):
        """坐标转换
        :param param_dict: location
        optional param: coordsys
        """
        super(Convert, self).__init__()
        self._url = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
        self._param_private = param_dict


class Weather(Common):
    def __init__(self, param_dict):
        """天气查询
        :param param_dict: city
        optional param: extensions
        """
        super(Weather, self).__init__()
        self._url = 'http://restapi.amap.com/v3/weather/weatherInfo'
        self._param_private = param_dict


class Inputtips(Common):
    def __init__(self, param_dict):
        """输入提示
        :param param_dict: keywords
        optional param: type, location, city, citylimit, datatype
        """
        super(Inputtips, self).__init__()
        self._url = 'http://restapi.amap.com/v3/assistant/inputtips'
        self._param_private = param_dict


class Rectangle_Traffic(Common):
    def __init__(self, param_dict):
        """矩形区域交通态势
        :param param_dict: rectangle
        optional param: level, extensions
        """
        super(Rectangle_Traffic, self).__init__()
        self._url = 'http://restapi.amap.com/v3/traffic/status/rectangle'
        self._param_private = param_dict


class Circle_Traffic(Common):
    def __init__(self, param_dict):
        """圆形区域交通态势
        :param param_dict: location
        optional param: level, extensions, radius
        """
        super(Circle_Traffic, self).__init__()
        self._url = 'http://restapi.amap.com/v3/traffic/status/circle'
        self._param_private = param_dict


class Road_Traffic(Common):
    def __init__(self, param_dict):
        """指定路线交通态势
        :param param_dict: name, city
        optional param: level, extensions, adcode
        """
        super(Road_Traffic, self).__init__()
        self._url = 'http://restapi.amap.com/v3/traffic/status/road'
        self._param_private = param_dict


class Creat_Geofence(Common):
    def __init__(self, param_dict):
        """创建地理围栏
        :param param_dict: name, (center, radius) or points, repeat or fixed_date
        optional param: enable, valid_time, repeat, time, desc, alert_condition
        """
        super(Creat_Geofence, self).__init__()
        self._url = 'http://restapi.amap.com/v4/geofence/meta'
        self._param_private = param_dict


def test():
    s = {'location': '121.164061,31.294312'}
    res = Surrounding_Search(s)
    answer = res.get()
    print(answer)
    s = {'keywords': '人民广场'}
    res = Keywords_Search(s)
    answer = res.get()
    print(answer)
    s = {'location': '121.164061,31.294312', 'keywords': '银行', 'extensions': 'all'}
    res = Surrounding_Search(s)
    answer = res.get()
    print(answer)


###############################################################################
class Distance(Common):
    def __init__(self, param_dict):
        """
        距离测量
        """
        super(Distance, self).__init__()
        self._url = 'http://restapi.amap.com/v3/distance'
        self._param_private = param_dict


def batch_body_idsearch(inputdict):
    url = '/v3/place/detail?key=' + key + '&output=JSON'
    urls = '&'
    for i in inputdict.items():
        (dkey, value) = i
        temp_str = dkey + "=" + value
        urls = urls + temp_str + "&"
    urls = urls[:-1]
    url = url + urls
    return url


def batch_body_surroudings(inputdict):
    url = '/v3/place/around?key=' + key + '&output=JSON'
    urls = '&'
    for i in inputdict.items():
        (dkey, value) = i
        temp_str = dkey + "=" + value
        urls = urls + temp_str + "&"
    urls = urls[:-1]
    url = url + urls
    return url


def batch_body_keysearch(inputdict):
    url = '/v3/place/text?key=' + key + '&output=JSON'
    urls = '&'
    for i in inputdict.items():
        (dkey, value) = i
        if value is not None:
            temp_str = dkey + "=" + value
            urls = urls + temp_str + "&"
    urls = urls[:-1]
    url = url + urls
    return url


def batch_body_distances(inputdict):
    url = '/v3/distance?key=' + key + '&output=JSON'
    urls = '&'
    for i in inputdict.items():
        (dkey, value) = i
        temp_str = dkey + "=" + value
        urls = urls + temp_str + "&"
    urls = urls[:-1]
    url = url + urls
    return url


def batch_search_surroudings(inputlist):
    url = 'http://restapi.amap.com/v3/batch?key=' + key
    ops = []
    for i in inputlist:
        ops.append({'url': batch_body_surroudings(i)})
    body = json.dumps({'ops': ops})
    res = requests.post(url, data=body)
    return json.loads(res.content.decode('utf-8'))


def batch_search_ids(inputlist):
    url = 'http://restapi.amap.com/v3/batch?key=' + key
    ops = []
    for i in inputlist:
        ops.append({'url': batch_body_idsearch(i)})
    body = json.dumps({'ops': ops})
    res = requests.post(url, data=body)
    return json.loads(res.content.decode('utf-8'))


def batch_search_keys(inputlist):
    url = 'http://restapi.amap.com/v3/batch?key=' + key
    ops = []
    for i in inputlist:
        ops.append({'url': batch_body_keysearch(i)})
    body = json.dumps({'ops': ops})
    res = requests.post(url, data=body)
    return json.loads(res.content.decode('utf-8'))


def batch_distances(inputlist):
    url = 'http://restapi.amap.com/v3/batch?key=' + key
    ops = []
    for i in inputlist:
        ops.append({'url': batch_body_distances(i)})
    body = json.dumps({'ops': ops})
    res = requests.post(url, data=body)
    return json.loads(res.content.decode('utf-8'))
