#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 上午8:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : data_base
# @Contact : guangze.yu@foxmail.com
"""

import random
import collections
import datetime
import logging
import time
import traceback
import vendor.gaode.api as gaode
import database.definition as definition
import utils.exception as exception
from sqlalchemy import desc

CONN = definition.Connect()


def arguments_check(func):
    def make_wrapper(method, data):
        class_keys = list(method.__dict__.keys())
        arguments_keys = list(data.keys())
        arguments_new = {}
        for i in arguments_keys:
            if i in class_keys:
                temp = data[i]
                if not temp:
                    arguments_new[i] = None
                else:
                    arguments_new[i] = temp
        return func(method, arguments_new)

    return make_wrapper


@arguments_check
def insert(method, data):
    return method(**data)


class User(object):
    def __init__(self, uid, conn=CONN):
        self._uid = uid
        self._conn = conn
        self.poi_history_list = self.get_poi_history()
        self.uinfo = self.get_uinfo()
        self.broadcast_history = self.get_broadcast_history()

    def get_poi_history(self, n=10):
        try:
            query = self._conn.session.query(definition.PoiHistory)
            poi_query = self._conn.session.query(definition.Poi)
            u = query.filter_by(uid=self._uid).all()
            if u:
                temp = collections.OrderedDict()
                temp_timestamp = {}
                for i in u:
                    if i.poi_id in temp.keys():
                        temp[i.poi_id] += 1
                        temp_timestamp[i.poi_id].append(float(i.time.timestamp()))
                    else:
                        temp[i.poi_id] = 1
                        temp_timestamp[i.poi_id] = [float(i.time.timestamp())]
                poi_search_history = collections.OrderedDict(sorted(temp.items(), key=lambda t: t[1], reverse=True))
                out = []
                index = 1
                maxnum = min(n, len(poi_search_history))
                temp = {}
                for poi_id, used_times in poi_search_history.items():
                    temp.clear()
                    temp['id'] = poi_id
                    poi_info = poi_query.filter_by(id=poi_id).first()
                    temp['tag'] = poi_info.tag
                    temp['name'] = poi_info.name
                    temp['type'] = poi_info.type
                    temp['typecode'] = poi_info.typecode
                    temp['location'] = poi_info.location
                    temp['used_times'] = used_times
                    temp_timestamp[poi_id].sort(reverse=True)
                    temp['used_timestamp'] = temp_timestamp[poi_id]
                    out.append(temp)
                    index += 1
                    if index > maxnum:
                        break
            else:
                out = None
            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def get_uinfo(self):
        try:
            query = self._conn.session.query(definition.UserInfo)
            user_query = query.filter_by(uid=self._uid).first()
            if user_query is not None:
                out = {'name': user_query.name,
                       'gender': user_query.gender,
                       'age': datetime.datetime.now().year - int(int(user_query.birth) / 10000),
                       'latitude': user_query.latitude}
            else:
                out = None
            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def get_broadcast_history(self):
        try:
            query = self._conn.session.query(definition.BroadCastHistory)
            u = query.filter_by(uid=self._uid).all()
            if u:
                temp = collections.OrderedDict()
                temp_timestamp = {}
                for i in u:
                    if i.isbroadcast:
                        if i.citycode in temp.keys():
                            temp[i.citycode] += 1
                            temp_timestamp[i.citycode].append(float(i.time.timestamp()))
                        else:
                            temp[i.citycode] = 1
                            temp_timestamp[i.citycode] = [float(i.time.timestamp())]
                broadcast_history = collections.OrderedDict(sorted(temp.items(), key=lambda t: t[1], reverse=True))
                out = []
                temp = {}
                for citycode, broadcast_num in broadcast_history.items():
                    temp.clear()
                    temp['citycode'] = citycode
                    temp['broadcast_num'] = broadcast_num
                    temp_timestamp[citycode].sort(reverse=True)
                    temp['broadcast_time'] = temp_timestamp[citycode]
                    out.append(temp)
            else:
                out = None
            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            return False


class BroadCity(object):
    """
        BroadCity
    """

    def __init__(self, citycode, conn):
        self._conn = conn
        query = self._conn.session.query(definition.BroadCastInfo)
        broad_data = query.filter_by(citycode=citycode).first()
        info = {'citycode': broad_data.citycode,
                'adcode': broad_data.adcode,
                'name': broad_data.name,
                'level': broad_data.level,
                'broad_info': broad_data.info}
        self.info = info

    def history_update(self, data):
        add_history = insert(definition.BroadCastHistory, data)
        self._conn.session.add(add_history)
        self._conn.commit()


class PoiHistory(object):
    """
        PoiHistory
    """

    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        self._conn = conn
        self._vin = vin
        self._uid = uid
        self._start_time = datetime.datetime.now() - datetime.timedelta(600)
        self._end_time = datetime.datetime.now()

    def get(self, start_time=None, end_time=None, keyword=None):
        """

        :param starttime:
        :param endtime:
        :param keyword:
        :return:
        """
        if start_time is None:
            starttime = datetime.datetime.now() - datetime.timedelta(600)
        else:
            starttime = start_time

        if end_time is None:
            endtime = datetime.datetime.now()
        else:
            endtime = end_time

        try:
            if keyword is None:
                if self._uid is None:
                    query = (
                            "SELECT "
                            "tb_poi_history.poi_id, tb_poi_history.poi_name, tb_poi_history.rating, tb_poi_history.cost, "
                            "tb_poi_history.poi_type, tb_poi_history.poi_location, tb_poi_history.photo_1_title, "
                            "tb_poi_history.photo_1, tb_poi_history.photo_2_title, tb_poi_history.photo_2, "
                            "tb_poi_history.photo_3_title, tb_poi_history.photo_3, tb_poi_history.type_code, "
                            "tb_poi_history.city_code, tb_poi_history.city_name, tb_poi_history.ad_name, "
                            "tb_poi_history.ad_code, tb_poi_history.address, tb_poi_history.tel, tb_poi_history.tag, "
                            "tb_poi_history.time "
                            "FROM (SELECT DISTINCT * FROM tb_poi_history "
                            "      WHERE tb_poi_history.valid = 1 "
                            "            AND tb_poi_history.vin='%s' "
                            "            AND tb_poi_history.uid is null "
                            "      ORDER BY tb_poi_history.time DESC) tb_poi_history "
                            "GROUP BY tb_poi_history.poi_name "
                            "ORDER BY tb_poi_history.time DESC; "
                            % (self._vin))
                else:
                    query = (
                            "SELECT "
                            "tb_poi_history.poi_id, tb_poi_history.poi_name, tb_poi_history.rating, tb_poi_history.cost, "
                            "tb_poi_history.poi_type, tb_poi_history.poi_location, tb_poi_history.photo_1_title, "
                            "tb_poi_history.photo_1, tb_poi_history.photo_2_title, tb_poi_history.photo_2, "
                            "tb_poi_history.photo_3_title, tb_poi_history.photo_3, tb_poi_history.type_code, "
                            "tb_poi_history.city_code, tb_poi_history.city_name, tb_poi_history.ad_name, "
                            "tb_poi_history.ad_code, tb_poi_history.address, tb_poi_history.tel, tb_poi_history.tag, "
                            "tb_poi_history.time "
                            "FROM (SELECT DISTINCT * FROM tb_poi_history "
                            "      WHERE tb_poi_history.valid = 1 "
                            "            AND tb_poi_history.uid='%s' "
                            "      ORDER BY tb_poi_history.time DESC) tb_poi_history "
                            "GROUP BY tb_poi_history.poi_name "
                            "ORDER BY tb_poi_history.time DESC; "
                            % (self._uid))

            else:
                if self._uid is None:
                    query = (
                            "SELECT "
                            "tb_poi_history.poi_id, tb_poi_history.poi_name, tb_poi_history.rating, tb_poi_history.cost, "
                            "tb_poi_history.poi_type, tb_poi_history.poi_location, tb_poi_history.photo_1_title, "
                            "tb_poi_history.photo_1, tb_poi_history.photo_2_title, tb_poi_history.photo_2, "
                            "tb_poi_history.photo_3_title, tb_poi_history.photo_3, tb_poi_history.type_code, "
                            "tb_poi_history.city_code, tb_poi_history.city_name, tb_poi_history.ad_name, "
                            "tb_poi_history.ad_code, tb_poi_history.address, tb_poi_history.tel, tb_poi_history.tag, "
                            "tb_poi_history.time "
                            "FROM (SELECT DISTINCT * FROM tb_poi_history "
                            "    WHERE tb_poi_history.valid = 1 "
                            "          AND tb_poi_history.vin='%s' "
                            "          AND tb_poi_history.uid is null "
                            "          AND tb_poi_history.poi_name like '%%%s%%' "
                            "    ORDER BY tb_poi_history.time DESC) tb_poi_history "
                            "GROUP BY tb_poi_history.poi_name "
                            "ORDER BY tb_poi_history.time DESC; "
                            % (self._vin, keyword))
                else:
                    query = (
                            "SELECT "
                            "tb_poi_history.poi_id, tb_poi_history.poi_name, tb_poi_history.rating, tb_poi_history.cost, "
                            "tb_poi_history.poi_type, tb_poi_history.poi_location, tb_poi_history.photo_1_title, "
                            "tb_poi_history.photo_1, tb_poi_history.photo_2_title, tb_poi_history.photo_2, "
                            "tb_poi_history.photo_3_title, tb_poi_history.photo_3, tb_poi_history.type_code, "
                            "tb_poi_history.city_code, tb_poi_history.city_name, tb_poi_history.ad_name, "
                            "tb_poi_history.ad_code, tb_poi_history.address, tb_poi_history.tel, tb_poi_history.tag, "
                            "tb_poi_history.time "
                            "FROM (SELECT DISTINCT * FROM tb_poi_history "
                            "   WHERE tb_poi_history.valid = 1 "
                            "         AND tb_poi_history.uid='%s' "
                            "         AND tb_poi_history.poi_name like '%%%s%%' "
                            "   ORDER BY tb_poi_history.time DESC) tb_poi_history "
                            "GROUP BY tb_poi_history.poi_name "
                            "ORDER BY tb_poi_history.time DESC; "
                            % (self._uid, keyword))
            print(query)
            data = self._conn.session.execute(query)
            out = [self.convert2gaode(i) for i in data]
            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            logging.exception('this is an exception message')
            return False

    def convert2gaode(self, params):

        out = {"adcode": params[16],
               "address": params[17],
               "adname": params[15],
               "alias": "",
               "biz_ext": {
                   "meal_ordering": "",
                   "rating": params[2],
                   "cost": params[3]
               },
               "biz_type": "",
               "business_area": "",
               "children": "",
               "citycode": params[13],
               "cityname": params[14],
               "discount_num": "",
               "distance": "",
               "email": "",
               "entr_location": "",
               "event": "",
               "exit_location": "",
               "gridcode": "",
               "groupbuy_num": "",
               "id": params[0],
               "importance": "",
               "indoor_data": {
                   "truefloor": "",
                   "floor": "",
                   "cpid": ""
               },
               "indoor_map": "",
               "location": params[5],
               "match": "",
               "name": params[1],
               "navi_poiid": "",
               "pcode": "",
               "photos": [
                   {
                       "title": params[6],
                       "url": params[7]
                   },
                   {
                       "title": params[8],
                       "url": params[9]
                   },
                   {
                       "title": params[10],
                       "url": params[11]
                   }
               ],
               "pname": "",
               "poiweight": "",
               "postcode": "",
               "recommend": "",
               "shopid": "",
               "shopinfo": "",
               "tag": params[9],
               "tel": params[18],
               "timestamp": "",
               "type": params[4],
               "typecode": params[12],
               'time': params[20].strftime("%Y-%m-%d %H:%S:%M"),
               "website": "",
               }
        return out

    def convert3(self, params):
        out = {"adcode": params[16],
               "address": params[17],
               "adname": params[15],
               "alias": "",
               "biz_ext": {
                   "meal_ordering": "",
                   "rating": params[2],
                   "cost": params[3]
               },
               "biz_type": "",
               "business_area": "",
               "children": "",
               "citycode": params[13],
               "cityname": params[14],
               "discount_num": "",
               "distance": "",
               "email": "",
               "entr_location": "",
               "event": "",
               "exit_location": "",
               "gridcode": "",
               "groupbuy_num": "",
               "id": params[0],
               "importance": "",
               "indoor_data": {
                   "truefloor": "",
                   "floor": "",
                   "cpid": ""
               },
               "indoor_map": "",
               "location": params[5],
               "match": "",
               "name": params[1],
               "navi_poiid": "",
               "pcode": "",
               "photos": [
                   {
                       "title": params[6],
                       "url": params[7]
                   },
                   {
                       "title": params[8],
                       "url": params[9]
                   },
                   {
                       "title": params[10],
                       "url": params[11]
                   }
               ],
               "pname": "",
               "poiweight": "",
               "postcode": "",
               "recommend": "",
               "shopid": "",
               "shopinfo": "",
               "tag": params[9],
               "tel": params[18],
               "timestamp": "",
               "type": params[4],
               "typecode": params[12],
               "website": "",
               }
        return out

    def clear(self):
        try:
            query = self._conn.session.query(definition.PoiHistory)
            if self._uid is None:
                data = query.filter_by(vin=self._vin, uid=self._uid, valid=True).all()
            else:
                data = query.filter_by(uid=self._uid, valid=True).all()
            for i in data:
                i.valid = False
            self._conn.commit()
            return True
        except exception.SQLConnectError:
            traceback.print_exc()
            logging.exception('this is an exception message')
            return False


class SearchWordHistory(object):
    """
        SearchWordHistory
    """

    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        self._conn = conn
        self._vin = vin
        self._uid = uid

    def get(self, start_time=None, end_time=None, keyword=None):
        """

        :param starttime:
        :param endtime:
        :return:
        """
        if start_time is None:
            starttime = datetime.datetime.now() - datetime.timedelta(600)
        else:
            starttime = start_time

        if end_time is None:
            endtime = datetime.datetime.now()
        else:
            endtime = end_time

        try:
            if keyword is None:
                if self._uid is None:
                    query = ("SELECT tb_searchkeys.keywords, tb_searchkeys.time FROM "
                             "(SELECT DISTINCT *  FROM tb_searchkeys WHERE "
                             "tb_searchkeys.valid = 1 "
                             "and tb_searchkeys.uid is NULL and tb_searchkeys.vin = '%s' "
                             "ORDER BY tb_searchkeys.time DESC) tb_searchkeys "
                             "GROUP BY tb_searchkeys.keywords "
                             "ORDER BY tb_searchkeys.time DESC; "
                             % (self._vin))
                else:
                    query = ("SELECT tb_searchkeys.keywords, tb_searchkeys.time FROM "
                             "(SELECT DISTINCT *  FROM tb_searchkeys WHERE "
                             "tb_searchkeys.valid = 1 "
                             "and tb_searchkeys.uid = '%s' "
                             "ORDER BY tb_searchkeys.time DESC) tb_searchkeys "
                             "GROUP BY tb_searchkeys.keywords "
                             "ORDER BY tb_searchkeys.time DESC; "
                             % (self._uid))
            else:
                if self._uid is None:
                    query = ("SELECT tb_searchkeys.keywords, tb_searchkeys.time FROM "
                             "(SELECT DISTINCT * FROM tb_searchkeys WHERE "
                             "tb_searchkeys.valid = 1 "
                             "and tb_searchkeys.keywords like '%%%s%%' "
                             "and tb_searchkeys.uid is NULL and tb_searchkeys.vin = '%s' "
                             "ORDER BY tb_searchkeys.time DESC) tb_searchkeys "
                             "GROUP BY tb_searchkeys.keywords "
                             "ORDER BY tb_searchkeys.time DESC; "
                             % (keyword, self._vin))
                else:
                    query = ("SELECT tb_searchkeys.keywords, tb_searchkeys.time FROM "
                             "(SELECT DISTINCT * FROM tb_searchkeys  WHERE "
                             "tb_searchkeys.valid = 1 "
                             "and tb_searchkeys.keywords like '%%%s%%' "
                             "and tb_searchkeys.uid = '%s' "
                             "ORDER BY tb_searchkeys.time DESC) tb_searchkeys "
                             "GROUP BY tb_searchkeys.keywords "
                             "ORDER BY tb_searchkeys.time DESC; "
                             % (keyword, self._uid))
            print(query)
            data = self._conn.session.execute(query)
            out = [{'keywords': i[0], 'time': i[1].strftime("%Y-%m-%d %H:%S:%M")} for i in data]
            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def add(self, keywords, timestamp=None):
        """

        :param keyword:
        :param timestamp:
        :return:
        """
        if timestamp is None:
            timestamp = int(time.time())
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            data = {'uid': self._uid,
                    'vin': self._vin,
                    'keywords': keywords,
                    'time': time_array,
                    'valid': True}
            word = definition.SearchKeys(**data)
            self._conn.session.add(word)
            self._conn.commit()
            return True
        except:
            # self._conn.rollback()
            traceback.print_exc()
            return False

    def clear(self, keywords=None):
        try:
            if keywords is not None:
                query = self._conn.session.query(definition.SearchKeys)
                data = query.filter_by(vin=self._vin, uid=self._uid, valid=True, keywords=keywords).all()
            else:
                query = self._conn.session.query(definition.SearchKeys)
                data = query.filter_by(uid=self._uid, valid=True).all()
            for i in data:
                i.valid = False
            self._conn.commit()
            return True
        except exception.SQLConnectError:
            traceback.print_exc()
            return False


class UserCollect(object):
    """
        UserCollect
    """

    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        self._conn = conn
        self._vin = vin
        self._uid = uid

    def get(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(definition.Collect)
            if self._uid is None:
                data = query.filter_by(vin=self._vin, uid=self._uid, valid=True).order_by(
                    desc(definition.Collect.modifiedtime)).all()
            else:
                data = query.filter_by(uid=self._uid, valid=True).order_by(desc(definition.Collect.modifiedtime)).all()
            out = [
                {'id': i.poi_id, 'name': i.poi_name, 'type': i.type, 'typecode': i.typecode, 'citycode': i.citycode,
                 'adname': i.adname, 'tel': i.tel, 'address': i.address, 'adcode': i.adcode, 'cityname': i.cityname,
                 'location': i.location}
                for i in data]

            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def add(self, poi_id, timestamp=None, poi_tag=None):
        """

        :param poi_id:
        :param location:
        :param timestamp:
        :param poi_type:
        :return:
        """
        if timestamp is None:
            timestamp = int(time.time())
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            query = self._conn.session.query(definition.Collect)
            poi = self._conn.session.query(definition.Poi).filter_by(id=poi_id).first()

            if poi is None:
                s = {'id': poi_id}
                poiinfo = gaode.ID_Search(s).get()
                if poiinfo['pois'][0]['name'] is None:
                    name = ""
                else:
                    name = poiinfo['pois'][0]['name']
                if poiinfo['pois'][0]['type'] is None:
                    poi_type = ""
                else:
                    poi_type = poiinfo['pois'][0]['type']
                if poiinfo['pois'][0]['typecode'] is None:
                    typecode = ""
                else:
                    typecode = poiinfo['pois'][0]['typecode']
                if poiinfo['pois'][0]['citycode'] is None:
                    citycode = ""
                else:
                    citycode = poiinfo['pois'][0]['citycode']
                if poiinfo['pois'][0]['adname'] is None:
                    adname = ""
                else:
                    adname = poiinfo['pois'][0]['adname']
                if len(poiinfo['pois'][0]['tel']) == 0:
                    tel = ""
                else:
                    tel = poiinfo['pois'][0]['tel']
                if poiinfo['pois'][0]['address'] is None:
                    address = ""
                else:
                    address = poiinfo['pois'][0]['address']
                if poiinfo['pois'][0]['adcode'] is None:
                    adcode = ""
                else:
                    adcode = poiinfo['pois'][0]['adcode']
                if poiinfo['pois'][0]['cityname'] is None:
                    cityname = ""
                else:
                    cityname = poiinfo['pois'][0]['cityname']
                if poiinfo['pois'][0]['location'] is None:
                    location = ""
                else:
                    location = poiinfo['pois'][0]['location']
            else:
                if poi.name is None:
                    name = ""
                else:
                    name = poi.name
                if poi.type is None:
                    poi_type = ""
                else:
                    poi_type = poi.type
                if poi.typecode is None:
                    typecode = ""
                else:
                    typecode = poi.typecode
                if poi.citycode is None:
                    citycode = ""
                else:
                    citycode = poi.citycode
                if poi.adname is None:
                    adname = ""
                else:
                    adname = poi.adname
                if poi.tel is None:
                    tel = ""
                else:
                    tel = poi.tel
                if poi.address is None:
                    address = ""
                else:
                    address = poi.address
                if poi.adcode is None:
                    adcode = ""
                else:
                    adcode = poi.adcode
                if poi.cityname is None:
                    cityname = ""
                else:
                    cityname = poi.cityname
                if poi.location is None:
                    location = ""
                else:
                    location = poi.location

            if self._uid is None:
                poicollect = query.filter_by(vin=self._vin, uid=self._uid, poi_id=poi_id).first()
            else:
                poicollect = query.filter_by(uid=self._uid, poi_id=poi_id).first()
            if poicollect is None:
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'location': location,
                        'poi_id': poi_id,
                        'type': poi_type,
                        'typecode': typecode,
                        'citycode': citycode,
                        'adname': adname,
                        'tel': tel,
                        'address': address,
                        'adcode': adcode,
                        'cityname': cityname,
                        'tag': poi_tag,
                        'valid': True,
                        'createtime': time_array,
                        'modifiedtime': time_array,
                        'poi_name': name}
                addpoi = definition.Collect(**data)
                self._conn.session.add(addpoi)
            else:
                poicollect.location = location
                poicollect.valid = True
                poicollect.modifiedtime = time_array
            self._conn.session.commit()
            return True
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def delete(self, poi_id, timestamp=None):
        """

        :param poi_id:
        :param timestamp:
        :return:
        """
        if timestamp is None:
            timestamp = int(time.time())
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            query = self._conn.session.query(definition.Collect)
            if self._uid is None:
                poicollect = query.filter_by(vin=self._vin, uid=self._uid, poi_id=poi_id).first()
            else:
                poicollect = query.filter_by(uid=self._uid, poi_id=poi_id).first()
            poicollect.valid = False
            poicollect.modifiedtime = time_array
            self._conn.session.commit()
            return True
        except exception.SQLConnectError:
            traceback.print_exc()
            return False


class UserTrace(object):
    """
        UserTrace
    """

    def __init__(self, vin, uid=None, conn=CONN):
        self._conn = conn
        self._vin = vin
        self._uid = uid

    def add(self, location, timestamp=None):
        if timestamp is None:
            time_array = datetime.datetime.fromtimestamp(time.time())
        else:
            time_array = datetime.datetime.fromtimestamp(timestamp)
        data = {'uid': self._uid, 'vin': self._vin, 'location': location,
                'time': time_array}
        print(data)
        new_trace = definition.Trace(**data)
        self._conn.session.add(new_trace)
        self._conn.commit()
        return True

    def get(self, timestamp=None):
        if timestamp is None:
            temp = "select max(time) from tb_trace where vin='%s';" % self._vin
            start_time = self._conn.session.execute(temp).fetchall()[0][0]
            time_array = start_time - datetime.timedelta(minutes=30)
        else:
            time_array = datetime.datetime.fromtimestamp(timestamp) - datetime.timedelta(minutes=30)
        query = ("SELECT tb_trace.time,"
                 "tb_trace.location "
                 "from tb_trace "
                 "where tb_trace.vin='%s' and tb_trace.time>'%s'"
                 % (self._vin, time_array))
        data = self._conn.session.execute(query)
        out = [{'time': str(i[0]), 'location': i[1]} for i in data]
        print(out)
        return out

    def getn(self, datanum):
        query = ("SELECT tb_trace.time,"
                 "tb_trace.location "
                 "from tb_trace "
                 "where tb_trace.vin='%s' ORDER BY tb_trace.time DESC LIMIT %s "
                 % (self._vin, datanum))
        data = self._conn.session.execute(query)
        out = [{'time': str(i[0]), 'location': i[1]} for i in data]
        return out


class UsualAddress(object):
    """
        SearchWordHistory
    """

    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        self._conn = conn
        self._vin = vin
        self._uid = uid

    def get(self):
        """

        :param
        :param
        :return:
        """
        try:
            if self._uid is None:
                query = ("SELECT poi_id, address,type from tb_usual_address "
                         "where  vin = '%s' "
                         "and uid is NULL and valid = 1 ;"
                         % (self._vin))
            else:
                query = ("SELECT poi_id, address,type from tb_usual_address "
                         "where uid = '%s' and valid = 1 ;"
                         % (self._uid))
            data = self._conn.session.execute(query)
            out = [{'poi_id': i[0], 'address': i[1], 'type': i[2]} for i in data]
            return out
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def add(self, poi_id=None, address=None, timestamp=None, type=None):
        """

        :param
        :param
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            data = {}
            if type is '1':
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'poi_id': poi_id,
                        'address': address,
                        'type': type,
                        'createtime': time_array,
                        'valid': True}
            elif type is '2':
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'poi_id': poi_id,
                        'address': address,
                        'type': type,
                        'createtime': time_array,
                        'valid': True}
            word = definition.UsualAddress(**data)
            self._conn.session.add(word)
            self._conn.commit()
            return True
        except exception.SQLConnectError:
            traceback.print_exc()
            return False

    def clear(self, type=None, timestamp=None):
        """

        :param
        :param
        :return:
        """
        if timestamp is None:
            timestamp = int(time.time())
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            query = self._conn.session.query(definition.UsualAddress)
            if self._uid is None:
                if type is '1':
                    data = query.filter_by(vin=self._vin, valid=True, type=type).first()
                elif type is '2':
                    data = query.filter_by(vin=self._vin, valid=True, type=type).first()
            else:
                if type is '1':
                    data = query.filter_by(vin=self._vin, uid=self._uid, valid=True, type=type).first()
                elif type is '2':
                    data = query.filter_by(vin=self._vin, uid=self._uid, valid=True, type=type).first()
            data.valid = False
            data.modifiedtime = time_array
            self._conn.session.commit()
            return True
        except exception.SQLConnectError:
            traceback.print_exc()
            return False


def gen_poi_data(connect):
    query = connect.session.query(definition.Poi)
    for i in range(200):
        print(i)
        loaction_x = random.randint(12085, 12220) / 100 + random.random() / 100
        loaction_y = random.randint(3067, 3188) / 100 + random.random() / 100
        s = {'location': '%6f,%6f' % (loaction_x, loaction_y), 'extensions': 'all'}
        poi = gaode.Surrounding_Search(s).get()['pois'][0]
        poi_id = poi['id']
        if '墓' in type:
            continue
        if '葬' in type:
            continue
        u = query.filter_by(id=poi_id).first()
        if u is not None:
            used_times = u.used_times + 1
            u.used_times = used_times
        else:
            ad_poi = insert(definition.Poi, poi)
            ad_poi.used_times = 1
            connect.session.add(ad_poi)
    connect.commit()


def gen_poi_history_data(connect):
    query = connect.session.query(definition.Poi)
    init = 1483200000.0
    for i in range(600):
        loaction_x = random.randint(12085, 12220) / 100 + random.random() / 100
        loaction_y = random.randint(3067, 3188) / 100 + random.random() / 100
        uid = [888888, 123456, 666666]
        vin_code = ['AAAAAAAAAAAAAAAAA', 'BBBBBBBBBBBBBBBBB', 'CCCCCCCCCCCCCCCCC']
        timestamp = (init + 86400 * random.randint(0, 300) + random.randint(0, 23) * 60 * 60
                     + random.randint(0, 60) + random.random())
        time_array = datetime.datetime.fromtimestamp(timestamp)
        user_index = random.randint(0, 2)
        poi_index = random.randint(1, 50)
        poi = query.filter_by(index=poi_index).first()
        valid = [True, False][random.randint(0, 1)]
        data = {'uid': uid[user_index],
                'vin': vin_code[user_index],
                'time': time_array,
                'poi_id': poi.id,
                'poi_name': poi.name,
                'used_location': '%6f,%6f' % (loaction_x, loaction_y),
                'valid': valid}
        add_item = definition.PoiHistory(**data)
        connect.session.add(add_item)
    connect.commit()


def gen_broadcast_data(connect):
    query = connect.session.query(definition.BroadCastInfo)
    s = {}
    info = gaode.District(s).get()
    province_info = info['districts'][0]['districts']
    for i in province_info:
        u = query.filter_by(adcode=i['adcode']).first()
        if u is None:
            temp = i
            temp['info'] = '欢迎来到%s' % i['name']
            province = insert(definition.BroadCastInfo, temp)
            connect.session.add(province)
        else:
            continue
        s = {'keywords': '%s' % i['name'], 'subdistrict': '1'}
        city_info = gaode.District(s).get()['districts']
        for k in city_info:
            for q in k['districts']:
                u = query.filter_by(adcode=q['adcode']).first()
                if u is None:
                    temp = q
                    temp['info'] = '欢迎来到%s' % q['name']
                    city = insert(definition.BroadCastInfo, temp)
                    connect.session.add(city)
                else:
                    continue
    connect.commit()


def gen_broadcast_history(connect):
    query = connect.session.query(definition.BroadCastInfo)
    init = 1483200000.0
    uid = [888888, 123456, 666666]
    vin = ['AAAAAAAAAAAAAAAAA', 'BBBBBBBBBBBBBBBBB', 'CCCCCCCCCCCCCCCCC']
    for i in range(300):
        index = random.randint(0, 2)
        if index == 0:
            broadindex = random.randint(289, 305)
        elif index == 1:
            broadindex = random.randint(153, 168)
        else:
            broadindex = random.randint(170, 183)
        u = query.filter_by(index=broadindex).first()
        timestamp = (init + 86400 * random.randint(0, 300) + random.randint(0, 23) * 60 * 60
                     + random.randint(0, 60) + random.random())
        time_array = datetime.datetime.fromtimestamp(timestamp)
        temp = {'uid': uid[index],
                'vin': vin[index],
                'time': time_array,
                'citycode': u.citycode,
                'isbroadcast': random.randint(0, 1)}
        broad_history = insert(definition.BroadCastHistory, temp)
        connect.session.add(broad_history)
    connect.commit()
