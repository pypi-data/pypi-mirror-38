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

class CustomizedCategories(Common):
    '''获取喜马拉雅提供的由合作方自定义图标的内容分类'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:icon_set_id.
        icon_set_id:定制化的图标集ID
        '''
        
        assert 'icon_set_id' in param_dict.keys(), 'There is no icon_set_id in the given params!'
        super(CustomizedCategories, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/customized/categories'

class CustomizedTracks(Common):
    '''获取合作方定制化的声音列表'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:customized_tracklist_id; 可选:page,count.
        customized_tracklist_id:定制化的声音集ID
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'customized_tracklist_id' in param_dict.keys(), 'There is no customized_tracklist_id in the given params!'
        super(CustomizedTracks, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/customized/tracks'

class V2CustomizedAlbumcolumns(Common):
    '''根据搜索条件和分页参数,获取符合条件的合作方自定制的专辑类听单'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,可选:publish_date_start,publish_date_end,dimensions,with_dimensions,page,count.
        publish_date_start:发布起始日期,与publish_date_end一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                           格式为”yyyyMMdd”,比如”20161123”.publish_date_start与publish_date_end必须成对出现.
        publish_date_end:发布截止日期,与publish_date_start一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                         格式为”yyyyMMdd”,比如”20161124” publish_date_start与publish_date_end必须成对出现.
        dimensions:维度(在自运营内容网站上配置)过滤参数,限定只返回满足维度过滤条件的听单内容详情.格式为:dimId1:dimVal1;
                   dimId2:dimVal2 ,比如有一个ID为1的维度表示孕期第几天,有一个ID为2的维度表示内容标签,则可以有”1:7;2:音乐”,
                   返回的是孕期第7天且内容标签为音乐的内容详情
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        super(V2CustomizedAlbumcolumns, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/v2/customized/album_columns'

class V2CustomizedTrackcolumns(Common):
    '''根据搜索条件和分页参数,获取符合条件的合作方自定制的声音类听单'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,可选:publish_date_start,publish_date_end,dimensions,with_dimensions,page,count.
        publish_date_start:发布起始日期,与publish_date_end一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                           格式为”yyyyMMdd”,比如”20161123”.publish_date_start与publish_date_end必须成对出现.
        publish_date_end:发布截止日期,与publish_date_start一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                         格式为”yyyyMMdd”,比如”20161124” publish_date_start与publish_date_end必须成对出现.
        dimensions:维度(在自运营内容网站上配置)过滤参数,限定只返回满足维度过滤条件的听单内容详情.格式为:dimId1:dimVal1;
                   dimId2:dimVal2 ,比如有一个ID为1的维度表示孕期第几天,有一个ID为2的维度表示内容标签,则可以有”1:7;2:音乐”,
                   返回的是孕期第7天且内容标签为音乐的内容详情
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        super(V2CustomizedTrackcolumns, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/v2/customized/track_columns'

class V2CustomizedAlbumcolumndetail(Common):
    '''根据搜索条件和分页参数,获取自定义专辑听单内容详情.'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:id;
            可选:category_id,paid_filter_type,publish_date_start,publish_date_end,dimensions,with_dimensions,page,count.
        id:自定义专辑听单ID
        category_id:分类ID,如果设置了则限制只返回指定分类下的内容详情
        paid_filter_type:付费专辑过滤字段,-1 –无此属性,0 –免费专辑,1 –付费专辑.如果不传该字段,则不根据该字段过滤.
        publish_date_start:发布起始日期,与publish_date_end一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                           格式为”yyyyMMdd”,比如”20161123”.publish_date_start与publish_date_end必须成对出现.
        publish_date_end:发布截止日期,与publish_date_start一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                         格式为”yyyyMMdd”,比如”20161124” publish_date_start与publish_date_end必须成对出现.
        dimensions:维度(在自运营内容网站上配置)过滤参数,限定只返回满足维度过滤条件的听单内容详情.格式为:dimId1:dimVal1;
                   dimId2:dimVal2 ,比如有一个ID为1的维度表示孕期第几天,有一个ID为2的维度表示内容标签,则可以有”1:7;2:音乐”,
                   返回的是孕期第7天且内容标签为音乐的内容详情
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'id' in param_dict.keys(), 'There is no id in the given params!'
        super(V2CustomizedAlbumcolumndetail, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/v2/customized/album_column_detail'

class V2CustomizedTrackcolumndetail(Common):
    '''根据搜索条件和分页参数,获取自定义声音听单内容详情.'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:id;
            可选:category_id,publish_date_start,publish_date_end,dimensions,with_dimensions,page,count.
        id:自定义专辑听单ID
        category_id:分类ID,如果设置了则限制只返回指定分类下的内容详情
        publish_date_start:发布起始日期,与publish_date_end一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                           格式为”yyyyMMdd”,比如”20161123”.publish_date_start与publish_date_end必须成对出现.
        publish_date_end:发布截止日期,与publish_date_start一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                         格式为”yyyyMMdd”,比如”20161124” publish_date_start与publish_date_end必须成对出现.
        dimensions:维度(在自运营内容网站上配置)过滤参数,限定只返回满足维度过滤条件的听单内容详情.格式为:dimId1:dimVal1;
                   dimId2:dimVal2 ,比如有一个ID为1的维度表示孕期第几天,有一个ID为2的维度表示内容标签,则可以有”1:7;2:音乐”,
                   返回的是孕期第7天且内容标签为音乐的内容详情
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'id' in param_dict.keys(), 'There is no id in the given params!'
        super(V2CustomizedTrackcolumndetail, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/v2/customized/track_column_detail'

class CustomizedSearchtracks(Common):
    '''根据搜索条件和分页参数,搜索所有声音听单下符合条件的声音列表.'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,可选:q,category_id,publish_date_start,publish_date_end,dimensions,with_dimensions,page,count.
        q:搜索关键词,如果设置了则限制只返回满足关键词过滤条件的听单内容详情
        category_id:分类ID,如果设置了则限制只返回指定分类下的内容详情
        publish_date_start:发布起始日期,与publish_date_end一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                           格式为”yyyyMMdd”,比如”20161123”.publish_date_start与publish_date_end必须成对出现.
        publish_date_end:发布截止日期,与publish_date_start一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                         格式为”yyyyMMdd”,比如”20161124” publish_date_start与publish_date_end必须成对出现.
        dimensions:维度(在自运营内容网站上配置)过滤参数,限定只返回满足维度过滤条件的听单内容详情.格式为:dimId1:dimVal1;
                   dimId2:dimVal2 ,比如有一个ID为1的维度表示孕期第几天,有一个ID为2的维度表示内容标签,则可以有”1:7;2:音乐”,
                   返回的是孕期第7天且内容标签为音乐的内容详情
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        super(CustomizedSearchtracks, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/customized/search_tracks'

class CustomizedTrackdetail(Common):
    '''根据声音ID和该声音所属声音听单ID获取声音详情'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:track_id,track_column_id; 可选:with_dimensions.
        track_id:声音ID
        track_column_id:声音所属听单ID
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        '''
        
        assert 'track_id' in param_dict.keys(), 'There is no track_id in the given params!'
        assert 'track_column_id' in param_dict.keys(), 'There is no track_column_id in the given params!'
        super(CustomizedTrackdetail, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/customized/track_detail'

class CustomizedSearchalbumsortrackcolumns(Common):
    '''根据搜索条件和分页参数,搜索所有专辑或声音听单,返回结果已去重'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:result_content_type; 可选:q,category_id,paid_filter_type,publish_date_start,
            publish_date_end,dimension_filter_type,dimensions,calc_dimensions,with_dimensions,page,count.
        result_content_type:搜索结果内容类型:album-专辑,trackColumn-声音听单
        q:搜索关键词,如果设置了则限制只返回满足关键词过滤条件的听单内容详情
        category_id:分类ID,如果设置了则限制只返回指定分类下的内容详情
        paid_filter_type:付费专辑过滤字段,-1 –无此属性,0 –免费专辑,1 –付费专辑.如果不传该字段,则不根据该字段过滤.
        publish_date_start:发布起始日期,与publish_date_end一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                           格式为”yyyyMMdd”,比如”20161123”.publish_date_start与publish_date_end必须成对出现.
        publish_date_end:发布截止日期,与publish_date_start一起组成日期区间,限定只返回指定发布时间区间内的内容详情,
                         格式为”yyyyMMdd”,比如”20161124” publish_date_start与publish_date_end必须成对出现.

        dimensions_filter_type:维度过滤类型:1-交集,2-并集. 默认交集.
        dimensions:维度(在自运营内容网站上配置)过滤参数,限定只返回满足维度过滤条件的听单内容详情.格式为:dimId1:dimVal1;
                   dimId2:dimVal2 ,比如有一个ID为1的维度表示孕期第几天,有一个ID为2的维度表示内容标签,则可以有”1:7;2:音乐”,
                   返回的是孕期第7天且内容标签为音乐的内容详情
        calc_dimensions:返回结果排序维度:2-最新创建在前,3-最多播放在前,默认为2.
        with_dimensions:返回值是否带上维度配置数据,不填则默认为false
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'result_content_type' in param_dict.keys(), 'There is no result_content_type in the given params!'
        super(CustomizedSearchalbumsortrackcolumns, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/customized/search_albums_or_track_columns'
