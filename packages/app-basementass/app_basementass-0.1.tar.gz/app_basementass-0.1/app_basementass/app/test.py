#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-26 下午2:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : test
# @Contact : guangze.yu@foxmail.com
"""
import time
import utils.logger as logger
import utils.result as result

LOG = logger.get_logger(__name__)


def sleepout(params):
    """

    :param params:
    :return:
    """
    print(params)
    LOG.info('Params:%s', params)
    time.sleep(1)
    return result.TestResult(res='Hello!')
