#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/13 12:35
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : response
# @Project : roewe_voice
# @Contact : guangze.yu@foxmail.com
"""


class Response(object):
    def __init__(self, app_result, request_path, method):
        """

        :param app_result:
        :param request_path:
        :param method:
        """
        self._result = app_result
        self._path = request_path
        self._method = method

    @property
    def info(self):
        res_info = {'data': self._result.response}
        return res_info

    def __repr__(self):
        return self.info
