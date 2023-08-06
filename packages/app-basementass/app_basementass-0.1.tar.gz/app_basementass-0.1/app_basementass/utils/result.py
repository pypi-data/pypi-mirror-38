#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-10-10 下午3:20
# @Author  : qian.wu
# @Site    : shanghai
# @File    : service
"""

import utils.exception as exception


class ResultBase(object):
    def __init__(self):
        self._status_code = None
        self._status_info = None
        self._response = None
        self._message = None

    @property
    def status_code(self):
        return self._status_code

    @property
    def status_info(self):
        return self._status_info

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        if self._message is None:
            return self._message
        else:
            return self._message.message


class TestResult(ResultBase):
    def __init__(self, res, message=None):
        super(TestResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class ErrorResult(ResultBase):
    def __init__(self, error, message=None):
        super(ErrorResult, self).__init__()
        self._status_code = error.code
        self._status_info = error.info
        self._response = self._status_info
        self._message = message


class CommonResult(ResultBase):
    def __init__(self, res, message=None):
        super(CommonResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class LocationResult(ResultBase):
    def __init__(self, res, message=None):
        super(LocationResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class TraceResult(ResultBase):
    def __init__(self, res, message=None):
        super(TraceResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class VehiclesResult(ResultBase):
    def __init__(self, res, message=None):
        super(VehiclesResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message