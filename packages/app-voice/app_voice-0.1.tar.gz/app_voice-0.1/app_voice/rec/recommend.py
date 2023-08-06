#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/6/5 8:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : daliy_rec
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""

import database.base_init as base_definition
import database.data_base as base_operation
import API.recommend as recommend
import API.ranks as ranks
import API.album as album


class RoeweRec(object):

    def __init__(self, vin, uid=None):
        """

        :param vin:
        :param uid:
        """
        self._vin = vin
        self._uid = uid
        self._conn = base_definition.Connect()
        self._history = base_operation.TracksHistoryList(vin, uid, self._conn).stat()
        self._track_his = self._history['track']
        self._album_his = self._history['album']
        self._artist_his = self._history['artist']
        self._conn.close()

    def get_recommend(self):
        album_byalbum = self._album_relative_by_playnums()
        album_bytrack = self._track_relative_by_playnums()
        album_byalbum.update(album_bytrack)
        return list(album_byalbum.values())

    def _album_relative_by_playnums(self, n=5):
        if len(self._album_his) == 0:
            params = {'device_type': 1, 'device_id': 'E4B3185B0932'}
            res = recommend.AlbumsGuesslike(params).get()
            out = {}
            temp = {str(j['id']): j for j in res}
            out.update(temp)
        else:
            album = self._album_his[:min(len(self._album_his), n)]
            out = {}
            for i in album:
                s = {'albumId': i['albumid']}
                res = recommend.AlbumsRelativealbum(s).get()
                temp = {str(j['id']): j for j in res['reletive_albums']}
                out.update(temp)
        return out

    def _track_relative_by_playnums(self, n=5):
        tracks = self._track_his[:min(len(self._album_his), n)]
        out = {}
        for i in tracks:
            s = {'trackId': i['track_id']}
            res = recommend.TracksRelativealbum(s).get()
            temp = {str(j['id']): j for j in res['reletive_albums']}
            out.update(temp)
        return out


class DailyRec(object):

    def __init__(self, vin=None, uid=None):
        """

        :param vin:
        :param uid:
        """
        self._vin = vin
        self._uid = uid

    def get_rank_id_list(self):
        s = {'rank_type': 1}
        res = ranks.RanksIndexlist(s).get()
        return list(set([j['id'] for i in res for j in i['index_rank_items']]))

    def get_recommend(self):
        ids = ''
        for i in self.get_rank_id_list():
            ids += str(i) + ','
        ids = {'ids': ids.strip(',')}
        res = album.GetBatch(ids).get()
        return res
