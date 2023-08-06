#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-12 下午3:47
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : search
# @Contact : guangze.yu@foxmail.com
"""


def poisearch():
    """
    @api {post} /map/search/poisearch poi搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription poi搜索

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} keywords 关键字
    @apiParam (Body) {String} page 页数
    @apiParam (Body) {String} location 经纬度

    @apiSuccess (Success) {Int}  count 总条数
    @apiSuccess (Success) {Object[]} pois 搜索POI信息列表
    @apiSuccess (Success) {String} pois.distance 离中心点距离
    @apiSuccess (Success) {String} pois.pcode poi所在省份编码
    @apiSuccess (Success) {String[]} pois.biz_ext 深度信息
    @apiSuccess (Success) {String} pois.biz_ext.cost 人均消费
    @apiSuccess (Success) {String} pois.biz_ext.rating 评分
    @apiSuccess (Success) {String} pois.importance 重要性
    @apiSuccess (Success) {String} pois.recommend 推荐
    @apiSuccess (Success) {String} pois.type 兴趣点类型
    @apiSuccess (Success) {String[]} pois.photos 照片相关信息
    @apiSuccess (Success) {String} pois.photos.title 图片介绍
    @apiSuccess (Success) {String} pois.photos.url 具体链接
    @apiSuccess (Success) {String} pois.discount_num 优惠信息数目
    @apiSuccess (Success) {String} pois.gridcode 地理格ID
    @apiSuccess (Success) {String} pois.poiweight poi权重
    @apiSuccess (Success) {String} pois.shopinfo 商店信息
    @apiSuccess (Success) {String} pois.typecode 兴趣点类型编码
    @apiSuccess (Success) {String} pois.adname 区域名称
    @apiSuccess (Success) {String} pois.citycode 城市编码
    @apiSuccess (Success) {String} pois.children  	是否按照层级展示子POI数据
    @apiSuccess (Success) {String} pois.alias 别名
    @apiSuccess (Success) {String} pois.tel 该POI的电话
    @apiSuccess (Success) {String} pois.id 唯一ID
    @apiSuccess (Success) {String} pois.tag  该POI的特色内容
    @apiSuccess (Success) {String} pois.event
    @apiSuccess (Success) {String} pois.entr_location 入口经纬度
    @apiSuccess (Success) {String} pois.indoor_map 是否有室内地图标志
    @apiSuccess (Success) {String} pois.email 该POI的电子邮箱
    @apiSuccess (Success) {String} pois.timestamp 印时戳
    @apiSuccess (Success) {String} pois.website 该POI的网址
    @apiSuccess (Success) {String} pois.address 地址
    @apiSuccess (Success) {String} pois.adcode 区域编码
    @apiSuccess (Success) {String} pois.pname poi所在省份名称
    @apiSuccess (Success) {String} pois.biz_type 行业类型
    @apiSuccess (Success) {String} pois.cityname 城市名
    @apiSuccess (Success) {String} pois.match
    @apiSuccess (Success) {String} pois.postcode 邮编
    @apiSuccess (Success) {String} pois.business_area 所在商圈
    @apiSuccess (Success) {Object} pois.indoor_data 室内地图相关数据
    @apiSuccess (Success) {String} pois.indoor_data.cmsid
    @apiSuccess (Success) {String} pois.indoor_data.truefloor 所在楼层
    @apiSuccess (Success) {String} pois.indoor_data.cpid 当前POI的父级POI
    @apiSuccess (Success) {String} pois.indoor_data.floor 楼层索引
    @apiSuccess (Success) {String} pois.sqtype 类型(poi\关键字)
    @apiSuccess (Success) {String} pois.exit_location 出口经纬度
    @apiSuccess (Success) {String} pois.name 名称
    @apiSuccess (Success) {String} pois.location 经纬度
    @apiSuccess (Success) {String} pois.shopid 商店id
    @apiSuccess (Success) {String} pois.navi_poiid 地图编号
    @apiSuccess (Success) {String} pois.groupbuy_num 团购数据

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "count": 100,
            "pois": [{
                "distance": "2035",
                "pcode": "310000",
                "biz_ext": {
                    "cost": "7.00",
                    "rating": ""
                },
                "importance": "",
                "recommend": "0",
                "type": "汽车服务;加油站;中国石化",
                "photos": [{
                    "title": "",
                    "url": "http://store.is.autonavi.com/showpic/71666921fe9a22e260cc5aa1fd79bf11"
                }],
                "discount_num": "0",
                "gridcode": "4621713701",
                "poiweight": "",
                "shopinfo": "0",
                "typecode": "010101",
                "adname": "嘉定区",
                "citycode": "021",
                "children": "",
                "alias": "",
                "tel": "021-59596307;021-59596305",
                "id": "B00155HDQT",
                "tag": "",
                "event": "",
                "entr_location": "",
                "indoor_map": "0",
                "email": "",
                "timestamp": "",
                "website": "",
                "address": "曹安公路4680号,黄沈村委会附近",
                "adcode": "310114",
                "pname": "上海市",
                "biz_type": "",
                "cityname": "上海市",
                "match": "0",
                "postcode": "",
                "business_area": "黄渡",
                "indoor_data": {
                    "cmsid": "",
                    "truefloor": "",
                    "cpid": "",
                    "floor": ""
                },
                "sqtype": "POI",
                "exit_location": "",
                "name": "中国石化加油站",
                "location": "121.218745,31.277413",
                "shopid": "",
                "navi_poiid": "H51F009010_22224",
                "groupbuy_num": "0"
            }]
        },
        "req_id": "r_d43e8ce8102248a3a268a3b9cfa35481",
        "err_resp": {
            "code": "0",
            "msg": null
        }
     }

    @apiError (Error) 21003  No keyword in the request params
    @apiErrorExample {json} Error-Response:
    {
        "err_resp": {
            "code": "21003",
            "msg": "No keyword in the request params!"
            },
        "req_id": "r_e4a3fe57fa8045b1afb668254fd66601"
    }
    """


def unionsearch():
    """
    @api {post} /map/search/unionsearch 关键字搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 关键字搜索

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} keywords 关键字
    @apiParam (Body) {String} page 页数
    @apiParam (Body) {String} location 经纬度

    @apiSuccess (keywords) {Int}  count 总条数
    @apiSuccess (keywords) {Object[]} pois 搜索POI信息列表
    @apiSuccess (keywords) {String}  pois.keywords 关键字
    @apiSuccess (keywords) {String}  pois.sqtype 类型
    @apiSuccess (keywords) {String}  pois.time 时间

    @apiSuccessExample {json} Success-Response(KEYWORD):
    {
        "data": {
            "count": 101,
            "pois": [
                {
                    "keywords": "加油站",
                    "sqtype": "KEYWORD",
                    "time": "2018-07-17 10:10:39"
                },
            ]
        }
    }

    @apiSuccess (poi) {Int}  count 总条数
    @apiSuccess (poi) {Object[]} pois 搜索POI信息列表
    @apiSuccess (poi) {String} pois.distance 离中心点距离
    @apiSuccess (poi) {String} pois.pcode poi所在省份编码
    @apiSuccess (poi) {String[]} pois.biz_ext 深度信息
    @apiSuccess (poi) {String} pois.biz_ext.cost 人均消费
    @apiSuccess (poi) {String} pois.biz_ext.rating 评分
    @apiSuccess (poi) {String} pois.importance 重要性
    @apiSuccess (poi) {String} pois.recommend 推荐
    @apiSuccess (poi) {String} pois.type 兴趣点类型
    @apiSuccess (poi) {String[]} pois.photos 照片相关信息
    @apiSuccess (poi) {String} pois.photos.title 图片介绍
    @apiSuccess (poi) {String} pois.photos.url 具体链接
    @apiSuccess (poi) {String} pois.discount_num 优惠信息数目
    @apiSuccess (poi) {String} pois.gridcode 地理格ID
    @apiSuccess (poi) {String} pois.poiweight poi权重
    @apiSuccess (poi) {String} pois.shopinfo 商店信息
    @apiSuccess (poi) {String} pois.typecode 兴趣点类型编码
    @apiSuccess (poi) {String} pois.adname 区域名称
    @apiSuccess (poi) {String} pois.citycode 城市编码
    @apiSuccess (poi) {String} pois.children  	是否按照层级展示子POI数据
    @apiSuccess (poi) {String} pois.alias 别名
    @apiSuccess (poi) {String} pois.tel 该POI的电话
    @apiSuccess (poi) {String} pois.id 唯一ID
    @apiSuccess (poi) {String} pois.tag  该POI的特色内容
    @apiSuccess (poi) {String} pois.event
    @apiSuccess (poi) {String} pois.entr_location 入口经纬度
    @apiSuccess (poi) {String} pois.indoor_map 是否有室内地图标志
    @apiSuccess (poi) {String} pois.email 该POI的电子邮箱
    @apiSuccess (poi) {String} pois.timestamp 印时戳
    @apiSuccess (poi) {String} pois.website 该POI的网址
    @apiSuccess (poi) {String} pois.address 地址
    @apiSuccess (poi) {String} pois.adcode 区域编码
    @apiSuccess (poi) {String} pois.pname poi所在省份名称
    @apiSuccess (poi) {String} pois.biz_type 行业类型
    @apiSuccess (poi) {String} pois.cityname 城市名
    @apiSuccess (poi) {String} pois.match
    @apiSuccess (poi) {String} pois.postcode 邮编
    @apiSuccess (poi) {String} pois.business_area 所在商圈
    @apiSuccess (poi) {Object} pois.indoor_data 室内地图相关数据
    @apiSuccess (poi) {String} pois.indoor_data.cmsid
    @apiSuccess (poi) {String} pois.indoor_data.truefloor 所在楼层
    @apiSuccess (poi) {String} pois.indoor_data.cpid 当前POI的父级POI
    @apiSuccess (poi) {String} pois.indoor_data.floor 楼层索引
    @apiSuccess (poi) {String} pois.sqtype 类型(poi\关键字)
    @apiSuccess (poi) {String} pois.exit_location 出口经纬度
    @apiSuccess (poi) {String} pois.name 名称
    @apiSuccess (poi) {String} pois.location 经纬度
    @apiSuccess (poi) {String} pois.shopid 商店id
    @apiSuccess (poi) {String} pois.navi_poiid 地图编号
    @apiSuccess (poi) {String} pois.groupbuy_num 团购数据

    @apiSuccessExample {json} Success-Response(POI):
    {
        "data": {
            "count": 101,
            "pois": [
                {
                    "distance": "13382",
                    "pcode": "310000",
                    "biz_ext": {
                        "cost": "",
                        "rating": ""
                    },
                    "importance": "",
                    "recommend": "0",
                    "type": "汽车服务;加油站;中国石化",
                    "photos": [
                        {
                            "title": "",
                            "url": "http://store.is.autonavi.com/showpic/4c0d69996f7e02b6163a22436e1f0bd5"
                        }
                    ],
                    "discount_num": "0",
                    "gridcode": "4621620121",
                    "poiweight": "",
                    "shopinfo": "0",
                    "typecode": "010101",
                    "adname": "青浦区",
                    "citycode": "021",
                    "children": "",
                    "alias": "",
                    "tel": "021-69762496",
                    "id": "B001536995",
                    "tag": "",
                    "event": "",
                    "entr_location": "",
                    "indoor_map": "0",
                    "email": "",
                    "timestamp": "",
                    "website": "",
                    "address": "明珠路420号",
                    "adcode": "310118",
                    "pname": "上海市",
                    "biz_type": "",
                    "cityname": "上海市",
                    "match": "0",
                    "postcode": "",
                    "business_area": "徐泾",
                    "indoor_data": {
                        "cmsid": "",
                        "truefloor": "",
                        "cpid": "",
                        "floor": ""
                    },
                    "sqtype": "POI",
                    "exit_location": "",
                    "name": "中国石化云珠加油站",
                    "location": "121.268183,31.173664",
                    "shopid": "",
                    "navi_poiid": "H51F010011_325538",
                    "groupbuy_num": "0"
                }
            ]
        },
        "req_id": "r_84682d8dd5a04895bb60fd60a8fedbb2",
        "err_resp": {
            "code": "0",
            "msg": null
         }
    }

    @apiError (Error) 21003 No keyword in the request params

    @apiErrorExample {json} Error-Response:
    {
    "err_resp": {
        "code": "21003",
        "msg": "No keyword in the request params!"
        },
    "req_id": "r_be0adaf4b16240838cb4f7e4c414bdf1"
    }
    """


def locationaddress():
    """
    @api {post} /map/search/locationaddress 经纬度周边推荐
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 经纬度周边推荐

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} location 经纬度

    @apiSuccess (Success)  {String}  address poi地址信息
    @apiSuccess (Success)  {String}  location 坐标点
    @apiSuccess (Success)  {Object[]} pois 搜索POI信息列表
    @apiSuccess (Success)  {String}  pois.poiweight poi权重
    @apiSuccess (Success)  {String}  pois.businessarea poi所在商圈名称
    @apiSuccess (Success)  {String}  pois.address poi地址信息
    @apiSuccess (Success)  {String}  pois.distance 门牌地址到请求坐标的距离
    @apiSuccess (Success)  {String}  pois.name poi点名称
    @apiSuccess (Success)  {String}  pois.tel 电话
    @apiSuccess (Success)  {String}  pois.location 坐标点
    @apiSuccess (Success)  {String}  pois.id poi的id
    @apiSuccess (Success)  {String}  pois.type poi类型
    @apiSuccess (Success)  {String}  pois.direction 方向


    @apiSuccessExample {json} Success-Response(POI):
    {
        "data": {
            "address": "上海市嘉定区安亭镇博园路6829号",
            "location": "121.188369,31.2746047",
            "pois": [
                {
                    "poiweight": "0.35579",
                    "businessarea": "安亭",
                    "address": "博园路6555号",
                    "distance": "558.792",
                    "name": "颖奕安亭高尔夫俱乐部",
                    "tel": "021-69502706;021-60568888",
                    "location": "121.188892,31.269316",
                    "id": "B0015588I6",
                    "type": "体育休闲服务;高尔夫相关;高尔夫球场",
                    "direction": "南"
                }
                ]
        },
        "req_id": "r_b7e40568dcf24b40b3aef9b8f215a37a",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }

    @apiError (Error) 21003 No keyword in the request params

    @apiErrorExample {json} Error-Response:
    {
    "err_resp": {
        "code": "21003",
        "msg": "No keyword in the request params!"
        },
    "req_id": "r_3c435785d76946ea82b009b366c23c09"
    }
    """


def iddetail():
    """
    @api {post} /map/search/iddetail poi详情
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription poi详情

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiParam (Body) {String} poi_id poi_id
    @apiParam (Body) {String} location 经纬度

    @apiSuccess (Success) {String} distance 离中心点距离
    @apiSuccess (Success) {String} pcode poi所在省份编码
    @apiSuccess (Success) {String[]} biz_ext 深度信息
    @apiSuccess (Success) {String} biz_ext.cost 人均消费
    @apiSuccess (Success) {String} biz_ext.rating 评分
    @apiSuccess (Success) {String} importance 重要性
    @apiSuccess (Success) {String} recommend 推荐
    @apiSuccess (Success) {String} type 兴趣点类型
    @apiSuccess (Success) {String[]} photos 照片相关信息
    @apiSuccess (Success) {String} photos.title 图片介绍
    @apiSuccess (Success) {String} photos.url 具体链接
    @apiSuccess (Success) {String} discount_num 优惠信息数目
    @apiSuccess (Success) {String} gridcode 地理格ID
    @apiSuccess (Success) {String} poiweight poi权重
    @apiSuccess (Success) {String} shopinfo 商店信息
    @apiSuccess (Success) {String} typecode 兴趣点类型编码
    @apiSuccess (Success) {String} adname 区域名称
    @apiSuccess (Success) {String} citycode 城市编码
    @apiSuccess (Success) {String} children  	是否按照层级展示子POI数据
    @apiSuccess (Success) {String} alias 别名
    @apiSuccess (Success) {String} tel 该POI的电话
    @apiSuccess (Success) {String} id 唯一ID
    @apiSuccess (Success) {String} tag  该POI的特色内容
    @apiSuccess (Success) {String} event
    @apiSuccess (Success) {String} entr_location 入口经纬度
    @apiSuccess (Success) {String} indoor_map 是否有室内地图标志
    @apiSuccess (Success) {String} email 该POI的电子邮箱
    @apiSuccess (Success) {String} timestamp 印时戳
    @apiSuccess (Success) {String} website 该POI的网址
    @apiSuccess (Success) {String} address 地址
    @apiSuccess (Success) {String} adcode 区域编码
    @apiSuccess (Success) {String} pname poi所在省份名称
    @apiSuccess (Success) {String} biz_type 行业类型
    @apiSuccess (Success) {String} cityname 城市名
    @apiSuccess (Success) {String} match
    @apiSuccess (Success) {String} postcode 邮编
    @apiSuccess (Success) {String} business_area 所在商圈
    @apiSuccess (Success) {Object} indoor_data 室内地图相关数据
    @apiSuccess (Success) {String} indoor_data.cmsid
    @apiSuccess (Success) {String} indoor_data.truefloor 所在楼层
    @apiSuccess (Success) {String} indoor_data.cpid 当前POI的父级POI
    @apiSuccess (Success) {String} indoor_data.floor 楼层索引
    @apiSuccess (Success) {String} sqtype 类型(poi\关键字)
    @apiSuccess (Success) {String} exit_location 出口经纬度
    @apiSuccess (Success) {String} name 名称
    @apiSuccess (Success) {String} location 经纬度
    @apiSuccess (Success) {String} shopid 商店id
    @apiSuccess (Success) {String} navi_poiid 地图编号
    @apiSuccess (Success) {String} groupbuy_num 团购数据

    @apiSuccessExample {json} Success-Response(POI):
    {
        "data": [
            {
                "distance": "",
                "pcode": "310000",
                "importance": "",
                "biz_ext": {
                    "cost": "",
                    "rating": "3.5"
                },
                "recommend": "0",
                "type": "体育休闲服务;高尔夫相关;高尔夫球场",
                "photos": [
                    {
                        "title": "",
                        "url": "http://store.is.autonavi.com/showpic/bb1cf027c74966a47b6d86199d9bc29f"
                    },
                    {
                        "title": "",
                        "url": "http://store.is.autonavi.com/showpic/9d47982c1a8afd5e02041c475eba4753"
                    },
                    {
                        "title": "",
                        "url": "http://store.is.autonavi.com/showpic/a65906660dc3bd9dd2e4860b921d03d5"
                    }
                ],
                "discount_num": "0",
                "gridcode": "4621712500",
                "typecode": "080201",
                "shopinfo": "0",
                "poiweight": "",
                "deep_info": {
                    "deepsrc": ""
                },
                "citycode": "021",
                "adname": "嘉定区",
                "indoor_src": "",
                "children": "",
                "tel": "021-69502706;021-60568888",
                "id": "B0015588I6",
                "tag": "",
                "event": "",
                "entr_location": "121.192514,31.273428",
                "indoor_map": "0",
                "email": "",
                "timestamp": "",
                "website": "www.enhancegolf.com",
                "address": "博园路6555号",
                "adcode": "310114",
                "pname": "上海市",
                "biz_type": "",
                "cityname": "上海市",
                "postcode": "",
                "match": "0",
                "business_area": "",
                "indoor_data": {
                    "cmsid": "",
                    "truefloor": "",
                    "cpid": "",
                    "floor": ""
                },
                "rich_content": "",
                "exit_location": "",
                "name": "颖奕安亭高尔夫俱乐部",
                "location": "121.188892,31.269316",
                "shopid": "",
                "navi_poiid": "H51F009010_1389",
                "groupbuy_num": "0"
            }
         ],
        "req_id": "r_5f6f66881bfa4e8ebe49a76988e9818c",
        "err_resp": {
            "code": "0",
            "msg": null
        }
    }
    @apiError (Error) 21003 No keyword in the request params

    @apiErrorExample {json} Error-Response:
    {
    "err_resp": {
        "code": "21003",
        "msg": "No keyword in the request params!"
        },
    "req_id": "r_3c435785d76946ea82b009b366c23c09"
    }
    """
