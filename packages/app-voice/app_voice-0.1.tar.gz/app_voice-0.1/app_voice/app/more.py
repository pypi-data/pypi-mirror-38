#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午9:16
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : more
# @Contact : xiangwenzhuo@yeah.net
"""

import utils.result as result
import utils.exception as exception
import utils.decorator as decorator
import time
import traceback
import API.demand as dem
import API.live as live
import API.announcers as ann
import logger
import app.collect as col
import app.playhistory as his
import rec.recommend as rec
import database.data_base as db
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


def filters(params):
    """
    function：从推荐的专辑中去掉已收藏的专辑
    :param params: page:系统推荐返回第几页；collect_ids:已收藏专辑的id列表
    :return:
    """
    page = params['page']
    text = {'category_id': 0, 'calc_dimension': 1, 'count': 30, 'page': page}
    album_list = dem.V2AlbumsList(text).get()['albums']
    album_ids = []
    for m in album_list:
        alb_id = str(m['id'])
        album_ids.append(alb_id)
    collect_ids = params['collect_ids']
    show_ids = list(set(album_ids) - set(collect_ids))
    return show_ids


@params_check
def albuminfo(params):
    """
    function: 专辑详情
    :param params:
    page: int 当前第几页，默认1
    count: int 每页多少条，不超过200，默认20
    :return:
        专辑中声音列表
    """
    LOG.info('albuminfo service:')
    LOG.info('params is %s' % params)
    try:
        vin = params['vin']
        if 'uid' in params.keys():
            uid = params['uid']
        else:
            uid = None
        album_id = params['album_id']
        text = {'album_id': album_id}
        res = dem.AlbumsBrowse(text).get()
        try:
            collect_list = col.getcollectalbum(params).response
            collect_ids = []
            for i in collect_list:
                col_id = i['album_id']
                collect_ids.append(col_id)
            album_id = int(album_id)
            if album_id in collect_ids:
                res['isLike'] = True
            else:
                res['isLike'] = False
            conn = init.Connect()
            res['record'] = {}
            record = db.UserTrackRecord(vin, uid, conn).get(album_id)
            record.sort(key=takeTime, reverse=True)
            res['record'] = record[0]
            conn.close()
        except:
            traceback.print_exc()
            LOG.exception('this is an data exception message')
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def radioinfo(params):
    """
    function: 电台详细信息
    :param params:
    page: int 当前第几页，默认1
    count: int 每页多少条，不超过200，默认20
    :return:
    """
    LOG.info('radioinfo service:')
    LOG.info('params is %s' % params)
    try:
        if 'id' in params.keys():
            id = params['id']
            if not len(id):
                return result.ErrorResult(exception.NoIdError())
        else:
            return result.ErrorResult(exception.NoIdError())
        text = {'ids': id, 'radio_id': id}
        res = live.LiveGetradiosbyids(text).get()
        list = live.LiveSchedules(text).get()
        current = live.LiveGetplayingprogram(text).get()
        res['list'] = list
        res['current'] = current
        try:
            collect_list = col.getcollectradio(params).response
            collect_ids = []
            for i in collect_list:
                col_id = i['id']
                collect_ids.append(col_id)
            id = int(id)
            if id in collect_ids:
                res['isLike'] = True
            else:
                res['isLike'] = False
        except:
            traceback.print_exc()
            LOG.exception('this is an data exception message')
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def roewe_rec(params):
    """

    :param params:
    :return:
    """
    LOG.info('roewe_rec service')
    LOG.info('params is %s' % params)
    try:
        vin = params['vin']
        uid = params['uid']
        album_id = rec.RoeweRec(vin, uid).get_recommend()[0]['id']
        params['album_id'] = album_id
        res = albuminfo(params).response
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def announceralbums(params):
    """

    :param params:
    :return:
    """
    LOG.info('announcer albums service')
    LOG.info('param is %s' % params)
    try:
        aid = params['id']
        text = {'aid': aid}
        res = ann.AnnouncersAlbums(text).get()
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError)


@params_check
def announcerinfo(params):
    """

    :param params:
    :return:
    """
    LOG.info('announcer info service')
    LOG.info('param is %s' % params)
    try:
        ids = params['id']
        text = {'ids': ids}
        res = ann.AnnouncersGetbatch(text).get()
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError)


@params_check
def lists(params):
    """

    :param params:
    :return:
    """
    LOG.info('home service:')
    LOG.info('params is %s' % params)
    try:
        vin = params['vin']
        uid = params['uid']
        daily_rec = rec.DailyRec(vin, uid).get_recommend()[0]
        daily_rec['isLike'] = False
        collect_list = col.getcollectalbum(params).response
        collect_list.sort(key=takeTime, reverse=True)
        daily_rec_id = str(rec.DailyRec(vin, uid).get_recommend()[0]['id'])
        collect_ids = [daily_rec_id]
        for i in collect_list:
            col_id = str(i['album_id'])
            collect_ids.append(col_id)
        page = 1
        params['page'] = page
        params['collect_ids'] = collect_ids
        show_ids = filters(params)
        num2 = len(show_ids)
        while num2 < 4:
            page += 1
            params['page'] = page
            show_ids = filters(params)
        ids = ','.join(show_ids)
        body = {'ids': ids}
        show_list = dem.AlbumsGetbatch(body).get()
        num3 = len(collect_list)
        if num3 >= 1:
            if num3 == 1:
                playlist_1 = collect_list[0]
                playlist_1['id'] = collect_list[0]['album_id']
                playlist_2 = show_list[2]
                playlist_1['isLike'] = True
                playlist_2['isLike'] = False
            else:
                playlist_1 = collect_list[0]
                playlist_2 = collect_list[1]
                playlist_1['id'] = collect_list[0]['album_id']
                playlist_2['id'] = collect_list[1]['album_id']
                playlist_1['isLike'] = playlist_2['isLike'] = True
        else:
            playlist_1 = show_list[2]
            playlist_2 = show_list[3]
            playlist_1['isLike'] = playlist_2['isLike'] = False
        params['count'] = 50
        playlist_3 = show_list[0]
        playlist_4 = show_list[1]
        playlist_3['isLike'] = playlist_4['isLike'] = False
        playlist = [playlist_1, playlist_2, playlist_3, playlist_4]
        res = {'album_num': num3, 'daily_rec': daily_rec, 'playlist': playlist}
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def num(params):
    """

    :param params:
    :return:
    """
    LOG.info('num service')
    LOG.info('params is %s' % params)
    try:
        num1 = len(col.getcollecttrack(params).response)
        num2 = len(his.gethistory(params).response)
        res = {'collect_num': num1, 'history_num': num2}
        timestamp = float(params['timestamp'])
        a = time.time() - timestamp
        print('返回时间差%ss' % a)
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


# @params_check
# def home(params):
#     """
#
#     :param params:
#     :return:
#     collect_num: 当前用户收藏声音的数目
#     history_num: 当前用户历史播放数目
#     """
#     LOG.info('home service:')
#     LOG.info('params is %s' % params)
#     try:
#         vin = params['vin']
#         uid = params['uid']
#         text = {'category_id': 0, 'calc_dimension': 1, 'count': 30}
#         roewe_rec = rec.RoeweRec(vin, uid).get_recommend()[0]
#         daily_rec = rec.DailyRec(vin, uid).get_recommend()[0]
#         album_list = dem.V2AlbumsList(text).get()['albums']
#         collect_list = col.getcollectalbum(params).response
#         collect_ids = [roewe_rec['id'], daily_rec['id']]
#         show_list = []
#         for i in collect_list:
#             col_id = i['album_id']
#             collect_ids.append(col_id)
#         for m in album_list:
#             if m['id'] not in collect_ids:
#                 show_list.append(m)
#         data1 = col.getcollecttrack(params).response
#         data2 = his.gethistory(params).response
#         num1, num2, num3 = len(data1), len(data2), len(collect_list)
#         params['count'] = 50
#         playlist_3 = show_list[1]
#         playlist_4 = show_list[2]
#         playlist_3['collect'] = playlist_4['collect'] = 0
#         if num3 >= 1:
#             if num3 == 1:
#                 playlist_1 = collect_list[0]
#                 playlist_1['id'] = collect_list[0]['album_id']
#                 playlist_2 = show_list[0]
#                 playlist_1['collect'] = 1
#                 playlist_2['collect'] = 0
#             else:
#                 playlist_1 = collect_list[0]
#                 playlist_2 = collect_list[1]
#                 playlist_1['collect'] = 1
#                 playlist_2['collect'] = 1
#         else:
#             playlist_1 = show_list[3]
#             playlist_2 = show_list[4]
#             playlist_1['collect'] = playlist_2['collect'] = 0
#         playlist = [playlist_1, playlist_2, playlist_3, playlist_4]
#         res = {'collect_num': num1, 'history_num': num2, 'album_num': num3,
#                'roewe_rec': roewe_rec,
#                'daily_rec': daily_rec, 'playlist': playlist}
#         timestamp = float(params['timestamp'])
#         a = time.time() - timestamp
#         print('返回时间差%ss' % a)
#         return result.MoreInfoResult(res=res)
#     except:
#         traceback.print_exc()
#         return result.ErrorResult(exception.InternalError())
