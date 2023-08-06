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

class AnnouncersCategories(Common):
    '''获取喜马拉雅主播分类'''
    def __init__(self, param_dict):
        '''
        参数:公共参数.
        '''
        
        super(AnnouncersCategories, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/announcers/categories'

class AnnouncersList(Common):
    '''获取某个分类下的主播列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:vcategory_id,calc_dimension; 可选:page,count.
        vcategory_id:主播分类ID
        calc_dimension:返回的主播列表排序规则,取值和含义如下:1-最火 ,2-最新,3-粉丝最多
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'vcategory_id' in param_dict.keys(), 'There is no vcategory_id in the given params!'
        assert 'calc_dimension' in param_dict.keys(), 'There is no calc_dimension in the given params!'
        super(AnnouncersList, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/announcers/list'

class AnnouncersGetbatch(Common):
    '''根据一批主播ID批量获取主播信息'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids.
        ids:主播用户ID列表
        '''
        
        assert 'ids' in param_dict.keys(), 'There is no ids in the given params!'
        super(AnnouncersGetbatch, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/announcers/get_batch'

class AnnouncersAlbums(Common):
    '''获取某个主播的专辑列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids; 可选:page,count.
        aid:主播用户ID
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'aid' in param_dict.keys(), 'There is no aid in the given params!'
        super(AnnouncersAlbums, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/announcers/albums'

class AnnouncersTracks(Common):
    '''获取某个主播的声音列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids; 可选:page,count.
        aid:主播用户ID
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'aid' in param_dict.keys(), 'There is no aid in the given params!'
        super(AnnouncersTracks, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/announcers/tracks'