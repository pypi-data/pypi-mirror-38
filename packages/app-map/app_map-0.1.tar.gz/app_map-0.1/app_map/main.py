#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-12 下午3:43
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : main
# @Contact : guangze.yu@foxmail.com
"""

from json import load
import tornado.web as web
import server.handler as handler
import tornado.ioloop as ioloop
from tornado.options import options, define
from kazoo.client import KazooClient
from utils import logger
import mq.mq_client as mq_client
import config.zookeepr as config
import database.cache as cache
import vendor.tuju.tuju as tuju
from urllib.request import urlopen


def gpsupdate():
    """

    :return:
    """
    vin = 'LSJA1234567890112'
    cache_loc = cache.VehicleLocation(vin)
    info = cache_loc.last_loc
    if info is None:
        out = 'No location info on the remote.'
    else:
        out = info
        # timestamp = time.time()
        # print(timestamp)
        # print(out)
        params = {"location": out.decode('utf-8'),
                  "uid": 123456,
                  "floor": -1}
        update = tuju.GPSUpdate(params)
        res = update.post()
        print(res)


LOG = logger.get_logger(__name__)
IP = load(urlopen('http://ip-api.com/json'))['query']

define('port', default=8888, type=int, help='Server port')
define('bind', default='0.0.0.0', type=str, help='Server bind')
define('zk_connect',
       default=config.zookeeper_host,
       type=str,
       help='zookeeper connect')

ZK = KazooClient(hosts=options.zk_connect)


def zk_stats():
    """

    :return:
    """
    if ZK.state == 'LOST':
        LOG.info('zookeeper state:%s' % ZK.state)
        ZK.start()


if __name__ == "__main__":
    TestHandler = handler.CommonHandler
    BroadcastHandler = handler.MapBroadcastHandler
    CollectHandler = handler.MapCollectHandler
    LocationHandler = handler.MapLocationHandler
    PoiHistoryHandler = handler.MapPoiHistoryHandler
    SearchHandler = handler.MapSearchHandler
    TempHandler = handler.MapTempHandler
    WeatherHandler = handler.MapWeatherHandler
    OperationHandler = handler.MapOperationHandler
    UsualAddressHandler = handler.MapUsualAddressHandler
    handlers = [(r'/map/test/(.*)', TestHandler),
                (r'/map/broadcast/(.*)', BroadcastHandler),
                (r'/map/collect/(.*)', CollectHandler),
                (r'/map/location/(.*)', LocationHandler),
                (r'/map/poihistory/(.*)', PoiHistoryHandler),
                (r'/map/search/(.*)', SearchHandler),
                (r'/map/weather/(.*)', WeatherHandler),
                (r'/map/operation/(.*)', OperationHandler),
                (r'/map/usualaddress/(.*)', UsualAddressHandler),
                (r'/map/getgps', TempHandler),
                (r'/map/gpsupdate', TempHandler),
                (r'/map/getvehicles', TempHandler),
                (r'/map/gettrace', TempHandler),
                (r'/map/selfgettrace', TempHandler)]
    app = web.Application(handlers)
    setattr(app, 'options', options)
    app.listen(options.port, address=options.bind)
    ZK.start()
    if ZK.exists('/roewe_server') is None:
        ZK.create('/roewe_server')
    if ZK.exists('/roewe_server/map') is None:
        ZK.create('/roewe_server/map')
    if ZK.exists('/roewe_server/map/%s:%s' % (IP, options.port)) is None:
        ZK.create(path='/roewe_server/map/%s:%s' % (IP, options.port), ephemeral=True)
    ioloop.PeriodicCallback(zk_stats, 100000).start()
    # ioloop.PeriodicCallback(gpsupdate, 1000).start()
    main_loop = ioloop.IOLoop.instance()
    mq_conn = mq_client.PikaClient(main_loop)
    setattr(app, 'mq', mq_conn)
    main_loop.start()
