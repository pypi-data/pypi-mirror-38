#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午9:09
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : collect
# @Contact : xiangwenzhuo@yeah.net
"""
import traceback
from utils import logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception
import database.data_base as db
import database.base_init as init

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


def takeTime(elem):
    return elem['time']


@params_check
def getcollecttrack(params):
    '''获取收藏的声音'''
    LOG.info('get collect service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            data = db.CollectTrack(vin, uid).get()
        else:
            vin = params['vin']
            uid = None
            data = db.CollectTrack(vin, uid).get()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        for i in data:
            i['id'] = i['track_id']
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addcollecttrack(params):
    '''收藏声音'''
    LOG.info('add collect service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'track_id' in params.keys():
            try:
                track_id = params['track_id']
            except:
                return result.ErrorResult(exception.NoTrackIdError())
            if 'uid' in params.keys():
                uid = params['uid']
                vin = params['vin']
                conn = init.Connect()
                data = db.CollectTrack(vin, uid, conn).add(timestamp, track_id)
                conn.close()
            else:
                vin = params['vin']
                uid = None
                conn = init.Connect()
                data = db.CollectTrack(vin, uid, conn).add(timestamp, track_id)
                conn.close()
            if data is False:
                return result.ErrorResult(exception.SQLConnectError())
            return result.CollectResult(res=data)
        else:
            return result.ErrorResult(exception.NoTrackIdError())

    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def cancelcollecttrack(params):
    '''取消收藏声音'''
    LOG.info('cancel collect service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'track_id' in params.keys():
            track_id = params['track_id']
            if not len(track_id):
                return result.ErrorResult(exception.NoTrackIdError())
            if 'uid' in params.keys():
                uid = params['uid']
                vin = params['vin']
                conn = init.Connect()
                data = db.CollectTrack(vin, uid, conn).cancel(timestamp, track_id)
                conn.close()
            else:
                vin = params['vin']
                uid = None
                conn = init.Connect()
                data = db.CollectTrack(vin, uid, conn).cancel(timestamp, track_id)
                conn.close()
            if data is False:
                return result.ErrorResult(exception.SQLConnectError())
            return result.CollectResult(res=data)
        else:
            return result.ErrorResult(exception.NoTrackIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getcollectplaylist(params):
    '''获取用户收藏听单'''
    LOG.info('get collect list service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            data = db.CollectPlayList(vin, uid, conn).get()
            conn.close()
        else:
            vin = params['vin']
            uid = None
            conn = init.Connect()
            data = db.CollectPlayList(vin, uid, conn).get()
            conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addcollectplaylist(params):
    '''收藏听单'''
    LOG.info('add collect list service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'playlistid' in params.keys():
            playlistid = params['playlistid']
            if 'uid' in params.keys():
                uid = params['uid']
                vin = params['vin']
                conn = init.Connect()
                data = db.CollectPlayList(vin, uid, conn).add(timestamp, playlistid)
                conn.close()
            else:
                vin = params['vin']
                uid = None
                conn = init.Connect()
                data = db.CollectPlayList(vin, uid, conn).add(timestamp, playlistid)
                conn.close()
            if data is False:
                return result.ErrorResult(exception.SQLConnectError())
            return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def cancelcollectplaylist(params):
    '''取消收藏听单'''
    LOG.info('cancel collect list service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'playlistid' in params.keys():
            playlistid = params['playlistid']
            if 'uid' in params.keys():
                uid = params['uid']
                vin = params['vin']
                conn = init.Connect()
                data = db.CollectPlayList(vin, uid, conn).cancel(timestamp, playlistid)
                conn.close()
            else:
                vin = params['vin']
                uid = None
                conn = init.Connect()
                data = db.CollectPlayList(vin, uid, conn).cancel(timestamp, playlistid)
                conn.close()
            if data is False:
                return result.ErrorResult(exception.SQLConnectError())
            return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getcollectalbum(params):
    """
    get collect albums
    :param params:
    :return:
    """
    LOG.info('get collect album service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            data = db.CollectAlbum(vin, uid, conn).get()
            conn.close()
        else:
            vin = params['vin']
            uid = None
            conn = init.Connect()
            data = db.CollectAlbum(vin, uid, conn).get()
            conn.close()
        for i in data:
            i['id'] = i['album_id']
        data.sort(key=takeTime, reverse=True)
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addcollectalbum(params):
    """
    add collect album
    :param params:
    :return:
    """
    LOG.info('add collect album service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'album_id' in params.keys():
            album_id = params['album_id'].split()
            if not len(album_id):
                return result.ErrorResult(exception.NoArtistIdError())
            vin = params['vin']
            if 'uid' in params.keys():
                uid = params['uid']
            else:
                uid = None
            for i in album_id:
                conn = init.Connect()
                data = db.CollectAlbum(vin, uid, conn).add(timestamp, i)
                conn.close()
                if data is False:
                    return result.ErrorResult(exception.SQLConnectError())
                    break
                else:
                    data = data
            return result.CollectResult(res=data)
        else:
            return result.ErrorResult(exception.NoArtistIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def cancelcollectalbum(params):
    """
    cacel collect album
    :param params:
    :return:
    """
    LOG.info('cancel collect album server:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'album_id' in params.keys():
            album_id = params['album_id'].split()
            if not len(album_id):
                return result.ErrorResult(exception.NoAlbumIdError())
            vin = params['vin']
            if 'uid' in params.keys():
                uid = params['uid']
            else:
                uid = None
            for i in album_id:
                conn = init.Connect()
                data = db.CollectAlbum(vin, uid, conn).cancel(timestamp, i)
                conn.close()
                if data is False:
                    return result.ErrorResult(exception.SQLConnectError())
                    break
                else:
                    data = data
            return result.CollectResult(res=data)
        else:
            return result.ErrorResult(exception.NoAlbumIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getcollectradio(params):
    """
    get collect radio
    :param params:
    :return:
    """
    LOG.info('get collect radio service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            data = db.CollectRadio(vin, uid, conn).get()
            conn.close()
        else:
            vin = params['vin']
            uid = None
            conn = init.Connect()
            data = db.CollectRadio(vin, uid, conn).get()
            conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addcollectradio(params):
    """
    add collect radio
    :param params:
    :return:
    """
    LOG.info('add collect radio service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'id' in params.keys():
            id = params['id'].split()
            if not len(id):
                return result.ErrorResult(exception.NoIdError())
            vin = params['vin']
            if 'uid' in params.keys():
                uid = params['uid']
            else:
                uid = None
            for i in id:
                conn = init.Connect()
                data = db.CollectRadio(vin, uid, conn).add(timestamp, i)
                conn.close()
                if data is False:
                    return result.ErrorResult(exception.SQLConnectError())
                    break
                else:
                    data = data
            return result.CollectResult(res=data)
        else:
            return result.ErrorResult(exception.NoIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def cancelcollectradio(params):
    """
    cacel collect radio
    :param params:
    :return:
    """
    LOG.info('cancel collect radio server:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'id' in params.keys():
            id = params['id'].split()
            if not len(id):
                return result.ErrorResult(exception.NoIdError())
            vin = params['vin']
            if 'uid' in params.keys():
                uid = params['uid']
            else:
                uid = None
            for i in id:
                conn = init.Connect()
                data = db.CollectRadio(vin, uid, conn).cancel(timestamp, i)
                conn.close()
                if data is False:
                    return result.ErrorResult(exception.SQLConnectError())
                    break
                else:
                    data = data
            return result.CollectResult(res=data)
        else:
            return result.ErrorResult(exception.NoIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getcollectannouncer(params):
    """
    get collect announcer
    :param params:
    :return:
    """
    LOG.info('get collect announcer service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            data = db.CollectAnnouncer(vin, uid, conn).get()
            conn.close()
        else:
            vin = params['vin']
            uid = None
            conn = init.Connect()
            data = db.CollectAnnouncer(vin, uid, conn).get()
            conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addcollectannouncer(params):
    """
    add collect radio
    :param params:
    :return:
    """
    LOG.info('add collect announcer service:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'id' in params.keys():
            id = params['id'].split()
            vin = params['vin']
            if 'uid' in params.keys():
                uid = params['uid']
            else:
                uid = None
            for i in id:
                conn = init.Connect()
                data = db.CollectAnnouncer(vin, uid, conn).add(timestamp, i)
                conn.close()
                if data is False:
                    return result.ErrorResult(exception.SQLConnectError())
                    break
                else:
                    data = data
            return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def cancelcollectannouncer(params):
    """
    cacel collect announcer
    :param params:
    :return:
    """
    LOG.info('cancel collect announcer server:')
    LOG.info('params is %s' % params)
    try:
        timestamp = params['timestamp']
        if 'id' in params.keys():
            id = params['id'].split()
            vin = params['vin']
            if 'uid' in params.keys():
                uid = params['uid']
            else:
                uid = None
            for i in id:
                conn = init.Connect()
                data = db.CollectAnnouncer(vin, uid, conn).cancel(timestamp, i)
                conn.close()
                if data is False:
                    return result.ErrorResult(exception.SQLConnectError())
                    break
                else:
                    data = data
            return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getcollect(params):
    """
    get collect radio and album
    :param params:
    :return:
    """
    LOG.info('get collect radio service:')
    LOG.info('params is %s' % params)
    try:
        if 'uid' in params.keys():
            uid = params['uid']
            vin = params['vin']
            conn = init.Connect()
            data_1 = db.CollectRadio(vin, uid, conn).get()
            data_2 = db.CollectAlbum(vin, uid, conn).get()
            conn.close()
            data = []
            for i in data_1:
                i['kind'] = 'radio'
                data.append(i)
            for n in data_2:
                n['kind'] = 'album'
                data.append(n)
        else:
            vin = params['vin']
            uid = None
            conn = init.Connect()
            data_1 = db.CollectRadio(vin, uid, conn).get()
            data_2 = db.CollectAlbum(vin, uid, conn).get()
            conn.close()
            data = []
            for i in data_1:
                i['kind'] = 'radio'
                data.append(i)
            for n in data_2:
                n['kind'] = 'album'
                data.append(n)
        data.sort(key=takeTime, reverse=True)
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
