#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/21 12:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : tuju
# @Project : app_map
# @Contact : guangze.yu@foxmail.com
"""
import requests
import json


class Common(object):
    def __init__(self, param_dict):
        self._http_body = param_dict
        self._http_params = param_dict
        self._url = 'http://api.st.97ting.com:8001/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'

    def post(self):
        res = json.loads(requests.post(url=self._url,
                                       json=self._http_body
                                       ).content.decode('utf-8'))
        return res

    def get(self):
        param = self._http_params
        res = requests.get(self._url, param)
        return json.loads(res.content.decode('utf-8'))


class GPSUpdate(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain location, uid, floor
        location:
        uid:
        floor:
        """
        super(GPSUpdate, self).__init__(param_dict)
        self._http_body = param_dict
        if 'uid' not in self._http_body:
            self._http_body['uid'] = 123456

        self._url = 'http://106.14.183.222:10008/location'

    def get(self):
        print('GET method is not supported.')
        return
