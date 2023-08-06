#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:16
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : broadcast
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""
import datetime
import traceback
import utils.logger as logger
import utils.exception as exception
import utils.result as result
import utils.decorator as decorator
import database.cache as cache
import database.definition as definition
import database.operation as operation
import app.map_AI as mapai

params_check = decorator.params_check
LOG = logger.get_logger(__name__)


@params_check
def check(params):
    """
        风情播报
    :param params:  broadcast_on：播报id、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('broadcast service:')
    LOG.info('params is %s', params)
    try:
        timestamp = params['timestamp']
        time_array = datetime.datetime.fromtimestamp(timestamp)
        vin = params['vin']
        uid = params['uid']
        if 'broadcast_on' not in params.keys():
            return result.ErrorResult(exception.NoBoradcastOnError())
        if uid is not None:
            uid = params['uid']
            cache_loc = cache.UserLastLocation(uid)
            data = {'uid': params['uid'], 'vin': params['vin'], 'time': time_array}
        else:
            data = {'vin': params['vin'], 'time': time_array}
            cache_loc = cache.VehicleLastLocation(vin)
        if 'location' not in params.keys():
            return result.ErrorResult(exception.NoLocationError())
        last_loc_read = cache_loc.last_loc
        current_loc = params['location']
        cache_loc.set(current_loc)
        if last_loc_read is None:
            last_loc = current_loc
        else:
            last_loc = cache_loc.last_loc.decode('utf-8')
        if int(params['broadcast_on']) != 0:
            city_code = mapai.broadcast(current_loc, last_loc)
            if city_code != 'no broadcast':
                conn = definition.Connect()
                bcity = operation.BroadCity(city_code['citycode'], conn)
                info = bcity.info
                data['citycode'] = city_code['citycode']
                data['adcode'] = info['adcode']
                data['isbroadcast'] = 1
                bcity.history_update(data)
                conn.close()
            else:
                info = 'location update success.'
        else:
            info = 'location update success.'
        return result.CommonResult(res=info)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
