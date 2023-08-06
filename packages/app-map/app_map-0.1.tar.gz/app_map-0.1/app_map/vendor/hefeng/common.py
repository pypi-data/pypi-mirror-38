#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-23 上午9:05
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : hefengAPI
# @Contact : guangze.yu@foxmail.com
"""
import requests
import json
import hashlib, base64
import time
import config.vendor as vendor

KEY = vendor.hefeng_key
UID = vendor.hefeng_uid


class Weather(object):
    def __init__(self, param_dict):
        self._key = KEY
        self._url = 'https://free-api.heweather.com/v5/weather'
        self._param_public = {'key': self._key}
        self._param_private = param_dict

    def get(self):
        param = self._param_public.copy()
        param.update(self._param_private)
        res = requests.get(self._url, param)
        return json.loads(res.content.decode('utf-8'))


class CommonSign(object):
    def __init__(self, param_dict):
        self._key = KEY
        self._uid = UID
        self._url = 'https://free-api.heweather.com/s6/weather/forecast'
        self._param = {'username': self._uid,
                       't': int(time.time())}
        self._param_private = param_dict
        self._param.update(self._param_private)

    def get(self):
        res = requests.get(self._url, self._param)
        return json.loads(res.content.decode('utf-8'))

    def signature(self, params, secret):
        canstring = ''
        params = sorted(params.items(), key=lambda item: item[0])
        for k, v in params:
            if (k != 'sign' and k != 'key' and v != ''):
                canstring += k + '=' + v + '&'
        canstring = canstring[:-1]
        canstring += secret
        md5 = hashlib.md5(canstring).digest()
        return base64.b64encode(md5)


class CommonKey(object):
    def __init__(self, param_dict):
        self._key = KEY
        self._url = 'https://free-api.heweather.com/v5/weather'
        self._param_public = {'key': self._key}
        self._param_private = param_dict

    def get(self):
        param = self._param_public.copy()
        param.update(self._param_private)
        res = requests.get(self._url, param)
        return json.loads(res.content.decode('utf-8'))
