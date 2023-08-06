#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-10-10 下午3:20
# @Author  : qian.wu
# @Site    : shanghai
# @File    : service
"""

from json import load
import tornado.web as web
import server.handler as handler
import tornado.ioloop as ioloop
from tornado.options import options, define
from kazoo.client import KazooClient
from utils import logger
import mq.mq_client as mq_client
import config.zookeepr as config
from urllib.request import urlopen


LOG = logger.get_logger(__name__)
IP = load(urlopen('http://ip-api.com/json'))['query']

define('port', default=8889, type=int, help='Server port')
define('bind', default='0.0.0.0', type=str, help='Server bind')
define('zk_connect',
       default=config.zookeeper_host,
       type=str,
       help='zookeeper connect')

ZK = KazooClient(hosts=options.zk_connect)


def zk_stats():
    """

    :return:
    """
    if ZK.state == 'LOST':
        LOG.info('zookeeper state:%s' % ZK.state)
        ZK.start()


if __name__ == "__main__":
    TestHandler = handler.CommonHandler
    LocationHandler = handler.BaseLocationHandler
    TraceHandler = handler.BaseTraceHandler
    VehiclesHandler = handler.BaseVehiclesHandler
    handlers = [(r'/basementass/test/(.*)', TestHandler),
                (r'/basementass/location/(.*)', LocationHandler),
                (r'/basementass/trace/(.*)', TraceHandler),
                (r'/basementass/vehicles/(.*)', VehiclesHandler)]
    app = web.Application(handlers)
    setattr(app, 'options', options)
    app.listen(options.port, address=options.bind)
    ZK.start()
    if ZK.exists('/roewe_server') is None:
        ZK.create('/roewe_server')
    if ZK.exists('/roewe_server/basementass') is None:
        ZK.create('/roewe_server/basementass')
    if ZK.exists('/roewe_server/basementass/%s:%s' % (IP, options.port)) is None:
        ZK.create(path='/roewe_server/basementass/%s:%s' % (IP, options.port), ephemeral=True)
    ioloop.PeriodicCallback(zk_stats, 100000).start()
    # ioloop.PeriodicCallback(gpsupdate, 1000).start()
    main_loop = ioloop.IOLoop.instance()
    mq_conn = mq_client.PikaClient(main_loop)
    setattr(app, 'mq', mq_conn)
    main_loop.start()
