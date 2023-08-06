#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-10-10 下午3:20
# @Author  : qian.wu
# @Site    : shanghai
# @File    : service
"""

import traceback
import database.cache as cache
import utils.logger as logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


def getvehicles(params):
    LOG.info('getvehicles service:')
    LOG.info('params is %s', params)
    try:
        vinall = cache.VehicleKeys('park').get()
        return result.VehiclesResult(res=vinall)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
