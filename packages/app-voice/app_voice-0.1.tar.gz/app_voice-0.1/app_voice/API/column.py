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

class ColumnQualitylist(Common):
    '''获取精品听单列表'''
    def __init__(self, param_dict):
        '''
        参数:公共参数; 可选:page,count.
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        super(ColumnQualitylist, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/column/quality_list'

class ColumnDetail(Common):
    '''获取某个听单详情,每个听单包含听单简介信息和专辑或声音的列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:id.
        id:听单ID
        '''
        
        assert 'id' in param_dict.keys(), 'There is no id in the given params!'
        super(ColumnDetail, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/column/detail'


# t = {'id': '1977'}
# s = ColumnDetail(t).get()
# print(s)