#!/usr/bin/env python
# -*- coding=utf-8 -*-
__CreateAt__ = '2020/4/19-18:31'

import os
from datetime import datetime


def get_test_case(data):
    if data["test_plan"] == 1:
        res = []
        for i in data["test_module"]:
            if os.path.isdir(os.path.join(data["root_path"], i)):
                script_list = os.listdir(os.path.join(data["root_path"], i))
                for j in script_list:
                    if j.find(".air") != -1:
                        res.append({"module": i, "case": j})
        return res
    elif data["test_plan"] == 0:
        res = []
        if os.path.join(data["root_path"]):
            script_list = os.listdir(data["root_path"])
            for i in script_list:
                module_case = os.path.isdir(os.path.join(data["root_path"], i))
                if module_case:
                    for j in os.listdir(os.path.join(data["root_path"], i)):
                        if j.find(".air") != -1:
                            res.append({"module": i, "case": j})
        return res


def get_test_case_runner2(data):
    if data["test_plan"] == 1:
        return data["test_data"]
    elif data["test_plan"] == 0:
        res = []
        if os.path.join(data["root_path"]):
            script_list = os.listdir(data["root_path"])
            for i in script_list:
                if i.find(".air") != -1:
                    res.append(i)
        return res


def get_case_total_time(start_time, end_time):
    """
    得到用例的总耗时
    :param start_time:  datetime.now().strftime("%H:%M:%S")
    :param end_time:
    :return:
    """
    formats = "%H:%M:%S"
    total_time = datetime.strptime(end_time, formats) - datetime.strptime(start_time, formats)
    return str(total_time)


def get_test_modules(modules):
    """
    得到测试模块
    :param modules: list
    :return:
    """
    modules_s = ""
    for i in set(modules):
        modules_s = modules_s + i + ","
    # 记录测试模块
    return modules_s.rstrip(",")
