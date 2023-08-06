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

class BannersRankbanners(Common):
    '''获取榜单的焦点图列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,可选:channel,app_version,image_scale.
        channel:app的渠道号(对应渠道焦点图配置),默认值为"and-f5"
        app_version:app版本号,默认值为"4.3.2.2"
        image_scale:控制焦点图图片大小参数,scale=2为iphone适配类型,scale=3为iphone6适配机型,对于Android一般设为2,默认为2.
        '''
        
        super(BannersRankbanners, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/banners/rank_banners'

class BannersDiscoverybanners(Common):
    '''获取发现页推荐的焦点图列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,可选:channel,app_version,image_scale.
        channel:app的渠道号(对应渠道焦点图配置),默认值为"and-f5"
        app_version:app版本号,默认值为"4.3.2.2"
        image_scale:控制焦点图图片大小参数,scale=2为iphone适配类型,scale=3为iphone6适配机型,对于Android一般设为2,默认为2.
        '''
        
        super(BannersDiscoverybanners, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/banners/discovery_banners'

class BannersCategorybanners(Common):
    '''获取分类推荐的焦点图列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:category_id,content_type; 可选:channel,app_version,image_scale.
        category_id:分类ID
        content_type:内容类型:暂时仅专辑(album)
        channel:app的渠道号(对应渠道焦点图配置),默认值为"and-f5"
        app_version:app版本号,默认值为"4.3.2.2"
        image_scale:控制焦点图图片大小参数,scale=2为iphone适配类型,scale=3为iphone6适配机型,对于Android一般设为2,默认为2.
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        assert 'content_type' in param_dict.keys(), 'There is no content_type in the given params!'
        super(BannersCategorybanners, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/banners/category_banners'