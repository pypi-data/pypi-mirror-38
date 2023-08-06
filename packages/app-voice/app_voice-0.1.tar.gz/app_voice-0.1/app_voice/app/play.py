#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午9:14
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : play
# @Contact : xiangwenzhuo@yeah.net
"""

import database.data_base as db
import database.base_init as base_definition
import time
import API.demand as dem
import app.collect as col
import traceback
from utils import logger
import utils.result as result
import utils.exception as exception
import utils.decorator as decorator
import database.base_init as init


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


def takeTime(elem):
    """
    function: 提取time字段
    :param elem:
    :return:
    """
    return elem['time']


@params_check
def play(params):
    '''播放声音'''
    LOG.info('play service:')
    LOG.info('params is %s' % params)
    try:
        vin = params['vin']
        timestamp = params['timestamp']
        if 'ids' in params.keys():
            ids = params['ids']
            if not len(ids):
                return result.ErrorResult(exception.NoIdsError())
        else:
            return result.ErrorResult(exception.NoIdsError())
        if 'uid' in params.keys():
            uid = params['uid']
        else:
            uid = None
        text = {'ids': ids}
        res = dem.TracksGetbatch(text).get()
        try:
            conn = base_definition.Connect()
            his = db.TracksHistoryList(vin, uid, conn)
            his.add(timestamp, ids)
            conn.close()
            collect_list = col.getcollecttrack(params).response
            collect_ids = []
            for i in collect_list:
                col_id = i['track_id']
                collect_ids.append(col_id)
            ids = int(ids)
            if ids in collect_ids:
                res['tracks'][0]['isLike'] = True
            else:
                res['tracks'][0]['isLike'] = False
        except:
            traceback.print_exc()
            LOG.exception('this is an data exception message')
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.PlayResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def index(params):
    '''返回标识位'''
    LOG.info('play service:')
    LOG.info('params is %s' % params)
    try:
        vin = params['vin']
        timestamp = params['timestamp']
        if 'ids' in params.keys():
            ids = params['ids']
        else:
            return result.ErrorResult(exception.NoTrackIdError())
        if 'uid' in params.keys():
            uid = params['uid']
        else:
            uid = None
        conn = init.Connect()
        record = db.UserTrackRecord(vin, uid, conn).get_position(ids)
        conn.close()
        if len(record) == 0:
            res = {}
        else:
            record.sort(key=takeTime, reverse=True)
            res = record[0]
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.PlayResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getlastplaytrack(params):
    '''获取上次播放所在页的声音'''
    LOG.info('getlasttrack service')
    LOG.info('param is %s' % params)
    try:
        if 'album_id' in params.keys():
            album_id = params['album_id']
        else:
            return result.ErrorResult(exception.NoAlbumIdError())
        if 'track_id' in params.keys():
            track_id = params['track_id']
        else:
            return result.ErrorResult(exception.NoTrackIdError)
        text = {'album_id': album_id, 'track_id': track_id}
        res = dem.TracksGetlastplaytracks(text).get()
        return result.PlayResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def record(params):
    """

    :param params:
    :return:
    """
    LOG.info('get last play record service')
    LOG.info('param is %s' % params)
    try:
        vin = params['vin']
        album_id = params['album_id']
        track_id = params['track_id']
        position = params['position']
        timestamp = params['timestamp']
        if 'uid' in params.keys():
            uid = params['uid']
        else:
            uid = None
        conn = base_definition.Connect()
        data = db.UserTrackRecord(vin, uid, conn).add(timestamp, album_id,
                                                         track_id, position)
        conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())

