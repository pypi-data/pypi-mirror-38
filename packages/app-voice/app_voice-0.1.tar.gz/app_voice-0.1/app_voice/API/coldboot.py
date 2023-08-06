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

class ColdbootGenres(Common):
    '''获取冷启动一级分类'''
    def __init__(self, param_dict):
        '''
        参数:公共参数.
        '''
        
        super(ColdbootGenres, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/coldboot/genres'

class ColdbootSubgenres(Common):
    '''获取冷启动二级分类'''
    def __init__(self, param_dict):
        '''
        参数:公共参数.
        '''
        
        super(ColdbootSubgenres, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/coldboot/sub_genres'

class ColdbootTags(Common):
    '''根据冷启动一级分类和冷启动二级分类获取相应类别下的冷启动标签列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:coldboot_genre,coldboot_sub_genre.
        coldboot_genre:冷启动分类
        coldboot_sub_genre:冷启动二级分类
        '''
        
        assert 'coldboot_genre' in param_dict.keys(), 'There is no coldboot_genre in the given params!'
        assert 'coldboot_sub_genre' in param_dict.keys(), 'There is no coldboot_sub_genre in the given params!'
        super(ColdbootTags, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/coldboot/tags'

class ColdbootSubmittags(Common):
    '''提交用户感兴趣的冷启动标签'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:coldboot_genre,coldboot_sub_genre,device_type,device_id,coldboot_tags.
        coldboot_genre:冷启动分类
        coldboot_sub_genre:冷启动二级分类
        device_type:1-ios,2-android,3-pc
        device_id:设备唯一标识,如果公共参数里已经有device_id 参数则不需要再传
        coldboot_tags:用户勾选的感兴趣的冷启动标签列表
        '''
        
        assert 'coldboot_genre' in param_dict.keys(), 'There is no coldboot_genre in the given params!'
        assert 'coldboot_sub_genre' in param_dict.keys(), 'There is no coldboot_sub_genre in the given params!'
        assert 'device_type' in param_dict.keys(), 'There is no device_type in the given params!'
        assert 'device_id' in param_dict.keys(), 'There is no device_id in the given params!'
        assert 'coldboot_tags' in param_dict.keys(), 'There is no coldboot_tags in the given params!'
        super(ColdbootSubmittags, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/coldboot/submit_tags'

class ColdbootDetail(Common):
    '''获取用户提交的冷启动标签详情'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:device_type,device_id.
        device_type:1-ios,2-android,3-pc
        device_id:设备唯一标识,如果公共参数里已经有device_id 参数则不需要再传
        '''
        
        assert 'device_type' in param_dict.keys(), 'There is no device_type in the given params!'
        assert 'device_id' in param_dict.keys(), 'There is no device_id in the given params!'
        super(ColdbootDetail, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/coldboot/detail'