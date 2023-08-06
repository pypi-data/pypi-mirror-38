#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:15
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : collect
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""


def delpoi():
    """
    @api {post} /map/collect/delpoi 删除收藏
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 删除收藏

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} poi_id poi_id

    @apiSuccess (Success) {String} data 成功标识

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_049b93db7754407bb872aaee3d28f352",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    @apiError (Error) 21020 No poi_id in the request params

    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21020",
            "msg": "No poi_id in the request params!"
        },
        "req_id": "r_da328a55dfbc46bda249122030b8677d"
    }
    """


def addpoi():
    """
    @api {post} /map/collect/addpoi 增加收藏
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 增加收藏

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} poi_id poi_id
    @apiParam (Body) {String} location 经纬度

    @apiSuccess (Success) {String} data 成功标识

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_049b93db7754407bb872aaee3d28f352",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }
    @apiError (Error) 21020  No poi_id in the request params

    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21020",
            "msg": "No poi_id in the request params!"
        },
        "req_id": "r_da328a55dfbc46bda249122030b8677d"
    }
    """


def getpoi():
    """
    @api {post} /map/collect/getpoi  获取收藏
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 获取收藏

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} location 经纬度

    @apiSuccess (Success) {Object[]} data 搜索收藏信息列表
    @apiSuccess (Success) {String} typecode 兴趣点类型编码
    @apiSuccess (Success) {String} address 地址
    @apiSuccess (Success) {String} citycode 城市编码
    @apiSuccess (Success) {String} adname 区域名称
    @apiSuccess (Success) {String} adcode 区域编码
    @apiSuccess (Success) {String} cityname 城市名
    @apiSuccess (Success) {String} name 名称
    @apiSuccess (Success) {String} tel 该POI的电话
    @apiSuccess (Success) {String} location 经纬度
    @apiSuccess (Success) {String} id 唯一ID
    @apiSuccess (Success) {String} type 兴趣点类型

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "typecode": "060000",
                "address": "张江高科技园区盛大青春里二期",
                "citycode": "021",
                "adname": "浦东新区",
                "adcode": "310115",
                "cityname": "上海市",
                "name": "联华",
                "tel": "",
                "location": "121.606493,31.170950",
                "id": "B0FFHP6I9M",
                "type": "购物服务;购物相关场所;购物相关场所"
            }
        ],
        "req_id": "r_14e5cb206c604e2aaad2cb655a9bdf71",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }
    """
