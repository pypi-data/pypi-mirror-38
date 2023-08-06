#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:14
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : poihistory
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""


def get():
    """
    @api {post} /map/poihistory/get  获取历史
    @apiVersion 1.0.0
    @apiGroup History
    @apiDescription  获取历史

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} page 页数

    @apiSuccess (Success) {String}  keywords 关键字
    @apiSuccess (Success) {String}  sqtype 类型
    @apiSuccess (Success) {String}  time 时间

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "keywords": "加油站",
                "sqtype": "KEYWORD",
                "time": "2018-07-17 14:09:22"
            }
        ],
        "req_id": "r_bb99baa658c4414faeed31b9d82ca3a4",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    """


def clear():
    """
    @api {post} /map/poihistory/clear 清空历史
    @apiVersion 1.0.0
    @apiGroup History
    @apiDescription  清空历史

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiSuccess (Success) {String} data 成功标识

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_cf9f3d0170b142ffb5bc2b0bcea97501",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }
    """


def delete():
    """
    @api {post} /map/poihistory/delete 删除历史
    @apiVersion 1.0.0
    @apiGroup History
    @apiDescription  删除历史

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} poi_id poi_id
    @apiParam (Body) {String} keywords 关键字

    @apiSuccess (Success) {String} data 成功标识

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_66a02102d89d4c3386d68673d1a7ada8",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    @apiError (Error)  21020 No poi_id in the request params

    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21020",
            "msg": "No poi_id in the request params!"
        },
        "req_id": "r_254eaeba9a944211b9bd5a5a5705539f"
    }
    """


