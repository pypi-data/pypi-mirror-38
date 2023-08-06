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

class SubscribeGetalbumsbyuid(Common):
    '''获取喜马拉雅用户的动态更新的订阅专辑列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid,updated_at; 可选:offset.
        uid:当前用户ID
        updated_at:Unix毫秒时间戳,表示获取updated_at更新时间点之前更新的offset条订阅专辑;
                  (为0表示从当前时间点最新更新的第一条订阅专辑开始获取)
        offset:拉取updated_at时间点之前更新的订阅专辑数目,默认20,最多不超过200
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        assert 'updated_at' in param_dict.keys(), 'There is no updated_at in the given params!'
        super(SubscribeGetalbumsbyuid, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/subscribe/get_albums_by_uid'

class SubscribeAddordelete(Common):
    '''用户新增或取消已订阅专辑'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid,operation_type,album_id.
        uid:当前用户ID
        operation_type:操作类型,现支持删除(0),新增(1)
        album_id:需要更新的订阅专辑ID
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        assert 'operation_type' in param_dict.keys(), 'There is no operation_type in the given params!'
        assert 'album_id' in param_dict.keys(), 'There is no album_id in the given params!'
        super(SubscribeAddordelete, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/subscribe/add_or_delete'

class SubscribeBatchadd(Common):
    '''用户批量新增已订阅专辑'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid,ids.
        uid:当前用户ID
        ids:需要更新的订阅专辑ID列表,用英文逗号分隔,例如1001,1002,1003
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        assert 'ids' in param_dict.keys(), 'There is no ids in the given params!'
        super(SubscribeBatchadd, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/subscribe/batch_add'
