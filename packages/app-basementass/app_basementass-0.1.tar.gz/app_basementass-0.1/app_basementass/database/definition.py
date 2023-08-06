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
from sqlalchemy import Column, String, Integer, create_engine, DateTime
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


class Trace(BASE):
    __tablename__ = 'tb_trace'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    location = Column(String(255))


a = Connect()
a.data_base_init()
