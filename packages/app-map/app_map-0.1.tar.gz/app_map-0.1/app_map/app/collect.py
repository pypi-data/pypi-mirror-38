#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:15
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : collect
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""
import traceback
import database.definition as definition
import database.operation as operation
import utils.exception as exception
import utils.result as result
import utils.decorator as decorator
import utils.logger as logger

params_check = decorator.params_check
LOG = logger.get_logger(__name__)


@params_check
def getpoi(params):
    """
        获取POI收藏记录
    :param params:  timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('get collect poi service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        poilist = operation.UserCollect(vin, uid, conn).get()
        conn.close()
        return result.CommonResult(res=poilist)
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addpoi(params):
    """
        增加poi收藏
    :param params:  poi_id：poiid、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('add collect poi service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        if 'poi_id' in params.keys():
            if params['poi_id'] is not "":
                poi_id = params['poi_id']
            else:
                return result.ErrorResult(exception.NullPoiIdError())
        else:
            return result.ErrorResult(exception.NoPoiIdError())
        if 'location' in params.keys():
            location = params['location']
        else:
            return result.ErrorResult(exception.NoLocationError())
        conn = definition.Connect()
        poi = operation.UserCollect(vin, uid, conn)
        if 'tag' in params:
            poi.add(poi_id, params['tag'])
        else:
            poi.add(poi_id)
        conn.close()
        return result.CommonResult(res='Success.')
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def delpoi(params):
    """
        删除poi收藏
    :param params:  poi_id：poiid、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('delcollectpoi service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        if 'poi_id' in params.keys():
            if params['poi_id'] is not "":
                poi_id = params['poi_id']
            else:
                return result.ErrorResult(exception.NullPoiIdError())
        else:
            return result.ErrorResult(exception.NoPoiIdError())
        conn = definition.Connect()
        poi = operation.UserCollect(vin, uid, conn)
        conn.close()
        if poi.delete(poi_id):
            return result.CommonResult(res='Success.')
        else:
            return result.ErrorResult(exception.SQLConnectError())
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
