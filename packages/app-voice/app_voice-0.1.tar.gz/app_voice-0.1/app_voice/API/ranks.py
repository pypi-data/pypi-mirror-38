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

class RanksIndexlist(Common):
    '''根据榜单类型获取榜单首页的榜单列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:rank_type.
        rank_type:榜单类型,1-节目榜单
        '''
        
        assert 'rank_type' in param_dict.keys(), 'There is no rank_type in the given params!'
        super(RanksIndexlist, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/ranks/index_list'

class RanksAlbums(Common):
    '''根据rank_key获取某个榜单下的专辑列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:rank_key; 可选:page,count.
        rank_key:用于获取具体榜单内容的key,可以先通过/rank/index_list获得
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'rank_key' in param_dict.keys(), 'There is no rank_key in the given params!'
        super(RanksAlbums, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/ranks/albums'

class RanksTracks(Common):
    '''根据rank_key获取某个榜单下的声音列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:rank_key; 可选:page,count.
        rank_key:用于获取具体榜单内容的key,可以先通过/rank/index_list获得
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'rank_key' in param_dict.keys(), 'There is no rank_key in the given params!'
        super(RanksTracks, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/ranks/tracks'

class RanksRadios(Common):
    '''根据rank_key获取某个榜单下的声音列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:radio_count.
        radio_count:需要获取排行榜中的电台数目
        '''
        
        assert 'radio_count' in param_dict.keys(), 'There is no radio_count in the given params!'
        super(RanksRadios, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/ranks/radios'

#
# s = {'rank_type': 1}
# res = RanksIndexlist(s).get()
# print(res)
