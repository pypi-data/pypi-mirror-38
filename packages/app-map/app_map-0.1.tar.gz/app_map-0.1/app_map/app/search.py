#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-12 下午3:47
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : search
# @Contact : guangze.yu@foxmail.com
"""
import traceback
import json
import datetime
import app.map_AI as mapai
import database.cache as cache
import database.definition as definition
import database.operation as operation
import database.paginator as paginator
import utils.logger as logger
import utils.decorator as decorator
import utils.exception as exception
import utils.result as result
import mq.mess as mess
import vendor.gaode.api as gaode

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def poisearch(params):
    """
        poi搜索
    :param params:  keywords：关键字、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('poisearch service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        if 'keywords' in params.keys():
            keywords = params['keywords'].replace(" ", "")
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if not keywords:
            return result.ErrorResult(exception.NullKeywordsError())
        if 'location' in params.keys():
            location = params['location']
        else:
            if uid is None:
                location = None
            else:
                location = cache.UserLastLocation(params['uid']).last_loc

        if 'offset' in params:
            offset = params['offset']
        else:
            offset = decorator.Common().ten()
        if 'page' in params:
            page = int(params['page'])
        else:
            page = 1

        #   高德推荐
        return_info = mapai.search_keys(
            uid, keywords, gps=location, offset='10', pages='10')

        for i in return_info:
            i['sqtype'] = 'POI'
        conn = definition.Connect()
        operation.SearchWordHistory(vin, uid, conn).add(keywords=keywords)
        #   poi历史
        poi_history = operation.PoiHistory(
            vin=vin, conn=conn).get(keyword=keywords)
        conn.close()

        #   poi历史、高德推荐[去重]
        poi_history, return_info = decorator.distinct_search(
            poi_history, return_info)
        for i in poi_history:
            i['sqtype'] = 'POI'

        poi_history_data = decorator.formatTool(poi_history)

        if len(poi_history_data) > 0:
            for i in range(len(poi_history_data)):
                poi_history_data.extend(return_info)
        else:
            poi_history_data = return_info

        res = json.loads(json.dumps(poi_history_data).replace('NaN', '""'), encoding='utf-8')

        if len(res) >= offset:
            first_item = offset * (page - 1)
            last_item = min(offset * page, len(res))
            res_page = res[first_item:last_item]
        else:
            res_page = res

        #   高德推荐排序
        res_page.sort(key=lambda x: x["distance"])

        return result.SearchResult(res=res_page, count=len(res))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def unionsearch(params):
    """
        关键字搜索
    :param params:  keywords：关键字、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('unionsearch service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        if 'keywords' in params.keys():
            keywords = params['keywords'].replace(" ", "")
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if not keywords:
            return result.ErrorResult(exception.NullKeywordsError())
        if 'location' in params.keys():
            location = params['location']
        else:
            if uid is None:
                location = None
            else:
                location = cache.UserLastLocation(params['uid']).last_loc

        if 'offset' in params:
            offset = params['offset']
        else:
            offset = decorator.Common().ten()
        if 'page' in params:
            page = int(params['page'])
        else:
            page = 1
        conn = definition.Connect()

        # 高德搜索数据
        return_info = mapai.search_keys(
            uid, keywords, gps=location, offset='10', pages='10')

        for r in return_info:
            r['sqtype'] = 'POI'

        # 关键字历史
        keyword = operation.SearchWordHistory(vin, uid,
                                              conn).get(keyword=keywords)
        for k in keyword:
            k['sqtype'] = 'KEYWORD'

        # poi历史
        poi_history = operation.PoiHistory(vin, uid,
                                           conn).get(keyword=keywords)

        # poi历史、高德推荐[去重]
        poi_history, return_info = decorator.distinct_search(
            poi_history, return_info)
        for p in poi_history:
            p['sqtype'] = 'POI'

        history_list = []
        if len(keyword) > 3:
            history_list.extend(keyword[0:3])
        else:
            history_list.extend(keyword)
        if len(poi_history) > 3:
            history_list.extend(poi_history[0:3])
        else:
            history_list.extend(poi_history)
        poi_history_data = decorator.date_sort(history_list)

        if len(poi_history_data) > 0:
            for i in range(len(poi_history_data)):
                poi_history_data.extend(return_info)
            return_info.sort(key=lambda x: int(x["distance"]))
            res = json.loads(
                json.dumps(poi_history_data).replace('NaN', '""'),
                encoding='utf-8')
        else:
            return_info.sort(key=lambda x: int(x["distance"]))
            res = json.loads(
                json.dumps(return_info).replace('NaN', '""'), encoding='utf-8')
        if len(res) >= offset:

            first_item = offset * (page - 1)
            last_item = min(offset * page, len(res))
            res_page = res[first_item:last_item]

        else:
            res_page = res
        conn.close()
        return result.SearchResult(res=res_page, count=len(res))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def locationaddress(params):
    """
        GPS周边搜索
    :param params: location：经纬度、timestamp：时间戳，dict 对象
    :return:  json
    """
    LOG.info('poisearch service:')
    LOG.info('params is %s', params)
    try:
        radius = 500
        if 'location' in params.keys():
            if params['location'] is not "":
                location = params['location']
            else:
                return result.ErrorResult(exception.NullLocationError())
        else:
            # location = cache.UserLastLocation(params['uid']).last_loc
            return result.ErrorResult(exception.NoLocationError())
        location_address_poi = mapai.regeocode(
            location=location, radius=radius)
        addresslist = [
            location_address_poi['regeocode']['addressComponent']['province'],
            location_address_poi['regeocode']['addressComponent']['district'],
            location_address_poi['regeocode']['addressComponent']['township'],
            location_address_poi['regeocode']['addressComponent'][
                'streetNumber']['street'], location_address_poi['regeocode'][
                'addressComponent']['streetNumber']['number']
        ]
        address = ''.join(addresslist)
        return_location = location_address_poi['regeocode'][
            'addressComponent']['streetNumber']['location']
        pois = location_address_poi['regeocode']['pois']
        pois = decorator.formatTool(pois)
        listpoi = []
        listpoi.extend(pois)
        res = json.loads(
            json.dumps(listpoi[0:10]).replace('NaN', '""'), encoding='utf-8')
        return result.LocationAddressResult(
            res=res, address=address, location=return_location)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def iddetail(params):
    """
        POI详情信息
    :param params:  poi_id：poiid、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('broadcast service:')
    LOG.info('params is %s', params)
    try:
        timestamp = params['timestamp']
        time_array = datetime.datetime.fromtimestamp(timestamp)
        if 'poi_id' not in params.keys():
            return result.ErrorResult(exception.NoPoiIdError())
        else:
            try:
                if params['poi_id'] is not "":
                    conn = definition.Connect()
                    poi = gaode.ID_Search({
                        'id': params['poi_id']
                    }).get()['pois'][0]
                    poi_history_data = decorator.formatTool([poi])

                    poi_name = poi['name']
                    poi_location = poi['location']
                    poi_type = poi['type']
                    if len(poi['biz_ext']) == 0:
                        rating = ""
                        cost = ""
                    else:
                        if len(poi['biz_ext']['rating']) == 0:
                            rating = ""
                        else:
                            rating = poi['biz_ext']['rating']
                        if len(poi['biz_ext']['cost']) == 0:
                            cost = ""
                        else:
                            cost = poi['biz_ext']['cost']
                    if len(poi['photos']) == 3:
                        photo_1_title = ""
                        photo_1 = poi['photos'][0]['url']
                        photo_2_title = ""
                        photo_2 = poi['photos'][1]['url']
                        photo_3_title = ""
                        photo_3 = poi['photos'][2]['url']
                    elif len(poi['photos']) == 2:
                        photo_1_title = ""
                        photo_1 = poi['photos'][0]['url']
                        photo_2_title = ""
                        photo_2 = poi['photos'][1]['url']
                        photo_3_title = ""
                        photo_3 = ""
                    elif len(poi['photos']) == 1:
                        photo_1_title = ""
                        photo_1 = poi['photos'][0]['url']
                        photo_2_title = ""
                        photo_2 = ""
                        photo_3_title = ""
                        photo_3 = ""
                    else:
                        photo_1_title = ""
                        photo_1 = ""
                        photo_2_title = ""
                        photo_2 = ""
                        photo_3_title = ""
                        photo_3 = ""

                    if len(poi['tag']) == 0:
                        tag = ""
                    else:
                        tag = poi['tag']

                    if len(poi['typecode']) == 0:
                        type_code = ""
                    else:
                        type_code = poi['typecode']

                    if len(poi['citycode']) == 0:
                        city_code = ""
                    else:
                        city_code = poi['citycode']

                    if len(poi['cityname']) == 0:
                        city_name = ""
                    else:
                        city_name = poi['cityname']

                    if len(poi['adname']) == 0:
                        ad_name = ""
                    else:
                        ad_name = poi['adname']

                    if len(poi['tel']) == 0:
                        tel = ""
                    else:
                        tel = poi['tel']

                    if len(poi['address']) == 0:
                        address = ""
                    else:
                        address = poi['address']

                    if len(poi['adcode']) == 0:
                        ad_code = ""
                    else:
                        ad_code = poi['adcode']

                    add_poi = operation.insert(definition.Poi, poi)
                    add_poi.used_times = 1
                    conn.session.add(add_poi)
                    if 'uid' in params:
                        data = {
                            'uid': params['uid'],
                            'vin': params['vin'],
                            'time': time_array,
                            'poi_id': params['poi_id'],
                            'valid': True,
                            'poi_name': poi_name,
                            'poi_type': poi_type,
                            'used_location': params['location'],
                            'rating': rating,
                            'cost': cost,
                            'photo_1_title': photo_1_title,
                            'photo_1': photo_1,
                            'photo_2_title': photo_2_title,
                            'photo_2': photo_2,
                            'photo_3_title': photo_3_title,
                            'photo_3': photo_3,
                            'poi_location': poi_location,
                            'type_code': type_code,
                            'city_code': city_code,
                            'city_name': city_name,
                            'ad_name': ad_name,
                            'ad_code': ad_code,
                            'tel': tel,
                            'address': address,
                            'tag': tag
                        }
                    else:
                        data = {
                            'vin': params['vin'],
                            'time': time_array,
                            'poi_id': params['poi_id'],
                            'valid': True,
                            'poi_name': poi_name,
                            'poi_type': poi_type,
                            'used_location': params['location'],
                            'rating': rating,
                            'cost': cost,
                            'photo_1_title': photo_1_title,
                            'photo_1': photo_1,
                            'photo_2_title': photo_2_title,
                            'photo_2': photo_2,
                            'photo_3_title': photo_3_title,
                            'photo_3': photo_3,
                            'poi_location': poi_location,
                            'type_code': type_code,
                            'city_code': city_code,
                            'city_name': city_name,
                            'ad_name': ad_name,
                            'ad_code': ad_code,
                            'tel': tel,
                            'address': address,
                            'tag': tag
                        }
                    add_item = definition.PoiHistory(**data)
                    conn.session.add(add_item)
                    conn.commit()
                    conn.close()
                    return result.IdDetailResult(res=poi_history_data)
                else:
                    return result.ErrorResult(exception.NullPoiIdError())
            except Exception:
                traceback.print_exc()
                return result.ErrorResult(exception.SQLConnectError())
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


def gethispoi(params):
    LOG.info('gethispoi service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        if 'keywords' not in params:
            return result.ErrorResult(exception.NoKeyWordError)
        else:
            keywords = params['keywords']
        if 'days' not in params:
            days = 720
        else:
            days = params['days']
        conn = definition.Connect()
        res = operation.PoiHistory(
            vin=vin, uid=uid, conn=conn).get(keyword=keywords)
        conn.close()
        return result.SearchResult(res=res, count=len(res))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def sursearch(params):
    """
        周边搜索
    :param params:  keywords：关键字、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('sursearch service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        if 'keywords' in params.keys():
            keywords = params['keywords']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if 'radius' in params.keys():
            radius = params['radius']
        else:
            radius = 3000
        if 'location' in params.keys():
            location = params['location']
        else:
            return result.ErrorResult(exception.NoLocationError())

        if 'offset' in params:
            offset = params['offset']
        else:
            offset = 20
        if 'page' in params:
            page = params['page']
        else:
            page = 1

        cache_paginator_data = paginator.SurSearchPagInator(vin, uid, keywords)

        if cache_paginator_data.get_value() is None:
            return_info = mapai.surrounding_search(
                location=location,
                keywords=keywords,
                radius=radius,
                page=page,
                offset=offset)
            # poi历史
            conn = definition.Connect()
            poi_history = operation.PoiHistory(
                vin=vin, conn=conn).get(keyword=keywords)
            conn.close()
            poi_history_data = decorator.formatTool(poi_history)
            if len(poi_history_data) > 0:
                poi_hostory_num = len(poi_history_data)
                for i in range(poi_hostory_num):
                    if len(poi_history_data) < poi_hostory_num:
                        i = 0
                    # 计算是否在半径内
                    history_location = poi_history_data[i]['location']
                    distance_state = decorator.get_distance_hav(
                        history_location, location, radius)
                    if distance_state is False:
                        del (poi_history_data[i])

                poi_history_data.extend(return_info)
                res = json.loads(
                    json.dumps(poi_history_data).replace('NaN', '""'),
                    encoding='utf-8')
            else:
                res = json.loads(
                    json.dumps(return_info).replace('NaN', '""'),
                    encoding='utf-8')
            if len(res) >= offset:
                cache_paginator_data.set_value(res)
                first_item = offset * (page - 1)
                last_item = min(offset * page, len(res))
                res_page = res[first_item:last_item]
            else:
                res_page = res
        else:
            res = json.loads(
                cache_paginator_data.get_value().decode('utf-8').replace(
                    "'", "\""))
            first_item = offset * (page - 1)
            last_item = min(offset * page, len(res))
            res_page = res[first_item:last_item]

        info = params
        message = mess.SearchWordsHistory(method='add', info=info)
        return result.SearchResult(
            res=res_page, message=message, count=len(res))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def inputtips(params):
    """
        输入提示
    :param params:  keywords：关键字、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('inputtips service:')
    LOG.info('params is %s', params)
    param_dict = {}
    try:
        if 'keywords' in params.keys():
            param_dict['keywords'] = params['keywords']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if 'location' in params.keys():
            param_dict['location'] = params['location']
        if 'type' in params.keys():
            param_dict['type'] = params['type']
        return_info = gaode.Inputtips(param_dict).get()['tips']
        return result.InputTipsResult(res=return_info)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def gethiskeys(params):
    """
        获取搜索词记录
    :param params:  keywords：关键字、timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('gethistory service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        # start_time = datetime.datetime.now() - datetime.timedelta(180)
        # end_time = datetime.datetime.now()
        keywords = operation.SearchWordHistory(
            vin=vin, uid=uid, conn=conn).get()
        conn.close()
        return result.SearchResult(res=keywords)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def clearhiskeys(params):
    """
        清空搜索词记录
    :param params:  timestamp：时间戳、location：经纬度，dict 对象
    :return:  json
    """
    LOG.info('clearsearchkeys service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        conn = definition.Connect()
        if operation.SearchWordHistory(vin, uid, conn).clear():
            conn.close()
            return result.CommonResult(res='Success.')
        else:
            conn.close()
            return result.ErrorResult(exception.SQLConnectError())
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
