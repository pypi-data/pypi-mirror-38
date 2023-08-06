#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:14
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : poihistory
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import datetime
import json
import utils.logger as logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception
import database.definition as definition
import database.operation as operation
import vendor.gaode.api as gaode

params_check = decorator.params_check
LOG = logger.get_logger(__name__)


@params_check
def get(params):
    """
        获取POI历史记录
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('get service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        if 'offset' in params:
            offset = params['offset']
        else:
            offset = decorator.Common().ten()
        if 'page' in params:
            page = int(params['page'])
        else:
            page = 1

        conn = definition.Connect()
        # 关键字历史
        keyword = operation.SearchWordHistory(vin, uid, conn).get()
        for k in keyword:
            k['sqtype'] = 'KEYWORD'
        # poi历史
        poi_history = operation.PoiHistory(vin, uid, conn).get()
        for p in poi_history:
            p['sqtype'] = 'POI'
        conn.close()
        #
        history_list = []
        history_list.extend(keyword)
        history_list.extend(poi_history)

        #   排序
        poi_history_data = decorator.date_sort(history_list)

        res = json.loads(json.dumps(poi_history_data).replace('NaN', '""'),
                         encoding='utf-8')
        if len(res) >= offset:
            first_item = offset * (page - 1)
            last_item = min(offset * page, len(res))
            res_page = res[first_item:last_item]
        else:
            res_page = res

        return result.HistoryResult(res=res_page, count=len(res))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def clear(params):
    """
       清空POI历史记录
    :param params: timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('clear service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        conn = definition.Connect()
        res = operation.PoiHistory(vin, uid, conn).clear()
        operation.SearchWordHistory(vin, uid, conn).clear()
        conn.close()
        if res:
            return result.CommonResult(res='Success.')
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def delete(params):
    """
        删除POI历史记录
    :param params: poi_id：pooiid、keywords：关键字、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('delete service:')
    LOG.info('params is %s', params)
    try:
        timestamp = params['timestamp']
        time_array = datetime.datetime.fromtimestamp(timestamp)
        vin = params['vin']
        uid = params['uid']
        conn = definition.Connect()
        poi_id = ""
        keyword = ""

        if 'poi_id' in params.keys():
            poi_id = params['poi_id']
        if 'keywords' in params.keys():
            keyword = params['keywords']

        if poi_id is not "" and keyword is "":
            query = conn.session.query(definition.PoiHistory)
            poi_his = query.filter_by(poi_id=poi_id,
                                      vin=params['vin'],
                                      uid=params['uid'],
                                      valid=True).all()
            for i in poi_his:
                i.valid = False
            conn.commit()
            conn.close()
            return result.CommonResult(res='Success.')
        elif poi_id is "" and keyword is not "":
            af = operation.SearchWordHistory(vin, uid, conn).clear(keywords=keyword)
            return result.CommonResult(res='Success.')
        elif poi_id is "" and keyword is "":
            return result.ErrorResult(exception.NullKeywordsOrPoiIdError())
        elif poi_id is not "" and keyword is not "":
            return result.ErrorResult(exception.ParameterTooMuchError())

    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def add(params):
    """
        增加POI历史记录
    :param params:  poi_id：poiid、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('add service:')
    LOG.info('params is %s', params)
    try:
        timestamp = params['timestamp']
        time_array = datetime.datetime.fromtimestamp(timestamp)
        if 'poi_id' not in params.keys():
            return result.ErrorResult(exception.NoPoiIdError())
        else:
            try:
                conn = definition.Connect()
                poi = gaode.ID_Search({'id': params['poi_id']}).get()['pois'][0]
                poi_name = poi['name']
                poi_type = poi['type']
                poi_location = poi['location']
                used_location = params['location'] if 'location' in params else None
                poi_photo_1 = poi['photos'][0]['url']
                poi_photo_2 = poi['photos'][1]['url']
                poi_photo_3 = poi['photos'][2]['url']
                poi_tag = poi['tag']
                poi_cost = poi['biz_ext']['cost']
                poi_rating = poi['biz_ext']['rating']
                add_poi = operation.insert(definition.Poi, poi)
                add_poi.used_times = 1
                conn.session.add(add_poi)

                data = {'uid': params['uid'],
                        'vin': params['vin'],
                        'time': time_array,
                        'poi_id': params['poi_id'],
                        'poi_type': poi_type,
                        'valid': True,
                        'poi_name': poi_name,
                        'poi_location': poi_location,
                        'used_location': used_location,
                        'tag': poi_tag,
                        'cost': poi_cost,
                        'rating': poi_rating,
                        'photo_1': poi_photo_1,
                        'photo_2': poi_photo_2,
                        'photo_3': poi_photo_3}

                add_item = definition.PoiHistory(**data)
                conn.session.add(add_item)
                conn.commit()
                conn.close()
                return result.CommonResult(res='Success.')
            except Exception:
                traceback.print_exc()
                return result.ErrorResult(exception.SQLConnectError())
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
