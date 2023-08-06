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

class ProfileUserinfo(Common):
    '''根据用户ID获取用户基本信息'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid.
        uid:当前用户ID
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        super(ProfileUserinfo, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/profile/user_info'

class ProfilePersona(Common):
    '''根据用户ID获取用户画像资料'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:uid.
        uid:当前用户ID
        '''
        
        assert 'uid' in param_dict.keys(), 'There is no uid in the given params!'
        super(ProfilePersona, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/profile/persona'