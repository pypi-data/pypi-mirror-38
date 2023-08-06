#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:24
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : weather
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import vendor.hefeng.air as airapi
import vendor.hefeng.weather as weather
import vendor.hefeng.solar as solar
import utils.logger as logger
import utils.exception as exception
import utils.result as result
import utils.decorator as decorator

LOG = logger.get_logger(__name__)
param_check = decorator.params_check


@param_check
def weather_all(params):
    """
        全部天气
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('all weather service:')
    LOG.info('params is %s', params)
    if 'location' in params:
        params_dict = {'location': params['location']}
    else:
        return result.ErrorResult(exception.NoLocationError())
    try:
        res = weather.Weather(params_dict).get()
        return result.WeatherResult(res=res)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@param_check
def forecast(params):
    """
        10天预报
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('weather service:')
    LOG.info('params is %s', params)
    if 'location' in params:
        params_dict = {'location': params['location']}
    else:
        return result.ErrorResult(exception.NoLocationError())
    try:
        res = weather.Forecast(params_dict).get()
        return result.WeatherResult(res=res)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@param_check
def now(params):
    """
        实况天气
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('weather now service:')
    LOG.info('params is %s', params)
    if 'location' in params:
        params_dict = {'location': params['location']}
    else:
        return result.ErrorResult(exception.NoLocationError())
    try:
        res = weather.Now(params_dict).get()
        return result.WeatherResult(res=res)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@param_check
def air(params):
    """
        空气质量数据集合
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('weather lifestyle service:')
    LOG.info('params is %s', params)
    if 'location' in params:
        params_dict = {'location': params['location']}
    else:
        return result.ErrorResult(exception.NoLocationError())
    try:
        res = airapi.Air(params_dict).get()
        return result.WeatherResult(res=res)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@param_check
def sun_rise_set(params):
    """
        日出日落
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('weather lifestyle service:')
    LOG.info('params is %s', params)
    if 'location' in params:
        params_dict = {'location': params['location']}
    else:
        return result.ErrorResult(exception.NoLocationError())
    try:
        res = solar.SunRiseSet(params_dict).get()
        return result.WeatherResult(res=res)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@param_check
def lifestyle(params):
    LOG.info('weather lifestyle service:')
    LOG.info('params is %s', params)
    if 'location' in params:
        params_dict = {'location': params['location']}
    else:
        return result.ErrorResult(exception.NoLocationError())
    try:
        res = weather.LifeStyle(params_dict).get()
        return result.WeatherResult(res=res)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
