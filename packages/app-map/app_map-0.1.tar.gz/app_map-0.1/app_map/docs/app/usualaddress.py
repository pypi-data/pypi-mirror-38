#!/usr/bin/python3
# -*- coding: utf-8 -*-

# -------------------------------------------------
#   @File_Name： usualaddress.py
#   @Author：    YanYi
#   @contact：   18874832147@163.com
#   @date：      2018/11/13 15:50
#   @version：   1.0
# -------------------------------------------------
#   @Description :
#
#
# -------------------------------------------------


def getaddress():
    """
    @api {post} /map/usualaddress/getaddress 获取常用地址
    @apiVersion 1.0.0
    @apiGroup Usualaddress
    @apiDescription 获取常用地址

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiSuccess (Success) {String}  address 地址
    @apiSuccess (Success) {String}  poi_id  poi_id
    @apiSuccess (Success) {String}  type  类型

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "address": "昌吉路224-2号",
                "poi_id": "B00155Q9XG",
                "type": 1
            },
            {
                "address": "安亭镇光明村泰海路230号",
                "poi_id": "B00155HDR1",
                "type": 2
            }
        ],
        "req_id": "r_a7c6609a7a8648e0ade873fb97b6c24b",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    """


def addhomeaddress():
    """
    @api {post} /map/usualaddress/addhomeaddress 增加家地址
    @apiVersion 1.0.0
    @apiGroup Usualaddress
    @apiDescription 增加家地址

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} poi_id poi_id
    @apiParam (Body) {String} address 地址

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_a2b05d090d3b456d96612e95dee825e3",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    @apiError (Error) 21030 poi_id or address could not be both empty

    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21030",
            "msg": "poi_id or address could not be both empty"
        },
        "req_id": "r_8cdd6b30180449c9ae1a04356c96c4c2"
    }
    """


def addcompanyaddress():
    """
    @api {post} /map/usualaddress/addcompanyaddress 增加公司地址
    @apiVersion 1.0.0
    @apiGroup Usualaddress
    @apiDescription 增加公司地址

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} poi_id poi_id
    @apiParam (Body) {String} address 地址

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_072b4de35d46436d86f6eb3d8daaf51e",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    @apiError (Error) 21030 poi_id or address could not be both empty

    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21030",
            "msg": "poi_id or address could not be both empty"
        },
        "req_id": "r_8cdd6b30180449c9ae1a04356c96c4c2"
    }
    """


def delhomeaddress():
    """
    @api {post} /map/usualaddress/delhomeaddress 删除家地址
    @apiVersion 1.0.0
    @apiGroup Usualaddress
    @apiDescription 删除家地址

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiErrorExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_1e51fbca4eaa4ec4b7c7d572c4bad453",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    """


def delcompanyaddress():
    """
    @api {post} /map/usualaddress/delcompanyaddress 删除公司地址
    @apiVersion 1.0.0
    @apiGroup Usualaddress
    @apiDescription 删除公司地址

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiErrorExample {json} Success-Response:
    {
        "data": "Success.",
        "req_id": "r_1e51fbca4eaa4ec4b7c7d572c4bad453",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    """
