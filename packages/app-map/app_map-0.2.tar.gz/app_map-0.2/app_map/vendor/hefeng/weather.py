#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/2 下午4:02
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : weather
# @File    : roewe_map
# @Contact : guangze.yu@foxmail.com
"""

from vendor.hefeng.common import CommonKey

Common = CommonKey


class Forecast(Common):
    def __init__(self, params_dict):
        super(Forecast, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/weather/forecast'


class Now(Common):
    def __init__(self, params_dict):
        super(Now, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/weather/now'


class Hourly(Common):
    def __init__(self, params_dict):
        """

        :param params_dict:
        """
        # permission denied
        super(Hourly, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/weather/hourly'


class LifeStyle(Common):
    def __init__(self, params_dict):
        super(LifeStyle, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/weather/lifestyle'


class Weather(Common):
    def __init__(self, params_dict):
        super(Weather, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/weather'

#
# params = {'location':'121.18705063770875,31.281607023362948'}
# s = Now(params)
# res = s.get()
# print(res)
