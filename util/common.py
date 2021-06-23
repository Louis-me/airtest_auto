#!/usr/bin/env python
# -*- coding=utf-8 -*-
__CreateAt__ = '2020/4/19-18:31'

import os
from datetime import datetime
import json

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


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


class Runner3Common(object):

    @staticmethod
    def init_result(result_path, case_path):
        """
        初始化记录用例结果的json
        :param result_path: 总结果json
        :param case_path: 单个用例的结果json
        :return:
        """
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump({"modules": "", "data": [], "total_time": "", "dev": ""}, f)
        with open(case_path, "w", encoding="utf-8") as f1:
            json.dump({"test_dev": [], "test_modules": [], "total_time": ""}, f1)

    @classmethod
    def get_case_module_dev(cls, path):
        """
        得到测试用例的设备和模块
        :param path:
        :return:
        """
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())

    @classmethod
    def set_case_module_dev(cls, d):
        """
        设置用例的测试模块和设备
        :param d: {}
        :return:
        """
        path = PATH("../config/case_data.json")
        get_case_j = cls.get_case_module_dev(path)
        for i in get_case_j:
            if d.get(i):
                get_case_j[i].append(d[i])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(get_case_j, f)

    @classmethod
    def get_result_json(cls):
        """
        得到测试用例总结果
        :return:
        """
        path = PATH("../config/result_data.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())

    @classmethod
    def set_result_json(cls, d):
        """
        记录每个用例的数据
        :param path:
        :param d: {}
        :return:
        """
        path = PATH("../config/result_data.json")
        # 先得到之前的结果
        get_res = cls.get_result_json()
        # 记录总结果
        get_res["data"].append(d)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(get_res, f)

    @classmethod
    def set_result_summary_json(cls, d):
        """
        记录测试总数据的模块，设备，耗时
        :param path:
        :param d:
        :return:
        """
        path = PATH("../config/result_data.json")
        get_d = cls.get_result_json()
        get_d["modules"] = d["modules"]
        get_d["dev"] = d["dev"]
        get_d["total_time"] = d["total_time"]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(get_d, f)

    @staticmethod
    def get_cases(data_item, dev, root_path):
        """
        得到用例列表
        :param data_item:
        :param root_path: 用例根目录
        :param dev: 设备序列号
        :return:
        """
        res = []
        if data_item["dev"] == dev:
            # 得到设备的各个模块
            for j in data_item["test_module"]:
                module_case = os.path.isdir(os.path.join(root_path, j))
                # 如果用例模块下文件夹存在
                if module_case:
                    for k in os.listdir(os.path.join(root_path, j)):
                        if k.find(".air") != -1:
                            res.append({"module": j, "case": k})
        if not res:
            print("无测试用例")
        return res


class Runner4Common():

    @staticmethod
    def get_cases(data_item, root_path):
        """
        得到用例列表
        :param data_item:
        :param root_path: 用例根目录
        :return:
        """
        res = []
        # 得到设备的各个模块
        for j in data_item["test_module"]:
            module_case = os.path.isdir(os.path.join(root_path, j))
            # 如果用例模块下文件夹存在
            if module_case:
                for k in os.listdir(os.path.join(root_path, j)):
                    if k.find(".air") != -1:
                        res.append({"module": j, "case": k})
        if not res:
            print("无测试用例")
        return res
