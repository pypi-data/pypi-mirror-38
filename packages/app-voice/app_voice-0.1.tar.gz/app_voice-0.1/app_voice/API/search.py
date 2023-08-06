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

class SearchAlbums(Common):
    '''搜索专辑'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:q; 可选:category_id,calc_dimension,page,count.
        q:搜索关键词
        category_id:分类ID,指定分类,为0时表示热门分类
        calc_dimension:排序条件:2-最新,3-最多播放,4-最相关(默认)
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'q' in param_dict.keys(), 'There is no search word in the given params!'
        super(SearchAlbums, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/albums'

class SearchTracks(Common):
    '''搜索声音'''
    def __init__(self, param_dict):
        '''
        :param param_dict: q:search word category_id: ID of category calc_dimension: sorted condition(2~4).
        参数:除公共参数外,必须包含:q; 可选:category_id,calc_dimension,page,count.
        q:搜索关键词
        category_id:分类ID,指定分类,为0时表示热门分类
        calc_dimension:排序条件:2-最新,3-最多播放,4-最相关(默认)
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'q' in param_dict.keys(), 'There is no search word in the given params!'
        super(SearchTracks, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/tracks'

class SearchHotwords(Common):
    '''获取最新热搜词'''
    def __init__(self,param_dict):
        '''
        参数:除公共参数外,必须包含:top.
        top:获取前top长度的热搜词.(1<=top<=20:目前top只支持最多20个)
        '''
        
        assert 'top' in param_dict.keys(), 'There is no top length in the given params!'
        super(SearchHotwords, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/hot_words'

class SearchSuggestwords(Common):
    '''获取某个关键词的联想词'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:q.
        q:搜索查询词参数
        '''
        
        assert 'q' in param_dict.keys(), 'There is no search word in the given params!'
        super(SearchSuggestwords, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/suggest_words'

class SearchRadios(Common):
    '''按照关键词搜索直播'''
    def __init__(self,param_dict):
        '''
        参数:除公共参数外,必须包含:q; 可选:radio_category_id,area,lnt,lat,outer_ip,count,page.
        q:搜索查询词参数
        radio_category_id:直播分类ID
        area:搜索地区参数.如果此参数有值,请在q参数中保留地区关键字以保证搜索质量,比如:q:上海交通广播; area:上海
        lnt:经度参数
        lat:纬度参数
        outer_ip:IP参数,此参数需传公网IP,如果需要根据地理位置查询,则经纬度和IP参数至少传一个
        count:每页多少条,默认20,最多不超过200
        page:分页请求参数,表示请求第几页,默认为1即第一页
        '''
        
        assert 'q' in param_dict.keys(), 'There is no search word in the given params!'
        super(SearchRadios, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/radios'

class SearchAnnouncers(Common):
    '''搜索主播'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:q; 可选:calc_dimension,page,count.
        q:搜索查询词参数
        calc_dimension:排序条件:4-最相关(默认),5-粉丝最多,6-声音最多
        page:返回第几页,必须大于等于1,不填默认为1
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'q' in param_dict.keys(), 'There is no search word in the given params!'
        super(SearchAnnouncers, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/announcers'

class SearchAll(Common):
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,必须包含:q; 可选:page,count.
        page:分页请求参数,表示请求第几页,默认为1即第一页
        count:每页多少条,默认20,最多不超过200
        '''
        
        assert 'q' in param_dict.keys(), 'There is no search word in the given params!'
        super(SearchAll, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/all'

class SearchSmartSearch(Common):
    '''智能搜索,可以用于语音搜索场景'''
    def __init__(self, param_dict):
        '''
        参数:除公共参数外,可选:q,category_id,metadatas,seq,date_range,search_result_list_size,recommend_result_list_size,
                            contains_paid.
        q:搜索关键词,若为空则按分类搜索
        category_id:分类ID,指定分类,为0时表示热门分类
        metadatas:元数据名称,为对应分类的中文名称,可指定多个,中间用英文逗号分隔
        seq:集数约束条件,以s或e开头,后面跟着集数,s代表从前往后,e从后往前.比如s2代表从前往后第二集,e3代表从后往前第三集.若此参数添值,
            搜索结果返回个数为1
        date_range:日期约束条件,格式为yyyy-MM-dd,yyy-MM-dd,其中的逗号为英文逗号,后面日期必须大于等于前面日期.比如2015-01-01,
                   2016-12-31.若此参数填值,搜索结果返回个数为1
        search_result_list_size:指定搜索返回结果的个数.与推荐结果个数之和不超过20.
        recommend_result_list_size:指定推荐返回结果的个数.与搜索结果个数之和不超过20
        contains_paid:是否输出付费专辑
        '''
        
        super(SearchSmartSearch, self).__init__()
        self._param_private = param_dict
        self._url = 'http://api.ximalaya.com/search/smart_search'

# s = {'top':'10'}
# t = SearchHotwords(s).get()
# print(t)

# s = {'q':'高晓松'}
# t = SearchSuggestwords(s).get()
# print(t)

# s = {'q':'高晓松'}
# t = SearchAlbums(s).get()
# print(t)

# s = {'q':'晓说2017'}
# t = SearchTracks(s).get()
# print(t)

# s = {'q':'晓说2017'}
# t = SearchRadios(s).get()
# print(t)

# s = {'q':'高晓松'}
# t = SearchAnnouncers(s).get()
# print(t)

# s = {'q':'高晓松'}
# t = SearchAll(s).get()
# print(t)
# # mp3链接点击无法跳转






