#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-7-05 上午10:13
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : playlist
# @Contact : xiangwenzhuo@yeah.net
"""

import API.demand as api
import traceback
from utils import logger
import utils.decorator as decorator
import utils.exception as exception
import utils.result as result


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def metadatalbums(params):
    """

    :param params:
    :return:
    """
    LOG.info('album/metadatalbums service:')
    LOG.info('params is %s' % params)
    try:
        text = {}
        data = api.CategoriesList(text).get()
        return result.AlbumResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def V2TagsList(params):
    """

    :param params: a dict contain category_id, type
    :return:
    """
    LOG.info('album/V2TagsList service:')
    LOG.info('params is %s' % params)
    try:
        id = params['category_id']
        type = params['type']
        text = {'category_id': id, 'type': type}
        data = api.V2TagsList(text).get()
        return result.AlbumResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def V2AlbumsList(params):
    """
    根据分类和标签获取某个分类某个标签下的热门专辑列表/最新专辑列表/最多播放专辑列表(V2版本)
    :param params: a dict, contain access_token, category_id, optional param, contain calc_dimension, page and count
        参数:除公共参数外,必须包含:category_id,calc_dimension; 可选:tag_name,page,count.
        category_id:分类ID,指定分类,为0时表示热门分类
        calc_dimension:calc_dimension:计算维度,现支持最火(1),最新(2),经典或播放最多(3)
        tag_name:分类下对应的专辑标签
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
    :return:
    """
    LOG.info('album/V2AlbumList')
    LOG.info('params is %s' % params)
    try:
        id = params['category_id']
        calc = params['calc_dimension']
        text = {'category_id': id, 'calc_dimension': calc}
        data = api.V2AlbumsList(text).get()
        return result.AlbumResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def tags(params):
    """

    :param params:
    :return:
    """
    LOG.info('album/tags')
    LOG.info('params is %s' % params)
    try:
        key = int(params['key'])
        res1 = [[3], [12, 16], [9, 39], [4, 28, 23, 24],
                [6], [2, 29], [40, 34], [15],
                [1], [21], [30, 13, 32, 38, 41], [8, 18],
                [7], [17], [22], [31, 10]]
        num = res1[key]
        a = int(20 / len(num))
        data = []
        for i in num:
            text = {'category_id': i, 'calc_dimension': 1}
            res = api.V2AlbumsList(text).get()
            res2 = res['albums'][0:a]
            for n in res2:
                data.append(n)
        return result.AlbumResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError)

