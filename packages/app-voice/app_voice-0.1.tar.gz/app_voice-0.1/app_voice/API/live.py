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

class LiveProvinces(Common):
    '''获取直播省市列表'''
    def __init__(self, param_dict):
        '''
        参数:公共参数.
        '''
        
        super(LiveProvinces, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/provinces'

class LiveRadios(Common):
    '''获取直播省市列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:radio_type;可选:province_code,page,count.
        radio_type:分类id,电台类型:1-国家台,2-省市台,3-网络台
        province_code:省份代码,radio_type为2时不能为空
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'radio_type' in param_dict.keys(), 'There is no radio_type in the given params!'
        super(LiveRadios, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/radios'

class LiveSchedules(Common):
    '''获取某个直播电台某一天的节目排期的列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:radio_id;可选:weekday.
        radio_id:直播电台id
        weekday:表示星期几,不填则取今天的星期.0-星期天,1-星期一,2-星期二,3-星期三,4-星期四,5-星期五,6-星期六
        '''
        
        assert 'radio_id' in param_dict.keys(), 'There is no radio_id in the given params!'
        super(LiveSchedules, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/schedules'

class LiveGetplayingprogram(Common):
    '''获取某个电台正在直播的节目'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:radio_id.
        radio_id:直播电台id
        '''
        
        assert 'radio_id' in param_dict.keys(), 'There is no radio_id in the given params!'
        super(LiveGetplayingprogram, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/get_playing_program'

class LiveCities(Common):
    '''获取某省份城市列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:province_code.
        province_code:省份code (国家行政规划的省代码)
        '''
        
        assert 'province_code' in param_dict.keys(), 'There is no province_code in the given params!'
        super(LiveCities, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/cities'

class LiveGetradiosbycity(Common):
    '''获取某省个城市下的电台列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:city_code; 可选:page,count.
        city_code:城市code(国家行政规划的城市代码)
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'city_code' in param_dict.keys(), 'There is no city_code in the given params!'
        super(LiveGetradiosbycity, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/get_radios_by_city'

class LiveGetradiosbyids(Common):
    '''根据电台ID,批量获取电台列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids.
        ids:电台ID列表,传参时用英文逗号分隔
        '''
        
        assert 'ids' in param_dict.keys(), 'There is no ids in the given params!'
        super(LiveGetradiosbyids, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/get_radios_by_ids'

class LiveRadiocategories(Common):
    '''获取直播电台的分类'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:id; 可选:kind,radio_category_name,order_num.
        id:直播分类ID
        kind:固定值"radio_category"
        radio_category_name:直播分类名称
        order_num:排序值,值越小排序越在前
        '''
        
        assert 'id' in param_dict.keys(), 'There is no id in the given params!'
        super(LiveRadiocategories, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/radio_categories'

class LiveGetradiobycategory(Common):
    '''根据电台分类获取直播电台数据'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:radio_category_id; 可选:page,count.
        radio_category_id:直播分类ID
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'radio_category_id' in param_dict.keys(), 'There is no radio_category_id in the given params!'
        super(LiveGetradiobycategory, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/live/get_radios_by_category'


# text = {'ids': 59}
# res = LiveGetradiosbyids(text).get()
# print(res)
