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
import config.redis as cfg

HOST = cfg.host
PORT = cfg.port
PASSWORD = cfg.password
pool = redis.ConnectionPool(host=HOST, password=PASSWORD, port=PORT)
cache = redis.Redis(connection_pool=pool)


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


class VehicleKeys(object):
    def __init__(self, type):
        self.type = type

    def get(self):
        keys = cache.keys()
        print(keys)
        keylist = [i.decode('utf-8').split('_')[1] for i in keys if 'park' in i.decode('utf-8')]
        return keylist
