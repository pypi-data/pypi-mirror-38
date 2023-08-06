#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午9:07
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : search
# @Contact : xiangwenzhuo@yeah.net
"""

import API.search as api
import logging
import database.data_base as db
import datetime
import traceback
import database.base_init as base
from utils import logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception


LOG = logger.get_logger(__name__)
params_check = decorator.params_check

Connection = base.Connect()


@params_check
def hotwords(params):
    '''获取最新热搜词'''
    LOG.info('hotwords service:')
    LOG.info('params is %s' % params)
    try:
        if 'top' in params.keys():
            top = params['top']
            if not len(top):
                return result.ErrorResult(exception.NoTopError())
            text = {'top': top}
            res = api.SearchHotwords(text).get()
            return result.SearchResult(res=res)
        else:
            return result.ErrorResult(exception.NoTopError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def suggestwords(params):
    '''获取某个关键词的联想词'''
    LOG.info('searchsuggestwords service')
    LOG.info('params is %s' % params)
    try:
        if 'q' in params.keys():
            q = params['q']
            if not len(q):
                return result.ErrorResult(exception.NoKeyWordError())
            text = {'q': q}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        res = api.SearchSuggestwords(text).get()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def album(params):
    '''获取专辑'''
    logging.info('searchalbums service')
    logging.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        vin = params['vin']
        if 'q' in params.keys():
            q = params['q']
            text = {'q': q}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        try:
            his = db.SearchWordHistory(vin, uid=None)
            his.add(timestamp, q)
        except:
            traceback.print_exc()
            logging.exception('this is an data exception message')
        res = api.SearchAlbums(text).get()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def track(params):
    '''获取声音'''
    LOG.info('searchtracks service')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        vin = params['vin']
        if 'q' in params.keys():
            q = params['q']
            text = {'q': q}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        try:
            his = db.SearchWordHistory(vin, uid=None)
            his.add(timestamp, q)
        except:
            traceback.print_exc()
            logging.exception('this is an data exception message')
        res = api.SearchTracks(text).get()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def radio(params):
    '''获取直播'''
    LOG.info('searchradios service')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        vin = params['vin']
        if 'q' in params.keys():
            q = params['q']
            text = {'q': q}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        try:
            his = db.SearchWordHistory(vin, uid=None)
            his.add(timestamp, q)
        except:
            traceback.print_exc()
            logging.exception('this is an data exception message')
        res = api.SearchRadios(text).get()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def announcer(params):
    '''获取主播'''
    LOG.info('searchannouncers service')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        vin = params['vin']
        if 'q' in params.keys():
            q = params['q']
            text = {'q': q}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        try:
            his = db.SearchWordHistory(vin, uid=None)
            his.add(timestamp, q)
        except:
            traceback.print_exc()
            LOG.exception('this is an data exception message')
        res = api.SearchAnnouncers(text).get()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def all(params):
    '''获取指定数量直播，声音，专辑的内容'''
    LOG.info('searchall service')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        vin = params['vin']
        if 'q' in params.keys():
            q = params['q']
            if not len(q):
                return result.ErrorResult(exception.NoKeyWordError())
            text = {'q': q}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        try:
            his = db.SearchWordHistory(vin, uid=None)
            his.add(timestamp, q)
        except:
            traceback.print_exc()
            LOG.exception('this is an data exception message')
        res = api.SearchAll(text).get()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def gethistory(params):
    """获取搜索记录"""
    LOG.info('gethistory service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        conn = base.Connect()
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(180)
        his = db.SearchWordHistory(vin, uid, conn)
        res = his.get(start_time, end_time)
        conn.close()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def clearhistory(params):
    """清空搜索记录"""
    LOG.info('delhistory service:')
    LOG.info('params is %s', params)
    try:
        # info = params
        # message = mess.SearchWordsHistory(method='clear', info=info)
        # res = 'Success.'
        # return result.SearchResult(res=res, message=message)
        vin = params['vin']
        uid = params['uid']
        conn = base.Connect()
        his = db.SearchWordHistory(vin, uid, conn)
        res = his.clear()
        conn.close()
        if res:
            return result.SearchResult(res='Success.')
        return result.ErrorResult(exception.SQLConnectError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
