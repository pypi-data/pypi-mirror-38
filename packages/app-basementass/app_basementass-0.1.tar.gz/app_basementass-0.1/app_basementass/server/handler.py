#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-10-10 下午3:20
# @Author  : qian.wu
# @Site    : shanghai
# @File    : service
"""

import traceback
import tornado.web as web
import tornado.gen as gen
import tornado.concurrent as concurrent
import server.response as res
import utils.result as result
import utils.logger as logger
from utils.exception import WebHandlerError, PikaConnectionError, InValidServiceError
import json
import datetime

LOG = logger.get_logger(__name__)


class CommonHandler(web.RequestHandler):
    """
    common handler for the request.
    """
    mod = __import__('app.test', globals(), locals(), ['object'], 0)
    executor = concurrent.futures.ThreadPoolExecutor(200)

    @web.asynchronous
    @gen.coroutine
    def post(self, service):
        """

        :param service:
        :return:
        """
        starttime = datetime.datetime.now()
        path = self.request.path
        try:
            self.pika_connect()
        except PikaConnectionError:
            traceback.print_exc()
            LOG.info('Rabbitmq connect failure.')
        try:
            body_params = self.request.body
            if body_params.decode('utf-8'):
                params = json.loads(body_params.decode('utf-8'))
            else:
                params = {}
            params['ip'] = self.request.remote_ip
            LOG.info('request params:%s', params)
            app_result = yield self.async_fun(service, params)
        except Exception:
            traceback.print_exc()
            app_result = result.ErrorResult(WebHandlerError())
        return_info = res.Response(app_result, path, 'POST').info
        message = app_result.message
        self.set_header("Content-Type", "application/json")
        self.set_header("Status_code", app_result.status_code)
        self.set_header("Status_info", app_result.status_info)
        self.write(return_info)
        self.finish()
        endtime = datetime.datetime.now()
        print(
            "----------------------------------------------------------------------------------------------------------")
        print(endtime - starttime)
        print(
            "----------------------------------------------------------------------------------------------------------")
        if message is not None:
            self.application.mq.channel.queue_declare(callback=None,
                                                      queue='map',
                                                      durable=True)
            self.application.mq.channel.basic_publish(exchange='',
                                                      routing_key='map',
                                                      body=json.dumps(message))

    def pika_connect(self):
        """

        :return:
        """
        self.application.mq.connect()

    @concurrent.run_on_executor
    def async_fun(self, service, params):
        """

        :param service:
        :param params:
        :return:
        """
        if service in self.mod.__dict__:
            func = getattr(self.mod, service)
            return func(params)
        else:
            return result.ErrorResult(InValidServiceError())


class BaseLocationHandler(CommonHandler):
    """
    Basement gps handler
    """
    mod = __import__('app.location', globals(), locals(), ['object'], 0)


class BaseTraceHandler(CommonHandler):
    """
    Basement trace handler
    """
    mod = __import__('app.trace', globals(), locals(), ['object'], 0)


class BaseVehiclesHandler(CommonHandler):
    """
    Basement vehicles handler
    """
    mod = __import__('app.vehicles', globals(), locals(), ['object'], 0)
