#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os

__author__ = 'shikun'
__CreateAt__ = '2020/4/19-18:31'
import yaml

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def get_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def set_yaml(path, data, model="w"):
    with open(path, mode=model, encoding="utf-8") as f:
        yaml.safe_dump(data, f)


def setting_result(data):
    """
    设置用例结果
    :param data: {} 存放的数据字典
    :return:
    """
    get_d = get_yaml(PATH("../config/result.yaml"))
    get_d["result"].append(data)
    set_yaml(PATH("../config/result.yaml"), get_d, model="a")


def get_test_case(root_dir):
    """
    得到测试用例列表数据
    :return:
    """
    data = {"airs": [], "module_airs": []}
    if os.path.isdir(root_dir):
        script_list = os.listdir(root_dir)
        for i in script_list:
            if i.find("air") != -1:
                data["airs"].append(i)
            elif i != "log":
                module_case = os.path.isdir(os.path.join(root_dir, i))
                if module_case:
                    for j in os.listdir(os.path.join(root_dir, i)):
                        if j.find(".air") != -1:
                            data["module_airs"].append({"module": i, "case": j})

    if data["airs"] or data["module_airs"]:
        print("用例有数据")
        return True, data
    else:
        print("用例无数据")
        return False, {}