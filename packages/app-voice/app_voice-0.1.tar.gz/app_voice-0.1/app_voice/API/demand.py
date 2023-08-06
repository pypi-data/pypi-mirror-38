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

class CategoriesList(Common):
    '''获取喜马拉雅内容分类'''
    def __init__(self, param_dict):
        '''Create a new categories_list object.
        :param  a dict, contain access_token
        参数:公共参数
        access_token:
        '''
        
        super(CategoriesList, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/categories/list'

class V2TagsList(Common):
    '''获取声音或专辑的标签'''
    def __init__(self, param_dict):
        '''Create a new v2_tags object.
        :param  a dict, contain access_token, category_id, type
        参数:除公共参数外,必须包含:category_id, type
        category_id:分类ID,指定分类,为0时表示热门分类
        type:指定查询的是专辑标签还是声音标签,0-专辑标签
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        assert 'type' in param_dict.keys(), 'There is no type in the given params!'
        super(V2TagsList, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/v2/tags/list'

class V2AlbumsList(Common):
    '''根据分类和标签获取某个分类某个标签下的热门专辑列表/最新专辑列表/最多播放专辑列表(V2版本)'''
    def __init__(self, param_dict):
        '''Create a new albums object.
        :param  a dict, contain access_token, category_id, optional param, contain calc_dimension, page and count
        参数:除公共参数外,必须包含:category_id,calc_dimension; 可选:tag_name,page,count.
        category_id:分类ID,指定分类,为0时表示热门分类
        calc_dimension:calc_dimension:计算维度,现支持最火(1),最新(2),经典或播放最多(3)
        tag_name:分类下对应的专辑标签
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        assert 'calc_dimension' in param_dict.keys(), 'There is no calc_dimension in the given params!'
        super(V2AlbumsList, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/v2/albums/list'

class AlbumsBrowse(Common):
    '''根据专辑ID获取专辑下的声音列表,即专辑浏览'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:album_id; 可选:sort,page,count.
        album_id:专辑ID
        sort:"asc"表示喜马拉雅正序,"desc"表示喜马拉雅倒序,"time_asc"表示时间升序,"time_desc"表示时间降序,默认为"asc"
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'album_id' in param_dict.keys(), 'There is no album_id in the given params!'
        super(AlbumsBrowse, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/browse'

class AlbumsGetbatch(Common):
    '''批量获取专辑列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids.
        ids:专辑ID列表,传参时用英文逗号分割,最大ID数量为200个,超过200个的ID将忽略.
        '''
        
        assert 'ids' in param_dict.keys(), 'There is no ids in the given params!'
        super(AlbumsGetbatch, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/get_batch'

class AlbumsGetupdatebatch(Common):
    '''根据专辑ID列表获取批量专辑更新提醒信息列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids.
        ids:专辑ID列表,传参时用英文逗号分隔.
        '''
        
        assert 'ids' in param_dict.keys(), 'There is no ids in the given params!'
        super(AlbumsGetupdatebatch, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/albums/get_update_batch'

class TracksHot(Common):
    '''根据分类和标签获取某个分类某个标签下的热门声音列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:category_id; 可选:tag_name,page,count.
        category_id:分类ID,指定分类,为0表示热门分类.
        tag_name:分类下对应声音标签,不填则为热门分类
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        super(TracksHot, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/tracks/hot'

class TracksGetbatch(Common):
    '''批量获取声音'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ids.
        ids:声音ID列表,传参时用英文逗号分割,最大ID数量为200个,超过200个的ID将忽略.
        '''
        
        assert 'ids' in param_dict.keys(), 'There is no ids in the given params!'
        super(TracksGetbatch, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/tracks/get_batch'

class TracksGetlastplaytracks(Common):
    '''根据上一次所听声音的id,获取此声音所在那一页的声音'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:ablum_id,track_id; 可选:count,sort.
        ablum_id:专辑id
        track_id:声音id
        count:分页请求参数,表示每页多少条记录,默认20,最多不超过200
        sort:"asc"表示正序或"desc"表示倒序,默认为"asc"
        '''
        
        assert 'album_id' in param_dict.keys(), 'There is no album_id in the given params!'
        assert 'track_id' in param_dict.keys(), 'There is no track_id in the given params!'
        super(TracksGetlastplaytracks, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/tracks/get_last_play_tracks'

class MetadataList(Common):
    '''获取某个分类下的元数据列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:category_id.
        category_id:分类id,指定分类.
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        super(MetadataList, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/metadata/list'

class MetadataAlbums(Common):
    '''获取某个分类的元数据属性键值组合下包含的热门专辑列表/最新专辑列表/最多播放专辑列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:category_id,calc_dimension;可选:metadata_attributes,page,count.
        category_id:分类id,指定分类,为0时表示热门分类.
        calc_dimension:计算维度,现支持最火(1),最新(2),经典或播放最多(3)
        metadata_attributes:元数据属性列表:在/metadata/list接口得到的结果中,取不同元数据属性的attr_key和atrr_value组成任意个数
                       的key-value键值,格式如:attr_key1:attr_value1;attr_key2:attr_value2;attr_key3:attr_value3
                       注意:此字段可为空,表示获取此分类下全部的最火、最新或者播放最多的专辑列表.
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'category_id' in param_dict.keys(), 'There is no category_id in the given params!'
        assert 'calc_dimension' in param_dict.keys(), 'There is no calc_dimension in the given params!'
        super(MetadataAlbums, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/metadata/albums'


# text = {'album_id': '86573', 'ids': '46430562', 'category_id': '13', 'calc_dimension': '1'}
# res = CategoriesList(text)
# res = MetadataList(text)
# res = MetadataAlbums(text)
# res2 = res.get()
# print(res2)
