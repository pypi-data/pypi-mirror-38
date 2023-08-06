#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-10-10 下午3:20
# @Author  : qian.wu
# @Site    : shanghai
# @File    : service
"""

import traceback
import database.operation as operation
import database.definition as definition
import utils.logger as logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def gettrace(params):
    LOG.info('gettrace service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        conn = definition.Connect()
        trace = operation.UserTrace(vin=vin, conn=conn)
        data = trace.get()
        conn.close()
        # print(data)
        return result.TraceResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def selfgettrace(params):
    LOG.info('selfgettrace service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        if 'datanum' in params.keys():
            num = params['datanum']
        else:
            return result.ErrorResult(exception.NoDatanumError())
            # num = 10
        conn = definition.Connect()
        trace = operation.UserTrace(vin=vin, conn=conn)
        data = trace.getn(datanum=num)
        # print(data)
        conn.close()
        return result.TraceResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())