#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 上午8:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : data_base
# @Contact : guangze.yu@foxmail.com
"""

import datetime
import time
import database.definition as definition

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
        # print(data)
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
        query = ("SELECT tb_trace.time, "
                 "tb_trace.location "
                 "from tb_trace "
                 "where tb_trace.vin='%s' and tb_trace.time>'%s' "
                 % (self._vin, time_array))
        data = self._conn.session.execute(query)
        out = [{'time': str(i[0]), 'location': i[1]} for i in data]
        # print(out)
        return out

    def getn(self, datanum):
        query = ("SELECT tb_trace.time, "
                 "tb_trace.location "
                 "from tb_trace "
                 "where tb_trace.vin='%s' ORDER BY tb_trace.time DESC LIMIT %s "
                 % (self._vin, datanum))
        data = self._conn.session.execute(query)
        out = [{'time': str(i[0]), 'location': i[1]} for i in data]
        return out
