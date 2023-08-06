#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-22 下午2:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : cache
# @Contact : guangze.yu@foxmail.com
"""

import database.data_base as db
import redis
import json
import traceback
import datetime

pool = redis.ConnectionPool(host='127.0.0.1', password='Root1q2w', port=6379)
cache = redis.Redis(connection_pool=pool)


class Common(object):
    def __init__(self, vin, uid=None, Conn=cache):
        self._vin = vin
        self._uid = uid
        self._conn = Conn


class SearchWordHistory(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(SearchWordHistory, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                out = cache.hget(self._uid,'VoiceSearchWordHistory')
            else:
                out = cache.hget(self._vin,'VoiceSearchWordHistory')
            if out is None:
                dbout = db.SearchWordHistory(self._vin, self._uid)
                if dbout is None:
                    dbout = []
                cache.hset(self._uid, 'VoiceSearchWordHistory',json.dumps(dbout))
                info = dbout
            else:
                info = json.loads(out)
            return info
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def clear(self):
        try:
            if self._uid is None:
                info = cache.hget(self._vin, 'VoiceSearchWordHistory')
            else:
                info = cache.hget(self._uid, 'VoiceSearchWordHistory')
            if info is None or info == []:
                return True
            else:
                cache.hset(self._uid,'VoiceSearchWordHistory',json.dumps([]))
                db.SearchWordHistory(self._vin,self._uid).clear()
                return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, keyword):
        try:
            db.SearchWordHistory(self._vin,self._uid).add(timestamp,keyword)
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            cacheinfo = cache.hget(uid,'VoiceSearchWordHistory')
            if cacheinfo is None:
                cache.hset(uid, 'VoiceSearchWordHistory', json.dumps([{'keyword':keyword}]))
                return True
            else:
                info = json.loads(cacheinfo)
                keywords = [i['keyword'] for i in info]
                try:
                    index = keywords.index(keyword)
                    info.__delitem__(index)
                    info.append({'keyword':keyword})
                    cache.hset(uid,'VoiceSearchWordHistory',json.dumps(info))
                except:
                    info.append({'keyword': keyword})
                    cache.hset(uid,'VoiceSearchWordHistory',json.dumps(info))
                return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class TracksHistoryList(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(TracksHistoryList, self).__init__(vin, uid, Conn)

    def get(self, starttime=datetime.datetime.now()-datetime.timedelta(180), endtime=datetime.datetime.now()):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'TracksHistoryList')
            if out is None:
                dbout = db.TracksHistoryList(self._vin,self._uid).get(starttime, endtime)
                if dbout is None or dbout==[]:
                    dbout = []
                info = dbout
                cache.hset(uid,'TracksHistoryList',json.dumps(dbout))
                return info
            else:
                info = json.loads(out)
                return info
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, itemid):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            db.TracksHistoryList(self._vin,self._uid).add(timestamp,itemid)
            info = db.TracksHistoryList(self._vin,self._uid).get()
            cache.hset(uid,'TracksgHistoryList',json.dumps(info))
            statinfo = db.TracksHistoryList(self._vin,self._uid).stat()
            cache.hset(uid, 'TracksHistoryListStat', json.dumps(statinfo))
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def stat(self, n=50, starttime=datetime.datetime.now()-datetime.timedelta(180), endtime=datetime.datetime.now()):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'TracksHistoryListStat')
            if out is None:
                info = db.TracksHistoryList(self._vin,self._uid).stat(n,starttime,endtime)
                cache.hset(uid,'TracksHistoryListStat',json.dumps(info))
                return info
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class CollectSong(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(CollectSong, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'CollectTrack')
            if out is None:
                dbout = db.CollectTrack(self._vin,self._uid).get()
                cache.hset(uid,'CollectTrack',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, itemid):
        try:
            db.CollectTrack(self._vin,self._uid).add(timestamp,itemid)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self, timestamp, itemid):
        try:
            db.CollectTrack(self._vin,self._uid).cancel(timestamp,itemid)
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class CollectPlayList(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(CollectPlayList, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'VoiceCollectPlayList')
            if out is None:
                dbout = db.CollectPlayList(self._vin,self._uid).get()
                cache.hset(uid,'VoiceCollectPlayList',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, playlistid, selflist=False):
        try:
            db.CollectPlayList(self._vin,self._uid).add(timestamp,playlistid,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self,timestamp, playlistid, selflist=False):
        try:
            db.CollectPlayList(self._vin,self._uid).cancel(timestamp,playlistid,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class CollectAlbum(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(CollectAlbum, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'VoiceCollectAlbum')
            if out is None:
                dbout = db.CollectAlbum(self._vin,self._uid).get()
                cache.hset(uid,'VoiceCollectAlbum',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, album_id, selflist=False):
        try:
            db.CollectAlbum(self._vin,self._uid).add(timestamp,album_id,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self,timestamp, album_id, selflist=False):
        try:
            db.CollectAlbum(self._vin,self._uid).cancel(timestamp,album_id,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class CollectRadio(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(CollectRadio, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'VoiceCollectRadio')
            if out is None:
                dbout = db.CollectAlbum(self._vin,self._uid).get()
                cache.hset(uid,'VoiceCollectRadio',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, id, selflist=False):
        try:
            db.CollectRadio(self._vin,self._uid).add(timestamp,id,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self,timestamp, id, selflist=False):
        try:
            db.CollectRadio(self._vin,self._uid).cancel(timestamp,id,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class UserPlaylist(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(UserPlaylist, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'VoiceUserPlaylist')
            if out is None:
                dbout = db.UserPlaylist(self._vin,self._uid).get()
                cache.hset(uid,'VoiceUserPlaylist',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            return False

    def create(self,playlistname):
        try:
            db.UserPlaylist(self._vin,self._uid).create(playlistname)
            return True
        except:
            traceback.print_exc()
            return False

    def add(self, timestamp, playlistid, itemid):
        try:
            db.UserPlaylist(self._vin, self._uid).add(timestamp,playlistid,itemid)
            return True
        except:
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, playlistid, itemid):
        try:
            db.UserPlaylist(self._vin,self._uid).cancel(timestamp, playlistid, itemid)
            return True
        except:
            traceback.print_exc()
            print('cancel failre')
            return False

    def getplaylistcontent(self, playlistid):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'VoiceUserPlaylistContent')
            if out is None:
                dbout = db.UserPlaylist(self._vin,self._uid).getplaylistcontent(playlistid)
                cache.hset(uid,'VoiceUserPlaylistContent',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('getplaylistcontent failre')
            return False


class CollectAnnouncer(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(CollectAnnouncer, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid,'VoiceCollectAnnouncer')
            if out is None:
                dbout = db.CollectAnnouncer(self._vin,self._uid).get()
                cache.hset(uid,'VoiceCollectAnnouncer',json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, id, selflist=False):
        try:
            db.CollectAnnouncer(self._vin,self._uid).add(timestamp,id,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self,timestamp, id, selflist=False):
        try:
            db.CollectAnnouncer(self._vin,self._uid).cancel(timestamp,id,selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False
