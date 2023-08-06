#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/31 8:42
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : paginator
# @Project : app_map 
# @Contact : guangze.yu@foxmail.com
"""
import redis
import config.redis as cfg

HOST = cfg.host
PORT = cfg.port
PASSWORD = cfg.password
pool = redis.ConnectionPool(host=HOST, password=PASSWORD, port=PORT)
cache = redis.Redis(connection_pool=pool)


class PagInatorCommon(object):
    def __init__(self, vin, uid):
        self._vin = vin
        self._uid = uid

    def create(self):
        pass

    def result(self):
        pass


class PoiSearchPagInator(object):

    def __init__(self, vin, uid, keywords):
        self.key = str(vin) + str(uid) + 'poi' + str(keywords.encode()).replace('\\', '').replace('\'', '')
        self.expire_time = 3
        self.value = cache.get(self.key)

    def get_value(self):
        cache.set(self.key, self.value, self.expire_time)
        return self.value

    def set_value(self, value):
        self.value = cache.get(self.key)
        cache.set(self.key, value, self.expire_time)


class UnionSearchPagInator(object):

    def __init__(self, vin, uid, keywords):
        self.key = str(vin) + str(uid) + 'union' + str(keywords.encode()).replace('\\', '').replace('\'', '')
        self.expire_time = 3
        self.value = cache.get(self.key)

    def get_value(self):
        cache.set(self.key, self.value, self.expire_time)
        return self.value

    def set_value(self, value):
        self.value = cache.get(self.key)
        cache.set(self.key, value, self.expire_time)


class SurSearchPagInator(object):

    def __init__(self, vin, uid, keywords):
        self.key = str(vin) + str(uid) + 'sur' + str(keywords.encode()).replace('\\', '').replace('\'', '')
        self.expire_time = 3
        self.value = cache.get(self.key)

    def get_value(self):
        cache.set(self.key, self.value, self.expire_time)
        return self.value

    def set_value(self, value):
        self.value = cache.get(self.key)
        cache.set(self.key, value, self.expire_time)
