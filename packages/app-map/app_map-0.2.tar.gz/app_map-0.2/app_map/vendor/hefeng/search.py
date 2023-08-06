#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/3 上午8:16
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : search
# @File    : roewe_map
# @Contact : guangze.yu@foxmail.com
"""

from vendor.hefeng.common import CommonKey

Common = CommonKey


class Search(Common):
    def __init__(self, params_dict):
        super(Search, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/search'
