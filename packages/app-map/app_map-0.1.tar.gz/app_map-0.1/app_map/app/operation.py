#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/27 下午2:42
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : operation
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""

import datetime
import traceback
import database.definition as definition
import database.operation as operation
import utils.exception as exception
import utils.result as result
import utils.logger as logger
import utils.decorator as decorator
import vendor.gaode.api as gaode

params_check = decorator.params_check
LOG = logger.get_logger(__name__)


@params_check
def poiselect(params):
    """
        poi选择
    :param params: poi_id：poiid、location：经纬度、timestamp：时间戳，dict 对象
    :return:
    """
    LOG.info('broadcast service:')
    LOG.info('params is %s', params)
    try:
        timestamp = params['timestamp']
        time_array = datetime.datetime.fromtimestamp(timestamp)
        if 'poi_id' not in params.keys():
            return result.ErrorResult(exception.NoPoiIdError())
        else:
            print(params['poi_id'])
            try:
                conn = definition.Connect()
                poi = gaode.ID_Search({'id': params['poi_id']}).get()['pois'][0]
                poi_name = poi['name']
                poi_location = poi['location']
                poi_type = poi['type']
                if len(poi['biz_ext']['rating']) == 0:
                    rating = 0
                else:
                    rating = poi['biz_ext']['rating']
                if len(poi['biz_ext']['cost']) == 0:
                    cost = 0
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
                    data = {'uid': params['uid'],
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
                    data = {'vin': params['vin'],
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
                return result.CommonResult(res='Success.')
            except Exception:
                traceback.print_exc()
                return result.ErrorResult(exception.SQLConnectError())
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
