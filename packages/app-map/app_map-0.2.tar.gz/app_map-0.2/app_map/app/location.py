#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:18
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : location
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""
import traceback
import database.cache as cache
import database.definition as definition
import database.operation as operation
import utils.logger as logger
import utils.decorator as decorator
import utils.exception as exception
import utils.result as result

params_check = decorator.params_check
LOG = logger.get_logger(__name__)


@params_check
def update(params):
    """
       GPS位置更新
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('update service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        # vin = 'LSJA1234567890118'
        print(vin)
        timestamp = params['timestamp']
        if 'location' in params.keys():
            location = params['location']
        else:
            return result.ErrorResult(exception.NoLocationError())
        cache_loc = cache.VehicleLocation(vin)
        cache_loc.set(location)
        LOG.info('vin:%s, location:%s' % (vin, location))
        try:
            CONN = definition.Connect()
            trace = operation.UserTrace(vin=vin, conn=CONN)
            trace.add(location=location, timestamp=timestamp)
            CONN.close()
            return result.CommonResult(res='Success.')
        except Exception:
            traceback.print_exc()
            result.ErrorResult(exception.CacheConnectError())
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


def get(params):
    """
        获取GPS位置
    :param params: timestamp：时间戳，dict 对象
    :return:  json
    """
    LOG.info('get service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        cache_loc = cache.VehicleLocation(vin)
        info = cache_loc.last_loc
        if info is None:
            return result.CommonResult(res='No location info on the remote.')
        else:
            return result.CommonResult(res=info.decode('utf-8'))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
