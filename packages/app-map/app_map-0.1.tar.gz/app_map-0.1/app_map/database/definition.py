#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/23 下午5:29
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : definition
# @File    : app_map
# @Contact : guangze.yu@foxmail.com
"""
from sqlalchemy import Column, String, Integer, create_engine, TEXT, Boolean, DateTime, FLOAT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config.mysql as cfg

BASE = declarative_base()
CONFIG = cfg.sqlconfig


class Connect:
    def __init__(self, config=CONFIG):
        self.engine = create_engine(config, encoding='utf-8')
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def data_base_init(self):
        # Base.metadata.drop_all(self.engine)
        BASE.metadata.create_all(self.engine)

    def data_base_add(self):
        BASE.metadata.create_all(self.engine)


class Poi(BASE):
    __tablename__ = 'tb_poi'
    index = Column(Integer(), primary_key=True, index=True, unique=True)
    id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    tag = Column(String(255))
    type = Column(String(255))
    typecode = Column(String(255))
    biz_type = Column(String(255))
    address = Column(String(255))
    tel = Column(String(255))
    postcode = Column(String(255))
    website = Column(String(255))
    email = Column(String(255))
    pcode = Column(String(255))
    pname = Column(String(255))
    citycode = Column(String(255))
    cityname = Column(String(255))
    adcode = Column(String(255))
    adname = Column(String(255))
    importance = Column(String(255))
    shopid = Column(String(255))
    shopinfo = Column(String(255))
    poiweight = Column(String(255))
    gridcode = Column(String(255))
    indoor_map = Column(String(255))
    poi_parking_type = Column(String(255))
    used_times = Column(Integer())


class UserInfo(BASE):
    __tablename__ = 'tb_user'
    uid = Column(Integer(), primary_key=True, nullable=False, unique=True)
    name = Column(String(255))
    gender = Column(Integer())
    birth = Column(String(255))
    latitude = Column(String(255))
    # used_poi = relationship('PoiSearchHistory', back_populates="user_poi_list")
    # used_broadcast = relationship('tb_broadcast_history')


class PoiHistory(BASE):
    __tablename__ = 'tb_poi_history'
    index = Column(Integer(), primary_key=True, index=True, unique=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    poi_id = Column(String(255), nullable=False)
    poi_name = Column(String(255), nullable=False)
    poi_type = Column(String(255), nullable=False)
    used_location = Column(String(255))
    valid = Column(Boolean, nullable=False)
    rating = Column(String(200), nullable=True)
    cost = Column(String(200), nullable=True)
    photo_1_title = Column(String(200), nullable=True)
    photo_1 = Column(String(2000), nullable=True)
    photo_2_title = Column(String(200), nullable=True)
    photo_2 = Column(String(2000), nullable=True)
    photo_3_title = Column(String(200), nullable=True)
    photo_3 = Column(String(2000), nullable=True)
    poi_location = Column(String(255), nullable=False)
    type_code = Column(String(200), nullable=True)
    city_code = Column(String(200), nullable=True)
    city_name = Column(String(200), nullable=True)
    tel = Column(String(2000), nullable=True)
    ad_name = Column(String(200), nullable=True)
    ad_code = Column(String(200), nullable=True)
    address = Column(String(200), nullable=True)
    tag = Column(String(2000), nullable=True)

    # user_poi_list = relationship("User", back_populates="used_poi")


class BroadCastHistory(BASE):
    __tablename__ = 'tb_broadcast_history'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    citycode = Column(String(255), nullable=False)
    isbroadcast = Column(Boolean, nullable=False)


class Trace(BASE):
    __tablename__ = 'tb_trace'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    location = Column(String(255))


class BroadCastInfo(BASE):
    __tablename__ = 'tb_broadcast_info'
    index = Column(Integer(), primary_key=True, index=True)
    citycode = Column(String(30))
    adcode = Column(String(30), nullable=False)
    name = Column(String(255), nullable=False)
    level = Column(String(255), nullable=False)
    info = Column(TEXT)


class SearchKeys(BASE):
    __tablename__ = 'tb_searchkeys'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    keywords = Column(String(255), nullable=False)
    valid = Column(Boolean, nullable=False)


class Collect(BASE):
    __tablename__ = 'tb_collect'
    index = Column(Integer(), primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    poi_id = Column(String(255), nullable=False)
    poi_name = Column(String(255), nullable=False)
    type = Column(String(255))
    typecode = Column(String(255), nullable=False)
    citycode = Column(String(255), nullable=False)
    adname = Column(String(255), nullable=False)
    tel = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    adcode = Column(String(255), nullable=False)
    cityname = Column(String(255), nullable=False)
    tag = Column(String(255))
    createtime = Column(DateTime, nullable=False)
    modifiedtime = Column(DateTime, nullable=True)
    valid = Column(Boolean, nullable=False)


class UsualAddress(BASE):
    __tablename__ = 'tb_usual_address'
    index = Column(Integer(), primary_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    poi_id = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    type = Column(Integer(), nullable=False)
    createtime = Column(DateTime, nullable=False)
    modifiedtime = Column(DateTime, nullable=True)
    valid = Column(Boolean, nullable=False)


a = Connect()
a.data_base_init()
