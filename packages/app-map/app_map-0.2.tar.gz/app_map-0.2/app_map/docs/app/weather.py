#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:24
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : weather
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""


def weather_all():
    """
    @api {post} /map/weather/weather_all 全部天气
    @apiVersion 1.0.0
    @apiGroup Weather
    @apiDescription 全部天气

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiSuccess (Success) {Object} basic 基础信息
    @apiSuccess (Success) {String} basic.cid 地区／城市ID
    @apiSuccess (Success) {String} basic.location 地区／城市名称
    @apiSuccess (Success) {String} basic.parent_city 该地区／城市的上级城市
    @apiSuccess (Success) {String} basic.admin_area 该地区／城市所属行政区域
    @apiSuccess (Success) {String} basic.cnty  	该地区／城市所属国家名称
    @apiSuccess (Success) {String} basic.lat 地区／城市纬度
    @apiSuccess (Success) {String} basic.lon 地区／城市经度
    @apiSuccess (Success) {String} basic.tz  	该地区／城市所在时区
    @apiSuccess (Success) {Object} update 接口更新时间
    @apiSuccess (Success) {String} update.loc 当地时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} update.utc UTC时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} status 接口状态
    @apiSuccess (Success) {Object} now 实况天气
    @apiSuccess (Success) {String} now.fl 体感温度，默认单位：摄氏度
    @apiSuccess (Success) {String} now.tmp 温度，默认单位：摄氏度
    @apiSuccess (Success) {String} now.cond_code 实况天气状况代码
    @apiSuccess (Success) {String} now.cond_txt 实况天气状况描述
    @apiSuccess (Success) {String} now.wind_deg 风向360角度
    @apiSuccess (Success) {String} now.wind_dir 风向
    @apiSuccess (Success) {String} now.wind_sc 风力
    @apiSuccess (Success) {String} now.wind_spd 风速，公里/小时
    @apiSuccess (Success) {String} now.hum 相对湿度
    @apiSuccess (Success) {String} now.pcpn 降水量
    @apiSuccess (Success) {String} now.pres 大气压强
    @apiSuccess (Success) {String} now.vis 能见度，默认单位：公里
    @apiSuccess (Success) {String} now.cloud 云量
    @apiSuccess (Success) {Object} daily_forecast 天气预报
    @apiSuccess (Success) {String} daily_forecast.cond_code_d 白天天气状况代码
    @apiSuccess (Success) {String} daily_forecast.cond_code_n 晚间天气状况代码
    @apiSuccess (Success) {String} daily_forecast.cond_txt_d 白天天气状况描述
    @apiSuccess (Success) {String} daily_forecast.cond_txt_n 晚间天气状况描述
    @apiSuccess (Success) {String} daily_forecast.date 预报日期
    @apiSuccess (Success) {String} daily_forecast.hum 相对湿度
    @apiSuccess (Success) {String} daily_forecast.mr 月升时间
    @apiSuccess (Success) {String} daily_forecast.ms 月落时间
    @apiSuccess (Success) {String} daily_forecast.pcpn 降水量
    @apiSuccess (Success) {String} daily_forecast.pop 降水概率
    @apiSuccess (Success) {String} daily_forecast.pres 大气压强
    @apiSuccess (Success) {String} daily_forecast.sr 日出时间
    @apiSuccess (Success) {String} daily_forecast.ss 日落时间
    @apiSuccess (Success) {String} daily_forecast.tmp_max 最高温度
    @apiSuccess (Success) {String} daily_forecast.tmp_min 最低温度
    @apiSuccess (Success) {String} daily_forecast.uv_index 紫外线强度指数
    @apiSuccess (Success) {String} daily_forecast.vis 能见度，单位：公里
    @apiSuccess (Success) {String} daily_forecast.wind_deg 风向360角度
    @apiSuccess (Success) {String} daily_forecast.wind_dir 风向
    @apiSuccess (Success) {String} daily_forecast.wind_sc 风力
    @apiSuccess (Success) {String} daily_forecast.wind_spd 风速，公里/小时
    @apiSuccess (Success) {Object} lifestyle  生活指数
    @apiSuccess (Success) {String} lifestyle.brf 生活指数简介
    @apiSuccess (Success) {String} lifestyle.txt 生活指数详细描述
    @apiSuccess (Success) {String} lifestyle.type 生活指数类型 comf：舒适度指数、cw：洗车指数、drsg：穿衣指数、flu：感冒指数、sport：运动指数、trav：旅游指数、uv：紫外线指数、air：空气污染扩散条件指数、ac：空调开启指数、ag：过敏指数、gl：太阳镜指数、mu：化妆指数、airc：晾晒指数、ptfc：交通指数、fisin：钓鱼指数、spi：防晒指数

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "basic": {
                    "cid": "CN101020500",
                    "location": "嘉定",
                    "parent_city": "上海",
                    "admin_area": "上海",
                    "cnty": "中国",
                    "lat": "31.38352394",
                    "lon": "121.25033569",
                    "tz": "+8.00"
                },
                "update": {
                    "loc": "2018-07-17 14:48",
                    "utc": "2018-07-17 06:48"
                },
                "status": "ok",
                "now": {
                    "cloud": "75",
                    "cond_code": "101",
                    "cond_txt": "多云",
                    "fl": "34",
                    "hum": "55",
                    "pcpn": "0.0",
                    "pres": "1008",
                    "tmp": "33",
                    "vis": "10",
                    "wind_deg": "182",
                    "wind_dir": "南风",
                    "wind_sc": "3",
                    "wind_spd": "16"
                },
                "daily_forecast": [
                    {
                        "cond_code_d": "101",
                        "cond_code_n": "101",
                        "cond_txt_d": "多云",
                        "cond_txt_n": "多云",
                        "date": "2018-07-17",
                        "hum": "75",
                        "mr": "09:24",
                        "ms": "22:20",
                        "pcpn": "0.0",
                        "pop": "1",
                        "pres": "1009",
                        "sr": "05:02",
                        "ss": "18:59",
                        "tmp_max": "34",
                        "tmp_min": "27",
                        "uv_index": "5",
                        "vis": "18",
                        "wind_deg": "134",
                        "wind_dir": "东南风",
                        "wind_sc": "4-5",
                        "wind_spd": "29"
                    }
                ],
                "lifestyle": [
                    {
                        "type": "comf",
                        "brf": "较不舒适",
                        "txt": "白天天气多云，有风，但会感到有些热，不很舒适。"
                    }
                ]
            }
        ]
    }
    """


def forecast():
    """
    @api {post} /map/weather/forecast  10天预报
    @apiVersion 1.0.0
    @apiGroup Weather
    @apiDescription 10天预报

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiSuccess (Success) {Object} basic 基础信息
    @apiSuccess (Success) {String} basic.cid 地区／城市ID
    @apiSuccess (Success) {String} basic.location 地区／城市名称
    @apiSuccess (Success) {String} basic.parent_city 该地区／城市的上级城市
    @apiSuccess (Success) {String} basic.admin_area 该地区／城市所属行政区域
    @apiSuccess (Success) {String} basic.cnty  	该地区／城市所属国家名称
    @apiSuccess (Success) {String} basic.lat 地区／城市纬度
    @apiSuccess (Success) {String} basic.lon 地区／城市经度
    @apiSuccess (Success) {String} basic.tz  	该地区／城市所在时区
    @apiSuccess (Success) {Object} update 接口更新时间
    @apiSuccess (Success) {String} update.loc 当地时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} update.utc UTC时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} status 接口状态
    @apiSuccess (Success) {Object} daily_forecast 天气预报
    @apiSuccess (Success) {String} daily_forecast.cond_code_d 白天天气状况代码
    @apiSuccess (Success) {String} daily_forecast.cond_code_n 晚间天气状况代码
    @apiSuccess (Success) {String} daily_forecast.cond_txt_d 白天天气状况描述
    @apiSuccess (Success) {String} daily_forecast.cond_txt_n 晚间天气状况描述
    @apiSuccess (Success) {String} daily_forecast.date 预报日期
    @apiSuccess (Success) {String} daily_forecast.hum 相对湿度
    @apiSuccess (Success) {String} daily_forecast.mr 月升时间
    @apiSuccess (Success) {String} daily_forecast.ms 月落时间
    @apiSuccess (Success) {String} daily_forecast.pcpn 降水量
    @apiSuccess (Success) {String} daily_forecast.pop 降水概率
    @apiSuccess (Success) {String} daily_forecast.pres 大气压强
    @apiSuccess (Success) {String} daily_forecast.sr 日出时间
    @apiSuccess (Success) {String} daily_forecast.ss 日落时间
    @apiSuccess (Success) {String} daily_forecast.tmp_max 最高温度
    @apiSuccess (Success) {String} daily_forecast.tmp_min 最低温度
    @apiSuccess (Success) {String} daily_forecast.uv_index 紫外线强度指数
    @apiSuccess (Success) {String} daily_forecast.vis 能见度，单位：公里
    @apiSuccess (Success) {String} daily_forecast.wind_deg 风向360角度
    @apiSuccess (Success) {String} daily_forecast.wind_dir 风向
    @apiSuccess (Success) {String} daily_forecast.wind_sc 风力
    @apiSuccess (Success) {String} daily_forecast.wind_spd 风速，公里/小时

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "basic": {
                    "cid": "CN101020500",
                    "location": "嘉定",
                    "parent_city": "上海",
                    "admin_area": "上海",
                    "cnty": "中国",
                    "lat": "31.38352394",
                    "lon": "121.25033569",
                    "tz": "+8.00"
                },
                "update": {
                    "loc": "2018-07-17 13:48",
                    "utc": "2018-07-17 05:48"
                },
                "status": "ok",
                "daily_forecast": [
                    {
                        "cond_code_d": "101",
                        "cond_code_n": "101",
                        "cond_txt_d": "多云",
                        "cond_txt_n": "多云",
                        "date": "2018-07-17",
                        "hum": "75",
                        "mr": "09:24",
                        "ms": "22:20",
                        "pcpn": "0.0",
                        "pop": "1",
                        "pres": "1009",
                        "sr": "05:02",
                        "ss": "18:59",
                        "tmp_max": "34",
                        "tmp_min": "27",
                        "uv_index": "5",
                        "vis": "18",
                        "wind_deg": "157",
                        "wind_dir": "东南风",
                        "wind_sc": "4-5",
                        "wind_spd": "26"
                    }
                ]
            }
        ]
    }
    """


def now():
    """
    @api {post} /map/weather/now实况天气
    @apiVersion 1.0.0
    @apiGroup Weather
    @apiDescription 实况天气

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiSuccess (Success) {Object} basic 基础信息
    @apiSuccess (Success) {String} basic.location 地区／城市名称
    @apiSuccess (Success) {String} basic.cid 地区／城市ID
    @apiSuccess (Success) {String} basic.lat 地区／城市纬度
    @apiSuccess (Success) {String} basic.lon 地区／城市经度
    @apiSuccess (Success) {String} basic.parent_city 该地区／城市的上级城市
    @apiSuccess (Success) {String} basic.admin_area 该地区／城市所属行政区域
    @apiSuccess (Success) {String} basic.cnty 该地区／城市所属国家名称
    @apiSuccess (Success) {String} basic.tz 该地区／城市所在时区
    @apiSuccess (Success) {Object} update 接口更新时间
    @apiSuccess (Success) {String} update.loc 当地时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} update.utc UTC时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} status 接口状态
    @apiSuccess (Success) {Object} now 实况天气
    @apiSuccess (Success) {String} now.fl 体感温度，默认单位：摄氏度
    @apiSuccess (Success) {String} now.tmp 温度，默认单位：摄氏度
    @apiSuccess (Success) {String} now.cond_code 实况天气状况代码
    @apiSuccess (Success) {String} now.cond_txt 实况天气状况描述
    @apiSuccess (Success) {String} now.wind_deg 风向360角度
    @apiSuccess (Success) {String} now.wind_dir 风向
    @apiSuccess (Success) {String} now.wind_sc 风力
    @apiSuccess (Success) {String} now.wind_spd 风速，公里/小时
    @apiSuccess (Success) {String} now.hum 相对湿度
    @apiSuccess (Success) {String} now.pcpn 降水量
    @apiSuccess (Success) {String} now.pres 大气压强
    @apiSuccess (Success) {String} now.vis 能见度，默认单位：公里
    @apiSuccess (Success) {String} now.cloud 云量

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "basic": {
                    "cid": "CN101020500",
                    "location": "嘉定",
                    "parent_city": "上海",
                    "admin_area": "上海",
                    "cnty": "中国",
                    "lat": "31.38352394",
                    "lon": "121.25033569",
                    "tz": "+8.00"
                },
                "update": {
                    "loc": "2018-07-17 13:48",
                    "utc": "2018-07-17 05:48"
                },
                "status": "ok",
                "now": {
                    "cloud": "75",
                    "cond_code": "101",
                    "cond_txt": "多云",
                    "fl": "34",
                    "hum": "53",
                    "pcpn": "0.0",
                    "pres": "1008",
                    "tmp": "33",
                    "vis": "35",
                    "wind_deg": "105",
                    "wind_dir": "东南风",
                    "wind_sc": "3",
                    "wind_spd": "15"
                }
            }
        ]
    }
    """


def air():
    """
    @api {post} /map/weather/air 空气质量数据集合
    @apiVersion 1.0.0
    @apiGroup Weather
    @apiDescription 空气质量数据集合

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    """


def sun_rise_set():
    """
    @api {post} /map/weather/sun_rise_set 日出日落
    @apiVersion 1.0.0
    @apiGroup Weather
    @apiDescription 日出日落

    @apiParam (Headers) {String} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳
    @apiParam (Headers) {String} location 经纬度

    @apiSuccess (Success) {Object} basic 基础信息
    @apiSuccess (Success) {String} basic.location 地区／城市名称
    @apiSuccess (Success) {String} basic.cid 地区／城市ID
    @apiSuccess (Success) {String} basic.lat 地区／城市纬度
    @apiSuccess (Success) {String} basic.lon 地区／城市经度
    @apiSuccess (Success) {String} basic.parent_city 该地区／城市的上级城市
    @apiSuccess (Success) {String} basic.admin_area 该地区／城市所属行政区域
    @apiSuccess (Success) {String} basic.cnty 该地区／城市所属国家名称
    @apiSuccess (Success) {String} basic.tz 该地区／城市所在时区
    @apiSuccess (Success) {Object} update 接口更新时间
    @apiSuccess (Success) {String} update.loc 当地时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} update.utc UTC时间，24小时制，格式yyyy-MM-dd HH:mm
    @apiSuccess (Success) {String} status 接口状态
    @apiSuccess (Success) {Object} SunriseSunset 日出日落
    @apiSuccess (Success) {String} SunriseSunset.date 预报日期
    @apiSuccess (Success) {String} SunriseSunset.sr 日出时间
    @apiSuccess (Success) {String} SunriseSunset.ss 日落时间
    @apiSuccess (Success) {String} SunriseSunset.mr 月升时间
    @apiSuccess (Success) {String} SunriseSunset.ms 月落时间

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "basic": {
                    "cid": "CN101020500",
                    "location": "嘉定",
                    "parent_city": "上海",
                    "admin_area": "上海",
                    "cnty": "中国",
                    "lat": "31.38352394",
                    "lon": "121.25033569",
                    "tz": "+8.00"
                },
                "update": {
                    "loc": "2018-07-17 14:48",
                    "utc": "2018-07-17 06:48"
                },
                "status": "ok",
                "sunrise_sunset": [
                    {
                        "date": "2018-07-17",
                        "mr": "09:24",
                        "ms": "22:20",
                        "sr": "05:02",
                        "ss": "18:59"
                    }
                ]
            }
        ]
    }
    """
