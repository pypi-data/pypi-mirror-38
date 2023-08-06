#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/6/6 13:00
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : album
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""

import API.common as common

Common = common.Common

class GetBatch(Common):
    def __init__(self, param_dict):
        '''Create a new categories_list object.
        :param  a dict, contain access_token
        参数:公共参数
        access_token:
        '''

        super(GetBatch, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/get_batch'
