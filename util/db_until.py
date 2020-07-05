# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/5 10:12
"""

from tables.model import *
from tables import Session


def init_result():
    session = Session()
    entry = Session(Result).filter(Result.id == 1).one_or_none()
    # 如数据不存在，就新增一条为1的空数据
    if not entry:
        session.add(Result(modules="", total_time="", data="", dev=""))
        session.commit()
    else:
        pass
    session.close()


def set_result(data):
    session = Session()
    entry = Session(Result).filter(Result.id == data["id"]).one_or_none()
    if entry:
        entry.modules = data["modules"]
        entry.total_time = data["total_time"]
        entry.data = data["data"]
        entry.dev = data["dev"]
        session.commit()
    else:
        print("实体类不存在")
    session.close()
