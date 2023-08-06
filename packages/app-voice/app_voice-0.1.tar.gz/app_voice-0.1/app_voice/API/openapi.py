#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2017/10/20 10:19
# @Author  : guangze.yu/LiShuo
# @Site    : shanghai
# @File    : ximalayaAPI.py
# @Contact : guangze.yu@foxmail.com
"""

import API.common as common

Common = common.Common

class OpenapicollectorappLivesinglerecord(Common):
    '''上传单条直播播放数据'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:radio_id,duration,played_secs; 可选:program_schedule_id,program_id,started_at,uid.
        radio_id:电台ID
        duration:播放时长,单位秒.即播放一个音频过程中,真正处于播放中状态的总时间.
        played_secs:播放第几秒或最后播放到的位置,是相对于这个音频开始位置的一个值.
                    如果没有拖动播放条、快进、快退、暂停、单曲循环等操作,played_secs的值一般和duration一致.
        program_schedule_id:节目排期ID
        program_id:节目ID
        started_at:播放开始时刻,Unix毫秒数时间戳
        uid:喜马拉雅用户ID
        '''
        
        assert 'radio_id' in param_dict.keys(), 'There is no radio_id in the given params!'
        assert 'duration' in param_dict.keys(), 'There is no duration in the given params!'
        assert 'played_secs' in param_dict.keys(), 'There is no played_secs in the given params!'
        super(OpenapicollectorappLivesinglerecord, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/live_single_record'

class OpenapicollectorappLivebatchrecords(Common):
    '''批量上传直播播放数据,每次批量小于等于200条'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:live_records; 可选:uid.
        live_records:直播播放数据列表,每条播放数据包含下列字段
            radio_id:电台ID
            program_schedule_id:节目排期ID
            program_id:节目ID
            duration:播放时长,单位秒.即播放一个音频过程中,真正处于播放中状态的总时间.
            played_secs:播放第几秒或最后播放到的位置,是相对于这个音频开始位置的一个值.
                        如果没有拖动播放条、快进、快退、暂停、单曲循环等操作,played_secs的值一般和duration一致.
            started_at:播放开始时刻,Unix毫秒数时间戳
        uid:喜马拉雅用户ID
        '''
        
        assert 'live_records' in param_dict.keys(), 'There is no live_records in the given params!'
        super(OpenapicollectorappLivebatchrecords, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/live_batch_records'

class OpenapicollectorappTracksinglerecord(Common):
    '''上传单条声音播放数据'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:track_id,duration,played_secs,play_type; 可选:started_at,uid.
        track_id:声音ID
        duration:播放时长,单位秒.即播放一个音频过程中,真正处于播放中状态的总时间.
        played_secs:播放第几秒或最后播放到的位置,是相对于这个音频开始位置的一个值.
                    如果没有拖动播放条、快进、快退、暂停、单曲循环等操作,played_secs的值一般和duration一致.
        play_type:0-联网播放,1-断网播放
        started_at:播放开始时刻,Unix毫秒数时间戳
        uid:喜马拉雅用户ID
        '''
        
        assert 'track_id' in param_dict.keys(), 'There is no track_id in the given params!'
        assert 'duration' in param_dict.keys(), 'There is no duration in the given params!'
        assert 'played_secs' in param_dict.keys(), 'There is no played_secs in the given params!'
        assert 'play_type' in param_dict.keys(), 'There is no play_type in the given params!'
        super(OpenapicollectorappTracksinglerecord, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/track_single_record'

class OpenapicollectorappTrackbatchrecords(Common):
    '''批量上传声音播放数据,每次批量小于等于200条'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:track_records; 可选:uid.
        track_records:直播播放数据列表,每条播放数据包含下列字段
            track_id:声音ID
            duration:播放时长,单位秒.即播放一个音频过程中,真正处于播放中状态的总时间.
            played_secs:播放第几秒或最后播放到的位置,是相对于这个音频开始位置的一个值.
                        如果没有拖动播放条、快进、快退、暂停、单曲循环等操作,played_secs的值一般和duration一致.
            started_at:播放开始时刻,Unix毫秒数时间戳
            play_type:0-联网播放,1-断网播放
        uid:喜马拉雅用户ID
        '''
        
        assert 'track_records' in param_dict.keys(), 'There is no track_records in the given params!'
        super(OpenapicollectorappTrackbatchrecords, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/track_batch_records'

class OpenapicollectorappUpdatealbumchannelplaycount(Common):
    '''更新专辑的渠道播放数'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:album_id.
        album_id:专辑ID
        '''
        
        assert 'album_id' in param_dict.keys(), 'There is no album_id in the given params!'
        super(OpenapicollectorappUpdatealbumchannelplaycount, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/update_album_channel_playcount'

class OpenapicollectorappUpdatealbumcolumnchannelplaycount(Common):
    '''更新专辑听单的渠道播放数'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:album_column_id.
        album_column_id:专辑听单的ID
        '''
        
        assert 'album_column_id' in param_dict.keys(), 'There is no album_column_id in the given params!'
        super(OpenapicollectorappUpdatealbumcolumnchannelplaycount, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/update_album_cloumn_channel_playcount'

class OpenapicollectorappUpdatetrackcolumnchannelplaycount(Common):
    '''更新声音听单的渠道播放数'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:track_column_id.
        track_column_id:专辑听单的ID
        '''
        
        assert 'track_column_id' in param_dict.keys(), 'There is no track_column_id in the given params!'
        super(OpenapicollectorappUpdatetrackcolumnchannelplaycount, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/openapi-collector-app/update_track_cloumn_channel_playcount'
