#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/3 上午8:14
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : solar
# @File    : roewe_map
# @Contact : guangze.yu@foxmail.com
"""

from vendor.hefeng.common import CommonKey

Common = CommonKey


class SunRiseSet(Common):
    def __init__(self, params_dict):
        super(SunRiseSet, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/solar/sunrise-sunset'

# params = {'location':'121.18705063770875,31.281607023362948'}
# s = SunRiseSet(params)
# res = s.get()
# print(res)
