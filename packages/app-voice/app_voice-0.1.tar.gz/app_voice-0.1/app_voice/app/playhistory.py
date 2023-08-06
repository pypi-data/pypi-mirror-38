#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午9:11
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : playhistory
# @Contact : xiangwenzhuo@yeah.net
"""

import utils.result as result
import utils.exception as exception
import utils.decorator as decorator
import database.base_init as init
import traceback
import database.data_base as db
import logger
import datetime

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def gethistory(params):
    '''历史记录'''
    LOG.info('playhistory service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            historylist = db.TracksHistoryList(vin, uid, conn).get()
            conn.close()
        else:
            vin = params['vin']
            conn = init.Connect()
            historylist = db.TracksHistoryList(vin, conn).get()
            conn.close()
        historylist = historylist[0:100]
        for i in historylist:
            i['id'] = i['track_id']
        return result.PlayHistoryResult(res=historylist)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def clearhistory(params):
    """清空历史记录"""
    LOG.info('clear playhistory service:')
    LOG.info('params is %s', params)
    # end_time = datetime.datetime.now()
    # start_time = end_time - datetime.timedelta(180)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            historylist = db.TracksHistoryList(vin, uid, conn).clear()
            conn.close()
        else:
            uid = None
            vin = params['vin']
            conn = init.Connect()
            historylist = db.TracksHistoryList(vin, uid, conn).clear()
            conn.close()
        return result.PlayHistoryResult(res=historylist)
    except exception.InternalError:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())