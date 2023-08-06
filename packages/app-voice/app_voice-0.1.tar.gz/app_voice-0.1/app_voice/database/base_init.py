#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-11 上午9:16
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : base_init
# @Contact : guangze.yu@foxmail.com
"""
from sqlalchemy import Column, String, Integer, create_engine, TEXT, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import database.config as cfg
import random
import datetime
import API.ranks as ranks_api
import logger

log = logger.get_logger(__name__)

Base = declarative_base()


class Connect():
    '''
    database connect:
    '''
    def __init__(self, config=cfg.sqlconfig):
        self.engine = create_engine(config,encoding='utf-8')
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def data_base_init(self):
        # Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def data_base_add(self):
        Base.metadata.create_all(self.engine)


class UserSearchKeyWordHistory(Base):
    '''
    用户搜索历史数据表
    '''
    __tablename__ = 'tb_searchword_history'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    keyword = Column(String(255), nullable=False)
    showinlist = Column(Boolean, nullable=False)


class UserTracksHistoryList(Base):
    '''
    单曲历史列表
    '''
    __tablename__ = 'tb_tracks_history'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    track_id = Column(Integer(), nullable=False)
    track_title = Column(String(255), nullable=True)
    announcer_id = Column(Integer(), nullable=True)
    nickname = Column(String(255), nullable=True)
    category_id = Column(Integer(), nullable=True)
    album_id = Column(Integer(), nullable=True)
    album_title = Column(String(255), nullable=True)
    play_count = Column(Integer(), nullable=True)
    modifiedtime = Column(DateTime, nullable=False)
    valid = Column(Boolean, nullable=False)
    cover_url_small = Column(String(1024), nullable=True)
    cover_url_middle = Column(String(1024), nullable=True)
    cover_url_large = Column(String(1024), nullable=True)
    duration = Column(String(255), nullable=False)
    play_url_32 = Column(String(1024), nullable=True)
    play_url_64 = Column(String(1024), nullable=True)
    duration = Column(Integer(), nullable=True)


class Track(Base):
    '''
    单曲信息
    '''
    __tablename__ = 'tb_track'
    track_id = Column(Integer(), primary_key=True, nullable=False)
    track_title = Column(String(255), nullable=True)

    announcer_id = Column(Integer(), nullable=True)
    nickname = Column(String(255), nullable=True)
    category_id = Column(Integer(), nullable=True)

    album_id = Column(Integer(), nullable=True)
    album_title = Column(String(255), nullable=True)

    play_count = Column(Integer(), nullable=True)
    comment_count = Column(Integer(), nullable=True)

    imageSmall = Column(String(1024), nullable=True)
    imageLarge = Column(String(1024), nullable=True)
    imageMiddle = Column(String(1024), nullable=True)

    duration = Column(Integer(), nullable=True)


class UserCollectTrack(Base):
    '''
    收藏单曲
    '''
    __tablename__ = 'tb_user_collect_track'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    track_id = Column(Integer(), nullable=False)
    track_title = Column(String(255), nullable=True)
    cover_url_small = Column(String(1024), nullable=True)
    cover_url_middle = Column(String(1024), nullable=True)
    cover_url_large = Column(String(1024), nullable=True)
    duration = Column(String(255), nullable=False)
    play_url_32 = Column(String(1024), nullable=True)
    play_url_64 = Column(String(1024), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)


class UserCollectPlayList(Base):
    '''
    收藏歌单
    '''
    __tablename__ = 'tb_user_collect_playlist'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    playlistid = Column(Integer(), nullable=False)
    playlistname = Column(String(255), nullable=True)
    imageSmall = Column(String(1024), nullable=True)
    imageMiddle = Column(String(1024), nullable=True)
    imageLarge = Column(String(1024), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    selflist = Column(Boolean, nullable=False)  ##是否为自建歌单


class UserPlayList(Base):
    '''
    用户歌单
    '''
    __tablename__ = 'tb_user_playlist'
    playlistid = Column(Integer(), primary_key=True, index=True)
    playlistname = Column(String(255), nullable=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    favorite = Column(Boolean, nullable=False)
    imageSmall = Column(String(1024), nullable=True)
    imageMiddle = Column(String(1024), nullable=True)
    imageLarge = Column(String(1024), nullable=True)
    createtime = Column(DateTime, nullable=False)
    modifiedtime = Column(DateTime, nullable=False)


class UserPlayListContent(Base):
    '''
    用户歌单内容
    '''
    __tablename__ = 'tb_user_playlist_content'
    index = Column(Integer(), primary_key=True, index=True)
    playlistid = Column(Integer(), nullable=False)
    track_id = Column(Integer(), nullable=False)
    track_title = Column(String(255), nullable=True)
    valid = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)


class UserCollectAlbum(Base):
    """
    collect album
    """
    __tablename__= 'tb_user_collect_album'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    album_id = Column(Integer(), nullable=False)
    album_title = Column(String(255), nullable=True)
    cover_url_small = Column(String(1024), nullable=True)
    cover_url_middle = Column(String(1024), nullable=True)
    cover_url_large = Column(String(1024), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    selflist = Column(Boolean, nullable=False)


class UserCollectRadio(Base):
    """
    collect radio
    """
    __tablename__= 'tb_user_collect_radio'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    id = Column(Integer(), nullable=False)
    radio_name = Column(String(255), nullable=True)
    cover_url_small = Column(String(1024), nullable=True)
    cover_url_large = Column(String(1024), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    selflist = Column(Boolean, nullable=False)


class UserCollectAnnouncer(Base):
    """
    collect announcer
    """
    __tablename__= 'tb_user_collect_announcer'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    id = Column(Integer(), nullable=False)
    nickname = Column(String(255), nullable=True)
    avatar_url = Column(String(1024), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    selflist = Column(Boolean, nullable=False)


class UserTrackRecord(Base):
    """
    record last play position
    """
    __tablename__ = 'tb_track_record'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    album_id = Column(Integer(), nullable=True)
    track_id = Column(Integer(), nullable=True)
    position = Column(Integer(), nullable=False)
    time = Column(DateTime, nullable=False)


def gen_keywords(Conn):
    # query = Conn.session.query(UserSearchKeyWordHistory)
    init = 1483200000.0
    uid = [888888, None, 666666]
    vin_code = ['LSJA01234567890112', 'LSJA01234567890118', 'LSJA02234567890112']
    keywords = ['流金岁月', '经典老歌', '影视金曲', '内地流行', '港台流行', '日韩流行', '欧美金曲', '摇滚', '少儿歌曲', '热门对唱', '校园民谣', '网络歌曲', '轻音乐',
                '天籁之声', '劲爆']
    for i in range(20):
        timestamp = init + 86400 * random.randint(0, 300) + random.randint(0,23)*60*60 + random.randint(0,60)
        timeArray = datetime.datetime.fromtimestamp(timestamp)
        user_index = random.randint(0,2)
        keywords_index = random.randint(0,len(keywords)-1)

        data = {'uid':uid[user_index], 'vin':vin_code[user_index], 'time':timeArray, 'keyword':keywords[keywords_index],
                'showinlist':True}
        add_item = UserSearchKeyWordHistory(**data)
        Conn.session.add(add_item)
    Conn.commit()
    Conn.close()


def gen_tracks(Conn):
    tracks = []
    for i in range(18):
        s = {'rank_key': '1_57_ranking:track:scoreByTime:1:0',
             'page': '%s'%(i+1),
             'count': '100'}
        b = ranks_api.RanksTracks(s).get()['tracks']
        tracks += b
    for i in tracks:
        print(i)
        track_id = i['id']
        query = Conn.session.query(Track).filter_by(track_id=track_id).all()
        print(query)
        if query == []:
            track_title = i['track_title']
            announcer_id = i['announcer']['id']
            nickname = i['announcer']['nickname']
            album_id = i['subordinated_album']['id']
            album_title = i['subordinated_album']['album_title']
            play_count = i['play_count']
            comment_count = i['comment_count']
            imageSmall = i['cover_url_small']
            imageMiddle = i['cover_url_middle']
            imageLarge = i['cover_url_large']
            duration = i['duration']
            data = {'track_id': track_id,
                    'track_title': track_title,
                    'announcer_id': announcer_id,
                    'nickname': nickname,
                    'album_id': album_id,
                    'album_title': album_title,
                    'play_count': play_count,
                    'comment_count': comment_count,
                    'imageSmall': imageSmall,
                    'imageMiddle': imageMiddle,
                    'imageLarge': imageLarge,
                    'duration': duration}
            print(data)
            add_item = Track(**data)
            Conn.session.add(add_item)
    Conn.commit()
    Conn.close()


def gen_trackhistory(Conn):
    query = Conn.session.query(Track)
    u = query.all()
    l = len(u)
    init = 1483200000.0
    uid = [123456, None, 666666]
    vin_code = ['LSJA01234567890112', 'LSJA01234567890118', 'LSJA02234567890112']
    for i in range(900):
        timestamp = init + 86400 * random.randint(0, 300) + random.randint(0, 23) * 60 * 60 + random.randint(0, 60)
        timeArray = datetime.datetime.fromtimestamp(timestamp)
        user_index = random.randint(0, 2)
        track_index = random.randint(0, l-1)
        track = u[track_index]
        data = {'uid': uid[user_index],
                'vin': vin_code[user_index],
                'time': timeArray,
                'track_id': track.track_id,
                'track_title': track.track_title,
                'announcer_id': track.announcer_id,
                'nickname': track.nickname,
                'album_id': track.album_id,
                'album_title': track.album_title,
                'play_count': track.play_count,
                'modifiedtime': timeArray,
                'valid': True}
        add_item = UserTracksHistoryList(**data)
        Conn.session.add(add_item)
    Conn.commit()
    Conn.close()
