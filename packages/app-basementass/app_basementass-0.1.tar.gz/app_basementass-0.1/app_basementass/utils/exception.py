#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-10-10 下午3:20
# @Author  : qian.wu
# @Site    : shanghai
# @File    : service
"""

BASE_CODE = 50000


class Common(Exception):
    _status_code = 0
    _status_info = 'Success.'

    @property
    def code(self):
        return self._status_code

    @property
    def info(self):
        return self._status_info

    def __str__(self):
        return repr(self._status_info)


class Success(Common):
    _status_code = 0
    _status_info = 'Success.'


class InternalError(Common):
    _status_code = BASE_CODE + 500
    _status_info = 'Internal fault.'


class GetTokenFailed(Common):
    _status_code = BASE_CODE + 501
    _status_info = 'Get token failed from vendor.'


class NoTimeStampError(Common):
    _status_code = BASE_CODE + 1001
    _status_info = 'No timestamp in the request params!'


class NoVinError(Common):
    _status_code = BASE_CODE + 1002
    _status_info = 'No vin in the request params!'


class PikaConnectionError(Common):
    _status_code = BASE_CODE + 1003
    _status_info = 'RabbitMQ connected error!'


class WebHandlerError(Common):
    _status_code = BASE_CODE + 1004
    _status_info = 'Error in the handler!'


class SQLConnectError(Common):
    _status_code = BASE_CODE + 1005
    _status_info = 'Database connect error!'


class CacheConnectError(Common):
    _status_code = BASE_CODE + 1006
    _status_info = 'Cache connect error!'


class NoLocationError(Common):
    _status_code = BASE_CODE + 1007
    _status_info = 'No location in the request params!'


class InValidServiceError(Common):
    _status_code = BASE_CODE + 1008
    _status_info = 'Invalid service! Please check the input.'


class VendorAPIError(Common):
    _status_code = BASE_CODE + 1009
    _status_info = 'Vendor API Error!'


class NullLocationError(Common):
    _status_code = BASE_CODE + 1010
    _status_info = 'location is null'


class ParameterTooMuchError(Common):
    _status_code = BASE_CODE + 1011
    _status_info = ' Too much parameter '


class NoDatanumError(Common):
    _status_code = BASE_CODE + 1012
    _status_info = ' No datanum error!'
