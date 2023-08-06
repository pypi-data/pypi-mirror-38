#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 上午7:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : main_server
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import tornado.web as web
import tornado.gen as gen
import tornado.concurrent as concurrent
import server.response as res
import utils.result as result
import utils.logger as logger
from utils.exception import WebHandlerError, PikaConnectionError, InValidServiceError
import json
import datetime

LOG = logger.get_logger(__name__)


class CommonHandler(web.RequestHandler):
    """
    common handler for the request.
    """
    mod = __import__('app.temp', globals(), locals(), ['object'], 0)
    executor = concurrent.futures.ThreadPoolExecutor(200)

    @web.asynchronous
    @gen.coroutine
    def post(self, service):
        """

        :param service:
        :return:
        """
        starttime = datetime.datetime.now()
        path = self.request.path
        LOG.info('request path:%s', path)
        LOG.info('request ip:%s', self.request.remote_ip)
        vin = self.request.headers.get_list('Vin')[0]
        uid = self.request.headers.get_list('User_id')[0]
        timestamp = self.request.headers.get_list('Timestamp')
        try:
            self.pika_connect()
        except PikaConnectionError:
            traceback.print_exc()
            LOG.info('Rabbitmq connect failure.')
        try:
            body_params = self.request.body
            if body_params.decode('utf-8'):
                params = json.loads(body_params.decode('utf-8'))
            else:
                params = {}
            if vin:
                params['vin'] = vin
            if uid:
                params['uid'] = uid
            if timestamp:
                params['timestamp'] = timestamp[0]
            params['ip'] = self.request.remote_ip
            LOG.info('request params:%s', params)
            app_result = yield self.async_fun(service, params)
        except Exception:
            traceback.print_exc()
            app_result = result.ErrorResult(WebHandlerError())
        return_info = res.Response(app_result, path, 'POST').info
        message = app_result.message
        self.set_header("Content-Type", "application/json")
        self.set_header("Status_code", app_result.status_code)
        self.set_header("Status_info", app_result.status_info)
        self.write(return_info)
        self.finish()
        endtime = datetime.datetime.now()
        print(
            "----------------------------------------------------------------------------------------------------------")
        print(endtime - starttime)
        print(
            "----------------------------------------------------------------------------------------------------------")
        if message is not None:
            self.application.mq.channel.queue_declare(callback=None,
                                                      queue='map',
                                                      durable=True)
            self.application.mq.channel.basic_publish(exchange='',
                                                      routing_key='map',
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
        if service in self.mod.__dict__:
            func = getattr(self.mod, service)
            return func(params)
        else:
            return result.ErrorResult(InValidServiceError())


class MapBroadcastHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.broadcast', globals(), locals(), ['object'], 0)


class MapCollectHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.collect', globals(), locals(), ['object'], 0)


class MapLocationHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.location', globals(), locals(), ['object'], 0)


class MapOperationHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.operation', globals(), locals(), ['object'], 0)


class MapPoiHistoryHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.poihistory', globals(), locals(), ['object'], 0)


class MapSearchHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.search', globals(), locals(), ['object'], 0)


class MapUsualAddressHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.usualaddress', globals(), locals(), ['object'], 0)


class MapWeatherHandler(CommonHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.weather', globals(), locals(), ['object'], 0)


class MapTempHandler(web.RequestHandler):
    """
    Map broadcast handler
    """
    mod = __import__('app.temp', globals(), locals(), ['object'], 0)
    executor = concurrent.futures.ThreadPoolExecutor(200)

    @web.asynchronous
    @gen.coroutine
    def post(self):
        path = self.request.path
        if path == '/map/getgps':
            service = 'getgps'
        elif path == '/map/gpsupdate':
            service = 'gpsupdate'
        elif path == '/map/getvehicles':
            service = 'getvehicles'
        elif path == '/map/gettrace':
            service = 'gettrace'
        elif path == '/map/selfgettrace':
            service = 'selfgettrace'
        else:
            service = 'invalid'
        try:
            body_params = self.request.body
            if body_params.decode('utf-8'):
                params = json.loads(body_params.decode('utf-8'))
            else:
                params = {}
            params['ip'] = self.request.remote_ip
            LOG.info('request params:%s', params)
            app_result = yield self.async_fun(service, params)
        except WebHandlerError:
            traceback.print_exc()
            app_result = result.ErrorResult(WebHandlerError())
        return_info = res.TempResponse(app_result, path, 'POST').info
        self.set_header("Content-Type", "application/json")
        self.set_header("status", app_result.status_code)
        self.write(return_info)
        self.finish()

    @concurrent.run_on_executor
    def async_fun(self, service, params):
        """

        :param service:
        :param params:
        :return:
        """
        func = getattr(self.mod, service)
        return func(params)
