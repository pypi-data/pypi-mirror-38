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

class AlbumsRelativealbum(Common):
    '''获取某个专辑的相关推荐专辑'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:albumId.
        albumId:要获得相关推荐的专辑id
        '''
        
        assert 'albumId' in param_dict.keys(), 'There is no albumId in the given params!'
        super(AlbumsRelativealbum, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/relative_album'

class TracksRelativealbum(Common):
    '''获取某个声音的相关推荐专辑'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:trackId.
        trackId:要获得相关推荐的声音id
        '''
        
        assert 'trackId' in param_dict.keys(), 'There is no trackId in the given params!'
        super(TracksRelativealbum, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/tracks/relative_album'

class AlbumsRecommenddownload(Common):
    '''获取下载听模块的推荐下载专辑'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:calc_dimension; 可选:page,count.
        calc_dimension:计算维度,现支持经典(0),最火(1),最新(2),播放最多(3)
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'calc_dimension' in param_dict.keys(), 'There is no calc_dimension in the given params!'
        super(AlbumsRecommenddownload, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/recommend_download'

class AlbumsGuesslike(Common):
    '''猜你喜欢的专辑.和在喜马拉雅主app的"猜你喜欢"栏点"更多"链接后返回的数据一样'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:device_type,device_id; 可选:like_count.
        device_type:1-IOS系统,2-Android系统,3-Web,4-Linux系统,5-ecos系统,6-qnix系统
        device_id:设备唯一标识,如果公共擦拭农户里已经有device_id,参数则不需要再传
        like_count:返回几条,不填则默认为3,取值区间为[1, 50]
        '''
        
        assert 'device_type' in param_dict.keys(), 'There is no device_type in the given params!'
        assert 'device_id' in param_dict.keys(), 'There is no device_id in the given params!'
        super(AlbumsGuesslike, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/guess_like'

class AlbumsDiscoveryrecommendalbums(Common):
    '''获取运营人员在发现页配置的分类维度专辑推荐模块的列表样'''
    def __init__(self, param_dict):
        '''
        参数:公共参数; 可选:display_count.
        display_count:每个分类维度专辑推荐模块包含的专辑数,不填则默认为3,取值区间为[1, 20]
        '''
        
        super(AlbumsDiscoveryrecommendalbums, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/discovery_recommend_albums'

class AlbumsCategoryrecommendalbums(Common):
    '''获取运营人员在发现页配置的分类维度专辑推荐模块的列表样'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:category_id; 可选:display_count.
        category_id:分类ID,指定分类
        display_count:每个分类维度专辑推荐模块包含的专辑数,不填则默认为3,取值区间为[1, 20]
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        super(AlbumsCategoryrecommendalbums, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/category_recommend_albums'


# s = {'device_type': '1', 'device_id': 'E4B3185B0932'}
# t = AlbumsGuesslike(s).get()
# print(t)
#'error_desc': 'access_token is invalid or expired'

# s = {'display_count':'3'}
# t = AlbumsDiscoveryrecommendalbums(s).get()
# print(t)

# s = {'category_id':'5621'}
# t = AlbumsCategoryrecommendalbums(s).get()
# print(t)
