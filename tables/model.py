# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/5 10:07
"""

from tables import Base, engine
from sqlalchemy import Column, Integer, String, TEXT


class Result(Base):
    __tablename__ = 't_result'
    id = Column(Integer, primary_key=True)
    modules = Column(String(255), comment="测试模块")
    total_time = Column(String(255), comment="总耗时")
    data = Column(TEXT, comment="用例结果")
    dev = Column(String(100), comment="设备名字")


Base.metadata.create_all(engine)
