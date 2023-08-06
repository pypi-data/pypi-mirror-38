#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:15
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : usualaddress
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
def getaddress(params):
    """
        获取家和公司地址
    :param params:
    :return:  json
    """
    LOG.info('get usual address service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        poilist = operation.UsualAddress(vin, uid, conn).get()
        conn.close()
        return result.CommonResult(res=poilist)
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addhomeaddress(params):
    """
        增加家地址
    :param params:
    :return:  json
    """
    LOG.info('add home service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        timestamp = params['timestamp']
        if 'poi_id' in params.keys():
            poi_id = params['poi_id'].replace(" ", "")
            if poi_id is "" or poi_id is None:
                poi_id = ""

        if 'address' in params.keys():
            address = params['address'].replace(" ", "")
            if address is "" or address is None:
                address = ""

        if (poi_id is "" or poi_id is None) and (address is "" or address is None):
            return result.ErrorResult(exception.NullKeyOrTypeError())
        else:
            conn = definition.Connect()
            operation.UsualAddress(vin, uid, conn).add(poi_id=poi_id, address=address, timestamp=timestamp, type="1")
            conn.close()
        return result.CommonResult(res='Success.')
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addcompanyaddress(params):
    """
        增加公司地址
    :param params:
    :return:  json
    """
    LOG.info('add company service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        timestamp = params['timestamp']
        if 'poi_id' in params.keys():
            poi_id = params['poi_id'].replace(" ", "")
            if poi_id is "" or poi_id is None:
                poi_id = ""

        if 'address' in params.keys():
            address = params['address'].replace(" ", "")
            if address is "" or address is None:
                address = ""

        if (poi_id is "" or poi_id is None) and (address is "" or address is None):
            return result.ErrorResult(exception.NullKeyOrTypeError())
        else:
            conn = definition.Connect()
            operation.UsualAddress(vin, uid, conn).add(poi_id=poi_id, address=address, timestamp=timestamp, type="2")
            conn.close()
        return result.CommonResult(res='Success.')
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def delhomeaddress(params):
    """
        删除家地址
    :param params:
    :return:  json
    """
    LOG.info('del home service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        type = "1"
        # if 'type' in params.keys():
        #         #     type = params['type'].replace(" ", "")
        #         #     if type is "" or type is None:
        #         #         return result.ErrorResult(exception.NullTypeError())
        conn = definition.Connect()
        operation.UsualAddress(vin, uid, conn).clear(type=type)
        conn.close()
        return result.CommonResult(res='Success.')
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def delcompanyaddress(params):
    """
        删除公司地址
    :param params:
    :return:  json
    """
    LOG.info('del company service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        type = "2"
        # if 'type' in params.keys():
        #     if params['type'] is not "":
        #         type = params['type']
        # else:
        #     return result.ErrorResult(exception.NullTypeError())
        conn = definition.Connect()
        operation.UsualAddress(vin, uid, conn).clear(type=type)
        conn.close()
        return result.CommonResult(res='Success.')
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
