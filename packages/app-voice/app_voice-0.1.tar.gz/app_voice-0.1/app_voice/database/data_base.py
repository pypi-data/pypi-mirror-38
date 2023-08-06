#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 上午8:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : data_base
# @Contact : guangze.yu@foxmail.com
"""

import database.base_init as base
import datetime
import API.demand as demand_api
import API.column as column_api
import API.live as live_api
import API.announcers as ann
import traceback
import json

Connection = base.Connect()


def takeTime(elem):
    """
    function: 提取time字段
    :param elem:
    :return:
    """
    return elem['time']


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class Common(object):
    def __init__(self, vin, uid=None, conn=Connection):
        self._vin = vin
        self._uid = uid
        self._conn = conn


class SearchWordHistory(Common):
    def __init__(self, vin, uid=None, conn=Connection):
        super(SearchWordHistory, self).__init__(vin, uid, conn)

    def get(self, start_time=None, end_time=None):
        starttime = start_time if start_time else datetime.datetime.now() - datetime.timedelta(720)
        endtime = end_time if end_time else datetime.datetime.now()
        try:
            if self._uid is None:
                query = ("SELECT "
                         "tb_searchword_history.keyword, "
                         "group_concat(tb_searchword_history.time "
                         "ORDER by tb_searchword_history.time DESC) "
                         "from tb_searchword_history "
                         "where tb_searchword_history.showinlist=1 "
                         "and tb_searchword_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_searchword_history.uid is NULL "
                         "AND tb_searchword_history.vin='%s' "
                         "group by tb_searchword_history.keyword "
                         "ORDER BY group_concat(tb_searchword_history.time "
                         "ORDER by tb_searchword_history.time DESC) DESC;"
                         % (starttime, endtime, self._vin))
            else:
                query = ("select "
                         "tb_searchword_history.keyword, "
                         "group_concat(tb_searchword_history.time "
                         "ORDER by tb_searchword_history.time DESC) "
                         "from tb_searchword_history "
                         "where tb_searchword_history.showinlist=1 "
                         "and tb_searchword_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_searchword_history.uid='%s' "
                         "group by tb_searchword_history.keyword "
                         "ORDER BY group_concat(tb_searchword_history.time "
                         "ORDER by tb_searchword_history.time DESC) DESC;"
                         % (starttime, endtime, self._uid))
            # log.info(query)
            data = self._conn.session.execute(query)
            out = [{'keyword': i[0]} for i in data]
            # log.info(out)
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def clear(self):
        try:
            query = self._conn.session.query(base.UserSearchKeyWordHistory)
            data = query.filter_by(vin=self._vin,
                                   uid=self._uid,
                                   showinlist=True).all()
            for i in data:
                i.showinlist = False
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('clear failre')
            return False

    def add(self, timestamp, keyword):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            data = {'uid': self._uid,
                    'vin': self._vin,
                    'time': time_array,
                    'keyword': keyword,
                    'showinlist': True}
            add_item = (base.UserSearchKeyWordHistory(**data))
            self._conn.session.add(add_item)
            self._conn.commit()
            self._conn.close()
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False


class TracksHistoryList(Common):
    def __init__(self, vin, uid=None, Conn=Connection):
        super(TracksHistoryList, self).__init__(vin, uid, Conn)

    def get(self, start_time=None, end_time=None):
        starttime = start_time if start_time else datetime.datetime.now()-datetime.timedelta(720)
        endtime = end_time if end_time else datetime.datetime.now()
        try:
            if self._uid is None:
                query = ("SELECT "
                         "tb_tracks_history.track_id, "
                         "tb_tracks_history.track_title,"
                         "tb_tracks_history.cover_url_small,"
                         "tb_tracks_history.cover_url_middle,"
                         "tb_tracks_history.cover_url_large,"
                         "tb_tracks_history.duration,"
                         "tb_tracks_history.play_url_32,"
                         "tb_tracks_history.play_url_64,"
                         "tb_tracks_history.valid,"
                         "group_concat(tb_tracks_history.time ORDER by tb_tracks_history.time DESC) "
                         "from tb_tracks_history LEFT JOIN tb_user_collect_track "
                         "on tb_tracks_history.track_id=tb_user_collect_track.track_id "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' and tb_tracks_history.uid is NULL AND "
                         "tb_tracks_history.valid=TRUE  AND "
                         "tb_tracks_history.vin='%s' group by "
                         "tb_tracks_history.track_id ORDER BY "
                         "group_concat(tb_tracks_history.time "
                         "ORDER by tb_tracks_history.time DESC) DESC;"
                         % (starttime, endtime, self._vin))
            else:
                query = ("select "
                         "tb_tracks_history.track_id, "
                         "tb_tracks_history.track_title,"
                         "tb_tracks_history.cover_url_small,"
                         "tb_tracks_history.cover_url_middle,"
                         "tb_tracks_history.cover_url_large,"
                         "tb_tracks_history.duration,"
                         "tb_tracks_history.play_url_32,"
                         "tb_tracks_history.play_url_64,"
                         "tb_tracks_history.valid, "
                         "group_concat(tb_tracks_history.time ORDER by tb_tracks_history.time DESC) "
                         "from tb_tracks_history LEFT JOIN tb_user_collect_track "
                         "on tb_tracks_history.track_id=tb_user_collect_track.track_id "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' and tb_tracks_history.uid='%s' AND "
                         "tb_tracks_history.valid=TRUE group by "
                         "tb_tracks_history.track_id order by "
                         "group_concat(tb_tracks_history.time ORDER by "
                         "tb_tracks_history.time DESC) DESC;"
                         % (starttime, endtime, self._uid))
            print(query)
            data = self._conn.session.execute(query)
            out = [{'track_id': i[0],
                    'track_title': i[1],
                    'cover_url_small': i[2],
                    'cover_url_middle': i[3],
                    'cover_url_large': i[4],
                    'duration': i[5],
                    'play_url_32': i[6],
                    'play_url_64': i[7],
                    'valid':i[8]} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, track_id):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            s = {'ids': track_id}
            trackdata = demand_api.TracksGetbatch(s).get()['tracks'][0]
            track_title = trackdata['track_title']
            announcer_id = trackdata['announcer']['id']
            nickname = trackdata['announcer']['nickname']
            category_id = trackdata['category_id']
            album_id = trackdata['subordinated_album']['id']
            album_title = trackdata['subordinated_album']['album_title']
            play_count = trackdata['play_count']
            cover_url_small = trackdata['cover_url_small']
            cover_url_middle = trackdata['cover_url_middle']
            cover_url_large = trackdata['cover_url_large']
            duration = trackdata['duration']
            play_url_32 = trackdata['play_url_32']
            play_url_64 = trackdata['play_url_64']
            data = {'uid': self._uid,
                    'vin': self._vin,
                    'time': time_array,
                    'track_id': track_id,
                    'track_title': track_title,
                    'announcer_id': announcer_id,
                    'nickname': nickname,
                    'category_id': category_id,
                    'album_id': album_id,
                    'album_title': album_title,
                    'play_count': play_count,
                    'modifiedtime': time_array,
                    'cover_url_small': cover_url_small,
                    'cover_url_middle': cover_url_middle,
                    'cover_url_large': cover_url_large,
                    'play_url_32': play_url_32,
                    'play_url_64': play_url_64,
                    'duration': duration,
                    'valid': True}
            add_item = (base.UserTracksHistoryList(**data))
            self._conn.session.add(add_item)
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def stat(self, n=50, start_time=None, end_time=None):
        starttime = start_time if start_time else datetime.datetime.now() - datetime.timedelta(720)
        endtime = end_time if end_time else datetime.datetime.now()
        try:
            if self._uid is None:
                query = ("SELECT "
                         "tb_tracks_history.track_id,"
                         "count(tb_tracks_history.track_id),"
                         "tb_tracks_history.track_title,"
                         "group_concat(time ORDER by time DESC) "
                         "from tb_tracks_history "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_tracks_history.uid is NULL "
                         "AND tb_tracks_history.vin='%s' "
                         "group by tb_tracks_history.track_id "
                         "ORDER BY count(track_id) DESC;"
                         % (starttime, endtime, self._vin))
            else:
                query = ("SELECT "
                         "tb_tracks_history.track_id,"
                         "count(tb_tracks_history.track_id),"
                         "tb_tracks_history.track_title,"
                         "group_concat(time ORDER by time DESC) "
                         "from tb_tracks_history "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_tracks_history.uid='%s' "
                         "group by tb_tracks_history.track_id "
                         "ORDER BY count(track_id) DESC;"
                         % (starttime, endtime, self._uid))

            track_data = self._conn.session.execute(query)
            if track_data:
                track_out = [{'track_id': i[0],
                              'playnum': i[1],
                              'track_title': i[2],
                              'playtime': i[3]} for i in track_data]
            else:
                track_out = None

            if self._uid is None:
                query = ("SELECT "
                         "tb_tracks_history.album_id,"
                         "count(tb_tracks_history.album_id),"
                         "group_concat(time ORDER by time DESC) "
                         "from tb_tracks_history "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_tracks_history.uid is NULL "
                         "AND tb_tracks_history.vin='%s' "
                         "group by tb_tracks_history.album_id "
                         "ORDER BY count(album_id) DESC;"
                         % (starttime, endtime, self._vin))
            else:
                query = ("SELECT "
                         "tb_tracks_history.album_id,"
                         "count(tb_tracks_history.album_id),"
                         "group_concat(time ORDER by time DESC) "
                         "from tb_tracks_history "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_tracks_history.uid='%s' "
                         "group by tb_tracks_history.album_id "
                         "ORDER BY count(album_id) DESC;"
                         % (starttime, endtime, self._uid))

            album_data = self._conn.session.execute(query)
            if album_data:
                album_out = [{'albumid': i[0],
                              'playnum': i[1],
                              'playtime': i[2]} for i in album_data]
            else:
                album_out = None

            if self._uid is None:
                query = ("SELECT "
                         "tb_tracks_history.announcer_id,"
                         "count(tb_tracks_history.announcer_id), "
                         "tb_tracks_history.nickname,"
                         "group_concat(time ORDER by time DESC) "
                         "from tb_tracks_history "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_tracks_history.uid is NULL "
                         "AND tb_tracks_history.vin='%s' "
                         "group by tb_tracks_history.announcer_id "
                         "ORDER BY count(announcer_id) DESC;"
                         % (starttime, endtime, self._vin))
            else:
                query = ("SELECT "
                         "tb_tracks_history.announcer_id,"
                         "count(tb_tracks_history.announcer_id), "
                         "tb_tracks_history.nickname,"
                         "group_concat(time ORDER by time DESC) "
                         "from tb_tracks_history "
                         "where tb_tracks_history.time "
                         "BETWEEN '%s'and'%s' "
                         "and tb_tracks_history.uid='%s' "
                         "group by tb_tracks_history.announcer_id "
                         "ORDER BY count(announcer_id) DESC;"
                         % (starttime, endtime, self._uid))

            artist_data = self._conn.session.execute(query)
            if artist_data:
                artist_out = [{'artistid': i[0],
                               'artistname': i[2],
                               'playnum': i[1],
                               'playtime': i[3]} for i in artist_data]
            else:
                artist_out = None
            out = {'track': track_out,
                   'album': album_out,
                   'artist': artist_out}
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False

    def clear(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(base.UserTracksHistoryList)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       valid=True).all()
                for i in data:
                    i.valid = False
            else:
                data = query.filter_by(uid=self._uid,
                                       valid=True).all()
                for i in data:
                    i.valid = False
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('clear failre')
            return False


class CollectTrack(Common):
    def __init__(self, vin, uid=None, Conn=Connection):
        super(CollectTrack, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            query = self._conn.session.query(base.UserCollectTrack)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).all()
            else:
                data = query.filter_by(uid=self._uid, favorite=True).all()
            out = [{'track_id': i.track_id,
                    'track_title': i.track_title,
                    'duration': i.duration,
                    'cover_url_small': i.cover_url_small,
                    'cover_url_middle': i.cover_url_middle,
                    'cover_url_large': i.cover_url_large,
                    'play_url_32': i.play_url_32,
                    'play_url_64': i.play_url_64,
                    'time': i.time.strftime("%Y-%m-%d %H:%M:%S")} for i in data]
            out.sort(key=takeTime, reverse=True)
            out = out[0:500]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False

    def add(self, timestamp, track_id):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectTrack).filter_by(uid=self._uid,
                                                                                    vin=self._vin,
                                                                                    track_id=track_id).first()
            else:
                collect = self._conn.session.query(base.UserCollectTrack).filter_by(uid=self._uid,
                                                                                    track_id=track_id).first()
            if collect is None:
                s = {'ids': track_id}
                trackdata = demand_api.TracksGetbatch(s).get()['tracks'][0]
                track_title = trackdata['track_title']
                duration = trackdata['duration']
                cover_url_small = trackdata['cover_url_small']
                cover_url_middle = trackdata['cover_url_middle']
                cover_url_large = trackdata['cover_url_large']
                play_url_32 = trackdata['play_url_32']
                play_url_64 = trackdata['play_url_64']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'track_id': track_id,
                        'duration': duration,
                        'cover_url_small': cover_url_small,
                        'cover_url_middle': cover_url_middle,
                        'cover_url_large': cover_url_large,
                        'play_url_32': play_url_32,
                        'play_url_64': play_url_64,
                        'track_title': track_title,
                        'favorite': True,
                        'time': time_array}
                add_item = base.UserCollectTrack(**data)
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, track_id):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectTrack).filter_by(uid=self._uid,
                                                                                    vin=self._vin,
                                                                                    track_id=track_id).first()
            else:
                collect = self._conn.session.query(base.UserCollectTrack).filter_by(uid=self._uid,
                                                                                    track_id=track_id).first()
            if collect is None:
                s = {'ids': track_id}
                trackdata = demand_api.TracksGetbatch(s).get()['tracks'][0]
                track_title = trackdata['track_title']
                duration = trackdata['duration']
                cover_url_small = trackdata['cover_url_small']
                cover_url_middle = trackdata['cover_url_middle']
                cover_url_large = trackdata['cover_url_large']
                play_url_32 = trackdata['play_url_32']
                play_url_64 = trackdata['play_url_64']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'track_id': track_id,
                        'duration': duration,
                        'cover_url_small': cover_url_small,
                        'cover_url_middle': cover_url_middle,
                        'cover_url_large': cover_url_large,
                        'play_url_32': play_url_32,
                        'play_url_64': play_url_64,
                        'track_title': track_title,
                        'favorite': False,
                        'time': time_array}
                add_item = (base.UserCollectTrack(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = False
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False


class CollectPlayList(Common):
    def __init__(self, vin, uid=None, conn=Connection):
        super(CollectPlayList, self).__init__(vin, uid, conn)

    def get(self):
        try:
            query = self._conn.session.query(base.UserCollectPlayList)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).all()
            else:
                data = query.filter_by(uid=self._uid, favorite=True).all()
            out = [{'playlistid': i.playlistid,
                    'playlistname': i.playlistname,
                    'imageS': i.imageSmall,
                    'imageM': i.imageMiddle,
                    'imageL': i.imageLarge} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, playlistid, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               playlistid=playlistid,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               playlistid=playlistid,
                               selflist=selflist).first()
            if collect is None:
                if selflist:
                    if self._uid is None:
                        playlist = self._conn.session.query(base.UserPlayList)\
                            .filter_by(uid=self._uid,
                                       vin=self._vin,
                                       playlistid=playlistid).first()
                    else:
                        playlist = self._conn.session.query(base.UserPlayList) \
                            .filter_by(uid=self._uid,
                                       playlistid=playlistid).first()
                    if playlist is None:
                        return 'No %s in self playlist!' %playlistid
                    else:
                        imageS = playlist.imageSmall
                        imageL = playlist.imageLagre
                        playlistname = playlist.playlistname
                else:
                    s = {'id': playlistid}
                    playlist = column_api.ColumnDetail(s).get()
                    imageS = playlist['logo_small']
                    imageL = playlist['cover_url_large']
                    playlistname = playlist['column_editor']['nickname']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'playlistid': playlistid,
                        'playlistname': playlistname,
                        'imageSmall': imageS,
                        'imageLarge': imageL,
                        'favorite': True,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectPlayList(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, playlistid, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               playlistid=playlistid,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               playlistid=playlistid,
                               selflist=selflist).first()
            if collect is None:
                if selflist:
                    if self._uid is None:
                        playlist = self._conn.session.query(base.UserPlayList)\
                            .filter_by(uid=self._uid,
                                       vin=self._vin,
                                       playlistid=playlistid).first()
                    else:
                        playlist = self._conn.session.query(base.UserPlayList) \
                            .filter_by(uid=self._uid,
                                       playlistid=playlistid).first()
                    if playlist is None:
                        return 'No %s in self playlist!' %playlistid
                    else:
                        imageS = playlist.imageSmall
                        imageM = playlist.imageMiddle
                        imageL = playlist.imageLagre
                        playlistname = playlist.playlistname
                else:
                    s = {'ids': playlistid}
                    playlist = demand_api.TracksGetbatch(s).get()[0]
                    imageS = playlist['cover_url_small']
                    imageM = playlist['cover_url_middle']
                    imageL = playlist['cover_url_large']
                    playlistname = playlist['album_title']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'playlistid': playlistid,
                        'playlistname': playlistname,
                        'imageSmall': imageS,
                        'imageMiddle': imageM,
                        'imageLarge': imageL,
                        'favorite': False,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectPlayList(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = False
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False


class UserPlaylist(Common):
    def __init__(self, vin, uid=None, Conn=Connection):
        super(UserPlaylist, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            query = self._conn.session.query(base.UserPlayList)
            if self._uid is None:
                data = query.filter_by(vin=self._vin, uid=self._uid).all()
            else:
                data = query.filter_by(uid=self._uid).all()
            out = [{'playlistid': i.playlistid,
                    'playlistname': i.playlistname,
                    'imageS': i.imageSmall,
                    'imageM': i.imageMiddle,
                    'imageL': i.imageLarge} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            return False

    def create(self,playlistname):
        try:
            data = {'playlistname': playlistname,
                    'vin': self._vin,
                    'uid': self._uid,
                    'createtime': datetime.datetime.now(),
                    'favorite': False}
            playlist = base.UserPlayList(**data)
            self._conn.session.add(playlist)
            self._conn.session.commit()
            self._conn.close()
            return {'playlistid': playlist.playlistid}
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            return False

    def add(self, timestamp, playlistid, track_id):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            playlist = self._conn.session.query(base.UserPlayList).filter_by(playlistid=playlistid).first()
            if playlist is None:
                return False
            playlistcontent = self._conn.session.query(base.UserPlayListContent) \
                .filter_by(playlistid=playlistid,
                           track_id=track_id).first()
            if playlistcontent is None:
                track = self._conn.session.query(base.Track).filter_by(track_id=track_id).first()
                if track is None:
                    s = {'ids': track_id}
                    trackdata = demand_api.TracksGetbatch(s).get()['tracks'][0]
                    track_title = trackdata['track_title']
                    announcer_id = trackdata['announcer']['id']
                    nickname = trackdata['announcer']['nickname']
                    category_id = trackdata['category_id']
                    album_id = trackdata['subordinated_album']['id']
                    album_title = trackdata['subordinated_album']['album_title']
                    play_count = trackdata['play_count']
                    comment_count = trackdata['comment_count']
                    imageS = trackdata['cover_url_small']
                    imageM = trackdata['cover_url_middle']
                    imageL = trackdata['cover_url_large']
                    duration = trackdata['duration']
                    addtrack = {'track_id': track_id,
                                'track_title': track_title,
                                'announcer_id': announcer_id,
                                'nickname': nickname,
                                'category_id': category_id,
                                'album_id': album_id,
                                'album_title': album_title,
                                'play_count': play_count,
                                'imageSmall': imageS,
                                'imageMiddle': imageM,
                                'imageLarge': imageL,
                                'comment_count': comment_count,
                                'duration': duration}
                    newtrack = base.Track(**addtrack)
                    self._conn.session.add(newtrack)
                else:
                    track_title = track.track_title
                    imageS = track.imagepathmapSmall
                    imageM = track.imagepathmapMiddle
                    imageL = track.imagepathmapLarge
                valid = True
                data = {'playlistid': playlistid,
                        'track_id': track_id,
                        'track_title': track_title,
                        'valid': valid,
                        'time': time_array}
                additem = base.UserPlayListContent(**data)
                playlist.imageSmall = imageS
                playlist.imageMiddle = imageM
                playlist.imageLagre = imageL
                self._conn.session.add(additem)
            else:
                playlistcontent.valid = True
                playlistcontent.vin = self._vin
                playlistcontent.time = time_array
            playlist.modifiedtime = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, playlistid, track_id):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            playlist = self._conn.session.query(base.UserPlayList).filter_by(playlistid=playlistid).first()
            if playlist is None:
                return False
            playlistcontent = self._conn.session.query(base.UserPlayListContent) \
                .filter_by(playlistid=playlistid, track_id=track_id).first()
            if playlistcontent is None:
                track = self._conn.session.query(base.Track).filter_by(track_id=track_id).first()
                if track is None:
                    s = {'ids': track_id}
                    trackdata = demand_api.TracksGetbatch(s).get()['tracks'][0]
                    track_title = trackdata['track_title']
                    announcer_id = trackdata['announcer']['id']
                    nickname = trackdata['announcer']['nickname']
                    category_id = trackdata['category_id']
                    album_id = trackdata['subordinated_album']['id']
                    album_title = trackdata['subordinated_album']['album_title']
                    play_count = trackdata['play_count']
                    comment_count = trackdata['comment_count']
                    imageS = trackdata['cover_url_small']
                    imageM = trackdata['cover_url_middle']
                    imageL = trackdata['cover_url_large']
                    duration = trackdata['duration']
                    addtrack = {'track_id': track_id,
                                'track_title': track_title,
                                'announcer_id': announcer_id,
                                'nickname': nickname,
                                'category_id': category_id,
                                'album_id': album_id,
                                'album_title': album_title,
                                'play_count': play_count,
                                'imageSmall': imageS,
                                'imageMiddle': imageM,
                                'imageLarge': imageL,
                                'comment_count': comment_count,
                                'duration': duration}
                    newtrack = base.Track(**addtrack)
                    self._conn.session.add(newtrack)
                else:
                    track_title = track.track_title
                valid = False
                data = {'playlistid': playlistid,
                        'track_id': track_id,
                        'track_title': track_title,
                        'valid': valid,
                        'time': time_array}
                additem = base.UserPlayListContent(**data)
                self._conn.session.add(additem)
            else:
                playlistcontent.valid = False
                playlistcontent.time = time_array
            playlist.modifiedtime = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False

    def getplaylistcontent(self, playlistid):
        try:
            query = self._conn.session.query(base.UserPlayListContent)
            data = query.filter_by(playlistid=playlistid,
                                   valid=True).order_by(base.UserPlayListContent.time.desc())
            if data:
                out = [{'track_id': i.track_id, 'track_title': i.track_title}
                       for i in data]
            else:
                out = []
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('getplaylistcontent failre')
            return False


class UserHistoryBase(object):
    def __init__(self, conn=Connection):
        self._conn = conn

    def getuid(self):
        query = ("SELECT "
                 "DISTINCT tb_tracks_history.uid "
                 "from tb_tracks_history "
                 "where tb_tracks_history.uid<>'';")
        uid = self._conn.session.execute(query)
        self._conn.close()
        return uid

    def getvin(self):
        query = ("SELECT "
                 "DISTINCT tb_tracks_history.vin "
                 "from tb_tracks_history "
                 "where ISNULL(tb_tracks_history.uid);")
        vin = self._conn.session.execute(query)
        self._conn.close()
        return vin


class CollectAlbum(Common):
    def __init__(self, vin, uid=None, conn=Connection):
        super(CollectAlbum, self).__init__(vin, uid, conn)

    def get(self):
        try:
            query = self._conn.session.query(base.UserCollectAlbum)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).all()
            else:
                data = query.filter_by(uid=self._uid, favorite=True).all()
            out = [{'album_id': i.album_id,
                    'album_title': i.album_title,
                    'cover_url_small': i.cover_url_small,
                    'cover_url_middle': i.cover_url_middle,
                    'cover_url_large': i.cover_url_large,
                    'time': json.dumps(i.time, cls=DateEncoder)} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, album_id, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectAlbum)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               album_id=album_id,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectAlbum)\
                    .filter_by(uid=self._uid,
                               album_id=album_id,
                               selflist=selflist).first()
            if collect is None:
                s = {'album_id': album_id}
                album = demand_api.AlbumsBrowse(s).get()
                cover_url_small = album['cover_url_small']
                cover_url_middle = album['cover_url_middle']
                cover_url_large = album['cover_url_large']
                album_title = album['album_title']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'album_id': album_id,
                        'album_title': album_title,
                        'cover_url_small': cover_url_small,
                        'cover_url_middle': cover_url_middle,
                        'cover_url_large': cover_url_large,
                        'favorite': True,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectAlbum(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, album_id, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectAlbum)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               album_id=album_id,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectAlbum)\
                    .filter_by(uid=self._uid,
                               album_id=album_id,
                               selflist=selflist).first()
            if collect is None:
                s = {'album_id': album_id}
                album = demand_api.AlbumsBrowse(s).get()
                cover_url_small = album['cover_url_small']
                cover_url_middle = album['cover_url_middle']
                cover_url_large = album['cover_url_large']
                album_title = album['album_title']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'album_id': album_id,
                        'album_title': album_title,
                        'cover_url_small': cover_url_small,
                        'cover_url_middle': cover_url_middle,
                        'cover_url_large': cover_url_large,
                        'favorite': False,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectAlbum(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = False
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False


class CollectRadio(Common):
    def __init__(self, vin, uid=None, conn=Connection):
        super(CollectRadio, self).__init__(vin, uid, conn)

    def get(self):
        try:
            query = self._conn.session.query(base.UserCollectRadio)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).all()
            else:
                data = query.filter_by(uid=self._uid, favorite=True).all()
            out = [{'id': i.id,
                    'radio_name': i.radio_name,
                    'cover_url_small': i.cover_url_small,
                    # 'cover_url_middle': i.cover_url_middle,
                    'cover_url_large': i.cover_url_large,
                    'time': json.dumps(i.time, cls=DateEncoder)} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, id, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectRadio)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               id=id,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectRadio)\
                    .filter_by(uid=self._uid,
                               id=id,
                               selflist=selflist).first()
            if collect is None:
                s = {'ids': id}
                radio = live_api.LiveGetradiosbyids(s).get()['radios'][0]
                cover_url_small = radio['cover_url_small']
                # cover_url_middle = radio['cover_url_middle']
                cover_url_large = radio['cover_url_large']
                radio_name = radio['radio_name']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'id': id,
                        'radio_name': radio_name,
                        'cover_url_small': cover_url_small,
                        # 'cover_url_middle': cover_url_middle,
                        'cover_url_large': cover_url_large,
                        'favorite': True,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectRadio(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, id, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectRadio)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               id=id,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectRadio)\
                    .filter_by(uid=self._uid,
                               id=id,
                               selflist=selflist).first()
            if collect is None:
                s = {'ids': id}
                radio = live_api.LiveGetradiosbyids(s).get()
                cover_url_small = radio['cover_url_small']
                # cover_url_middle = radio['cover_url_middle']
                cover_url_large = radio['cover_url_large']
                radio_name = radio['radio_name']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'id': id,
                        'radio_name': radio_name,
                        'cover_url_small': cover_url_small,
                        # 'cover_url_middle': cover_url_middle,
                        'cover_url_large': cover_url_large,
                        'favorite': False,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectRadio(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = False
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False


class CollectAnnouncer(Common):
    def __init__(self, vin, uid=None, conn=Connection):
        super(CollectAnnouncer, self).__init__(vin, uid, conn)

    def get(self):
        try:
            query = self._conn.session.query(base.UserCollectAnnouncer)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).all()
            else:
                data = query.filter_by(uid=self._uid, favorite=True).all()
            out = [{'id': i.id,
                    'nickname': i.nickname,
                    'avatar_url': i.avatar_url} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, id, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectAnnouncer)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               id=id,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectAnnouncer)\
                    .filter_by(uid=self._uid,
                               id=id,
                               selflist=selflist).first()
            if collect is None:
                s = {'ids': id}
                announcer = ann.AnnouncersGetbatch(s).get()[0]
                avatar_url = announcer['avatar_url']
                nickname = announcer['nickname']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'id': id,
                        'nickname': nickname,
                        'avatar_url': avatar_url,
                        'favorite': True,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectAnnouncer(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, id, selflist=False):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectAnnouncer)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               id=id,
                               selflist=selflist).first()
            else:
                collect = self._conn.session.query(base.UserCollectAnnouncer)\
                    .filter_by(uid=self._uid,
                               id=id,
                               selflist=selflist).first()
            if collect is None:
                s = {'ids': id}
                announcer = ann.AnnouncersGetbatch(s).get()[0]
                avatar_url = announcer['avatar_url']
                nickname = announcer['nickname']
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'id': id,
                        'nickname': nickname,
                        'avatar_url': avatar_url,
                        'favorite': False,
                        'time': time_array,
                        'selflist': selflist}
                add_item = (base.UserCollectAnnouncer(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = False
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('cancel failre')
            return False


class UserTrackRecord(Common):
    def __init__(self, vin, uid=None, conn=Connection):
        super(UserTrackRecord, self).__init__(vin, uid, conn)

    def get_track(self, album_id):
        try:
            query = self._conn.session.query(base.UserTrackRecord)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       album_id=album_id).all()
            else:
                data = query.filter_by(uid=self._uid,
                                       album_id=album_id).all()
            out = [{'track_id': i.track_id} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def get_position(self, track_id):
        try:
            query = self._conn.session.query(base.UserTrackRecord)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       track_id=track_id).all()
            else:
                data = query.filter_by(uid=self._uid,
                                       track_id=track_id).all()
            out = [{'duration': i.position,
                    'time': i.time.strftime("%Y-%m-%d %H:%M:%S")} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False


    def get(self, album_id):
        try:
            query = self._conn.session.query(base.UserTrackRecord)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       album_id=album_id).all()
            else:
                data = query.filter_by(uid=self._uid,
                                       album_id=album_id).all()
            out = [{'duration': i.position, 'track_id': i.track_id,
                    'time': i.time.strftime("%Y-%m-%d %H:%M:%S")} for i in data]
            self._conn.close()
            return out
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, album_id, track_id, position):
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            data = {'uid': self._uid,
                    'vin': self._vin,
                    'album_id': album_id,
                    'track_id': track_id,
                    'position': position,
                    'time': time_array}
            add_item = (base.UserTrackRecord(**data))
            self._conn.session.add(add_item)
            self._conn.commit()
            self._conn.close()
            return True
        except:
            self._conn.session.rollback()
            self._conn.close()
            traceback.print_exc()
            print('add failre')
            return False
