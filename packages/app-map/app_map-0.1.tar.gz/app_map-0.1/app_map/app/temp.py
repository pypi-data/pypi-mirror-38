#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-12 下午3:47
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : service
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import database.cache as cache
import database.operation as operation
import database.definition as definition
import utils.logger as logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def gpsupdate(params):
    LOG.info('gpsupdate service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        # vin = 'LSJA1234567890118'
        timestamp = params['timestamp']
        if 'location' in params.keys():
            location = params['location']
        else:
            return result.ErrorResult(exception.NoLocationError())
        cache_loc = cache.VehicleLocation(vin)
        cache_loc.set(location)
        LOG.info('vin:%s, location:%s' % (vin, location))
        try:
            conn = definition.Connect()
            trace = operation.UserTrace(vin=vin, conn=conn)
            trace.add(location=location, timestamp=timestamp)
            conn.close()
        except:
            pass
        return result.CommonResult(res='Success.')
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getgps(params):
    LOG.info('getgps service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        cache_loc = cache.VehicleLocation(vin)
        info = cache_loc.last_loc
        print(info)
        if info is None:
            return result.ErrorResult(exception.NoLocationError())
        else:
            return result.TempResult(res=info.decode('utf-8'))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


def invalid(params):
    LOG.info('invalid service:')
    LOG.info('params is %s', params)
    return result.ErrorResult(exception.InValidServiceError())


def getvehicles(params):
    LOG.info('getvehicles service:')
    LOG.info('params is %s', params)
    try:
        vinall = cache.VehicleKeys('park').get()
        return result.TempResult(res=vinall)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def gettrace(params):
    LOG.info('gettrace service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        conn = definition.Connect()
        trace = operation.UserTrace(vin=vin, conn=conn)
        data = trace.get()
        conn.close()
        print(data)
        return result.TempResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def selfgettrace(params):
    LOG.info('selfgettrace service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        num = params['datanum']
        conn = definition.Connect()
        trace = operation.UserTrace(vin=vin, conn=conn)
        data = trace.getn(datanum=num)
        print(data)
        conn.close()
        return result.TempResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


