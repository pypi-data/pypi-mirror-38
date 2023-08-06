#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-26 下午2:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : main
# @Contact : guangze.yu@foxmail.com
"""
import tornado.web as web
import tornado.ioloop as ioloop
from tornado.options import options, define
import server.handler as handler
from kazoo.client import KazooClient
from utils import logger
import mq.client as mq_client
import config.zookeeper as zk_config
import config.server as server_config

LOG = logger.get_logger(__name__)
IP = server_config.IP
PORT = server_config.PORT

define('port', default=PORT, type=int, help='Server port')
define('bind', default='0.0.0.0', type=str, help='Server bind')
define('zk_connect',
       default=zk_config.zookeeper_host,
       type=str,
       help='zookeeper connect')


def zk_stats():
    """

    :return:
    """
    if ZK.state == 'LOST':
        LOG.info('zookeeper state:%s', ZK.state)
        ZK.start()


if __name__ == "__main__":
    TestHandler = handler.CommonHandler
    SearchHandler = handler.RoeweVoiceSearchHandler
    CollectHandler = handler.RoeweVoiceCollectHandler
    PlayHandler = handler.RoeweVoicePlayHandler
    PlayListHandler = handler.RoeweVoicePlayListHandler
    PlayHistoryHandler = handler.RoeweVoicePlayHistoryHandler
    MoreInfoHandler = handler.RoeweVoiceMoreInfoHandler
    RecommendHandler = handler.RoeweVoiceRecommendHandler
    AlbumHandler = handler.RoeweVoiceAlbumHandler
    handlers = [(r'/voice/collect/(.*)',CollectHandler),
                (r'/voice/search/(.*)', SearchHandler),
                (r'/voice/play/(.*)', PlayHandler),
                (r'/voice/playlist/(.*)', PlayListHandler),
                (r'/voice/playhistory/(.*)', PlayHistoryHandler),
                (r'/voice/moreinfo/(.*)', MoreInfoHandler),
                (r'/voice/recommend/(.*)', RecommendHandler),
                (r'/voice/album/(.*)', AlbumHandler)]
    app = web.Application(handlers)
    ZK = KazooClient(hosts=options.zk_connect)
    setattr(app, 'options', options)
    app.listen(options.port, address=options.bind)
    ZK.start()
    if ZK.exists('/roewe_server') is None:
        ZK.create('/roewe_server')
    if ZK.exists('/roewe_server/music') is None:
        ZK.create('/roewe_server/music')
    if ZK.exists('/roewe_server/music/%s:%s' % (IP, options.port)) is None:
        ZK.create(path='/roewe_server/music/%s:%s' % (IP, options.port), ephemeral=True)
    ioloop.PeriodicCallback(zk_stats, 100000).start()
    main_loop = ioloop.IOLoop.instance()
    mq_conn = mq_client.PikaClient(main_loop)
    setattr(app, 'mq', mq_conn)
    main_loop.start()
    ioloop.IOLoop.instance().start()