#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/2 下午4:21
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : air
# @File    : roewe_map
# @Contact : guangze.yu@foxmail.com
"""

from vendor.hefeng.common import CommonKey

Common = CommonKey


class Now(Common):
    """
    环保部1500个监测站点实况数据为免费数据，全国3181个城市实时空气质量指数为付费数据
    """

    def __init__(self, params_dict):
        super(Now, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/air/now'


class Hourly(Common):
    """
    逐小时预报，收费
    """

    def __init__(self, parmas_dict):
        super(Hourly, self).__init__(parmas_dict)
        self._url = 'https://free-api.heweather.com/s6/air/hourly'


class Air(Common):
    def __init__(self, params_dict):
        super(Air, self).__init__(params_dict)
        self._url = 'https://free-api.heweather.com/s6/air/now'
