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

class PlayhistoryGetbyuid(Common):
    '''根据用户ID获取用户播放云历史记录'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid.
        uid:当前用户ID
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        super(PlayhistoryGetbyuid, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/play_history/get_by_uid'

class PlayhistoryUpload(Common):
    '''用户上传播放云历史记录'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid,break_second;
        可选:content_type,album_id,track_id,radio_id,schedule_id,play_begin_at,play_end_at.
        uid:当前用户ID
        break_second:相对于音频开始位置的播放跳出位置,单位为秒.比如当前音频总时长60s,本次播放到音频第25s处就退出或者切到下一首,
                     那么break_second就是25
        content_type:-点播(不传时候的默认值),2-广播
        album_id:content_type=1时候必填,表示专辑ID
        track_id:content_type=1时候必填,为声音ID,表示具体播放专辑里哪条声音
        radio_id:content_type=2时候必填,表示广播电台ID
        schedule_id:content_type=2时候必填,表示收听的广播节目时间表ID
        play_begin_at:开始播放时刻,Unix毫秒数时间戳
        play_end_at:结束播放时刻,Unix毫秒数时间戳
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        assert 'break_second' in param_dict.keys(), 'There is no break_second in the given params!'
        super(PlayhistoryUpload, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/play_history/upload'

class PlayhistoryBatchupload(Common):
    '''用户批量上传播放云历史记录'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid,play_history_records.
        uid:当前用户ID
        play_history_records:需要上传的播放数据列表,每条播放数据包含下列字段:
            content_type:1-点播,2-广播
            album_id:content_type=1时候必填,播放的专辑ID
            track_id:content_type=1时候必填,声音ID,表示具体播放专辑里哪条声音
            radio_id:content_type=2时候必填,表示广播电台ID
            schedule_id:content_type=2时候必填,表示收听的广播节目时间表ID
            break_second: 相对于音频开始位置的播放跳出位置,单位为秒.比如当前音频总时长60s,本次播放到音频第25s处就退出
                          或者切到下一首,那么break_second就是25
            play_begin_at:开始播放时刻,Unix毫秒数时间戳
            play_end_at:结束播放时刻,Unix毫秒数时间戳
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        assert 'play_history_records' in param_dict.keys(), 'There is no play_history_records in the given params!'
        super(PlayhistoryBatchupload, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/play_history/batch_upload'

class PlayhistoryBatchdelete(Common):
    '''用户批量删除播放云历史记录'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid,play_history_records.
        uid:当前用户ID
        play_history_records:需要上传的播放数据列表,每条播放数据包含下列字段:
            content_type:1-点播,2-广播
            album_id:content_type=1时不为空,表示专辑ID
            track_id:content_type=1时不为空,表示声音ID
            radio_id:content_type=2时不为空,表示电台ID
            schedule_id:content_type=2时不为空,表示电台播放节目时间表ID
            delete_at:删除发生的时间点
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        assert 'play_history_records' in param_dict.keys(), 'There is no play_history_records in the given params!'
        super(PlayhistoryBatchdelete, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/play_history/batch_delete'



# s = {'uid':'3284576'}
# t = PlayhistoryGetbyuid(s).get()
# print(t)
# #'error_desc': 'access_token is invalid or expired'

# s = {'uid':'2134325','break_second':'10'}
# t = PlayhistoryUpload(s).get()
# print(t)
# #'error_desc': 'access_token is invalid or expired'

# s = {'uid':'3284576'}
# t = PlayhistoryBatchupload(s).get()
# print(t)
##There is no play_history_records in the given params!

# s = {'uid':'3284576'}
# t = PlayhistoryBatchdelete(s).get()
# print(t)
# #There is no play_history_records in the given params!

