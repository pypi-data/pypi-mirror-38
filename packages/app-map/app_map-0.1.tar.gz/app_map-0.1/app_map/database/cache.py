#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-22 下午2:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : cache
# @Contact : guangze.yu@foxmail.com
"""
import redis
import json
import database.operation as data_base
import config.redis as cfg

HOST = cfg.host
PORT = cfg.port
PASSWORD = cfg.password
pool = redis.ConnectionPool(host=HOST, password=PASSWORD, port=PORT)
cache = redis.Redis(connection_pool=pool)


class User(object):
    def __init__(self, uid):
        self.uid = uid
        cache_uinfo = cache.hget(uid, 'uinfo')
        if cache_uinfo is None:
            self.uinfo = data_base.User(uid).get_uinfo()
            cache.hset(uid, 'uinfo', json.dumps(self.uinfo))
        else:
            self.uinfo = json.loads(cache_uinfo)
        cache_poi_history_list = cache.hget(uid, 'poi_history_list')
        if cache_poi_history_list is None:
            self.poi_history_list = data_base.User(uid).get_poi_history()
            cache.hset(uid, 'poi_history_list', json.dumps(self.poi_history_list))
        else:
            self.poi_history_list = json.loads(cache_poi_history_list)
        cache_broadcast_history = cache.hget(uid, 'broadcast_history')
        if cache_broadcast_history is None:
            self.broadcast_history = data_base.User(uid).get_broadcast_history()
            cache.hset(uid, 'broadcast_history', json.dumps(self.broadcast_history))
        else:
            self.broadcast_history = json.loads(cache_broadcast_history)

    def update(self):
        self.__init__(self)


class UserLastLocation(object):
    def __init__(self, uid):
        self.uid = 'broad%s' % uid
        self.last_loc = cache.hget(self.uid, 'last_location')
        self.expire_time = 900

    def set(self, location):
        cache.hset(self.uid, 'last_location', location)
        cache.expire(self.uid, self.expire_time)


class VehicleLastLocation(object):
    def __init__(self, vin):
        self.vin = 'broad%s' % vin
        self.last_loc = cache.hget(self.vin, 'last_location')
        self.expire_time = 900

    def set(self, location):
        cache.hset(self.vin, 'last_location', location)
        cache.expire(self.vin, self.expire_time)


class VehicleLocation(object):
    def __init__(self, vin):
        self.vin = 'park_%s' % vin
        self.last_loc = cache.hget(self.vin, 'gps_location')
        # self.expire_time = 3600

    def set(self, location):
        cache.hset(self.vin, 'gps_location', location)
        # cache.expire(self.vin, self.expire_time)

class PoiSerachResult(object):
    def __init__(self, uid, keyword):
        self.uid = uid
        self.keyword = keyword
        self.expire_time = 300

    # def set(self, ):

class VehicleKeys(object):
    def __init__(self, type):
        self.type = type

    def get(self):
        keys = cache.keys()
        print(keys)
        keylist = [i.decode('utf-8').split('_')[1] for i in keys if 'park' in i.decode('utf-8')]
        return keylist
