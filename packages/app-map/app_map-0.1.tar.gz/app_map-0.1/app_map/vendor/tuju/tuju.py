#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/21 12:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : tuju
# @Project : app_map
# @Contact : guangze.yu@foxmail.com
"""
import requests
import json


class Common(object):
    def __init__(self, param_dict):
        self._http_body = param_dict
        self._http_params = param_dict
        self._url = 'http://api.st.97ting.com:8001/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'

    def post(self):
        res = json.loads(requests.post(url=self._url,
                                       json=self._http_body
                                       ).content.decode('utf-8'))
        return res

    def get(self):
        param = self._http_params
        res = requests.get(self._url, param)
        return json.loads(res.content.decode('utf-8'))


class GPSUpdate(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain location, uid, floor
        location:
        uid:
        floor:
        """
        super(GPSUpdate, self).__init__(param_dict)
        self._http_body = param_dict
        if 'uid' not in self._http_body:
            self._http_body['uid'] = 123456

        self._url = 'http://106.14.183.222:10008/location'

    def get(self):
        print('GET method is not supported.')
        return


class Navi(Common):
    def __init__(self, param_dict):
        """

        :param param_dict:
        """
        super(Navi, self).__init__(param_dict)
        self._http_params = param_dict
        self._url = 'https://apinagrand.ipalmap.com/navi'

    def post(self):
        print('POST method is not supported.')
        return

#
# params = {'from_x': 13515977.901135772,
#           'from_y': 3661232.6252974896,
#           'from_floor': 3657658,
#           'to_x:': 13516080.702578673,
#           'to_y': 3661193.924576937,
#           'to_floor': 3657658}
#
# a = Navi(params)
# b = a.get()
# print(b)
# params = {"location": "121.233132,31.779212",
#           "uid": 123456,
#           "floor": -1}
# c = GPSUpdate(params)
# d = c.post()
# print(d)
