#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-27 上午9:13
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : playlist
# @Contact : xiangwenzhuo@yeah.net
"""

import API.column as api
import traceback
from utils import logger
import utils.decorator as decorator
import utils.exception as exception
import utils.result as result


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def hotplaylists(params):
    '''获取精品听单列表'''
    LOG.info('hotplaylist service:')
    LOG.info('params is %s' % params)
    try:
        if 'count' in params.keys():
            count = params['count']
        else:
            count = 20
        if 'page' in params.keys():
            page = params['page']
        else:
            page = 1
        text = {'page': page, 'count': count}
        data = api.ColumnQualitylist(text).get()
        return result.PlayListResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())

@params_check
def detail(params):
    '''听单详情'''
    LOG.info('playlist detail service:')
    LOG.info('params is %s' % params)
    try:
        if 'playlistid' in params.keys():
            playlistid = params['playlistid']
        else:
            return result.ErrorResult(exception.NoPlayListIdError())
        text = {'id': playlistid}
        data = api.ColumnDetail(text).get()
        return result.PlayListResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
