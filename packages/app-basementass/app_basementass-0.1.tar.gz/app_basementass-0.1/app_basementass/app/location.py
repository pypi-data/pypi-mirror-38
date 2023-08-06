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
import database.operation as operation
import database.definition as definition
import utils.logger as logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def gpsupdate(params):
    LOG.info('gpsupdate service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        # vin = 'LSJA1234567890118'
        timestamp = params['timestamp']
        if 'location' in params.keys():
            location = params['location']
        else:
            return result.ErrorResult(exception.NoLocationError())
        cache_loc = cache.VehicleLocation(vin)
        cache_loc.set(location)
        LOG.info('vin:%s, location:%s' % (vin, location))
        try:
            conn = definition.Connect()
            trace = operation.UserTrace(vin=vin, conn=conn)
            trace.add(location=location, timestamp=timestamp)
            conn.close()
        except:
            pass
        return result.LocationResult(res='Success.')
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getgps(params):
    LOG.info('getgps service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        cache_loc = cache.VehicleLocation(vin)
        info = cache_loc.last_loc
        print(info)
        if info is None:
            return result.ErrorResult(exception.NoLocationError())
        else:
            return result.LocationResult(res=info.decode('utf-8'))
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())