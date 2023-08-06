#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-26 下午2:33
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : testhandler
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import json
import tornado.web as web
import tornado.gen as gen
import tornado.concurrent as concurrent
import server.response as res
import utils.result as result
from utils import logger
from utils.exception import WebHandlerError, PikaConnectionError

LOG = logger.get_logger(__name__)


class CommonHandler(web.RequestHandler):
    """
    common handler for the request.
    """
    mod = __import__('app.test', globals(), locals(), ['object'], 0)
    executor = concurrent.futures.ThreadPoolExecutor(100)

    @web.asynchronous
    @gen.coroutine
    def post(self, service):
        """

        :param service:
        :return:
        """
        path = self.request.path
        LOG.info('request path:%s', path)
        LOG.info('request ip:%s', self.request.remote_ip)
        vin = self.request.headers.get_list('vin')
        uid = self.request.headers.get_list('User_id')
        timestamp = self.request.headers.get_list('Timestamp')
        try:
            self.pika_connect()
        except PikaConnectionError:
            traceback.print_exc()
            LOG.info('Rabbitmq connect failuer.')
        try:
            body_params = self.request.body
            if body_params.decode('utf-8'):
                params = json.loads(body_params.decode('utf-8'))
            else:
                params = {}
            if vin:
                params['vin'] = vin[0]
            if uid:
                params['uid'] = uid[0]
            if timestamp:
                params['timestamp'] = timestamp[0]
            LOG.info('request params:%s', params)
            app_result = yield self.async_fun(service, params)
        except WebHandlerError:
            traceback.print_exc()
            app_result = result.ErrorResult(WebHandlerError())
        return_info = res.Response(app_result, path, 'POST').info
        message = app_result.message
        self.set_header("Content-Type", "application/json")
        self.set_header("Status_code", app_result.status_code)
        self.set_header("Status_info", app_result.status_info)
        self.write(return_info)
        self.finish()
        if message is not None:
            self.application.mq.channel.queue_declare(callback=None,
                                                      queue='voice',
                                                      durable=True)
            self.application.mq.channel.basic_publish(exchange='',
                                                      routing_key='voice',
                                                      body=json.dumps(message))

    def pika_connect(self):
        """

        :return:
        """
        self.application.mq.connect()

    @concurrent.run_on_executor
    def async_fun(self, service, params):
        """

        :param service:
        :param params:
        :return:
        """
        func = getattr(self.mod, service)
        return func(params)


class RoeweVoiceSearchHandler(CommonHandler):
    mod = __import__('app.search', globals(), locals(), ['object'], 0)


class RoeweVoiceCollectHandler(CommonHandler):
    mod = __import__('app.collect', globals(), locals(), ['object'], 0)


class RoeweVoicePlayHistoryHandler(CommonHandler):
    mod = __import__('app.playhistory', globals(), locals(), ['object'], 0)


class RoeweVoicePlayListHandler(CommonHandler):
    mod = __import__('app.playlist', globals(), locals(), ['object'], 0)


class RoeweVoicePlayHandler(CommonHandler):
    mod = __import__('app.play', globals(), locals(), ['object'], 0)


class RoeweVoiceMoreInfoHandler(CommonHandler):
    mod = __import__('app.more', globals(), locals(), ['object'], 0)


class RoeweVoiceRecommendHandler(CommonHandler):
    mod = __import__('app.recommend', globals(), locals(), ['object'], 0)


class RoeweVoiceAlbumHandler(CommonHandler):
    mod = __import__('app.album', globals(), locals(), ['object'], 0)