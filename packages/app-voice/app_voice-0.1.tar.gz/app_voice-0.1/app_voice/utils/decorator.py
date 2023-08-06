#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/7 15:02
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : decorator
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""

import time
import utils.result as result
import utils.exception as exception


def params_check(func):
    def wrapper(params):
        if 'vin' not in params:
            return result.ErrorResult(exception.NoVinError())
        if 'timestamp' not in params:
            return result.ErrorResult(exception.NoTimeStampError())
        params['timestamp'] = time.time()
        if 'uid' not in params:
            params['uid'] = None
        return func(params)
    return wrapper
