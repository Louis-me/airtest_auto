#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2020/4/19-18:31'
import yaml
import os
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


def init_data():
    set_yaml(PATH("../config/result.yaml"), {"result": []})


def get_test_case(root_dir, run_model):
    """
    得到测试用例列表数据
    : run_model: 0执行全部用例|1执行调试用例，数据来源为debug.yaml|2执行失败用例,数据来源fail.yaml
    :return:
    """
    print(run_model)
    if run_model == 0:
        data = []
        for f in os.listdir(root_dir):
            if f.endswith(".air"):
                data.append(f)
        if  len(data) > 0:
            print("执行全部用例===用例有数据")
        else:
            print("执行全部用例===用例无数据")
        return data
    elif run_model == 1:
        data = get_yaml(PATH("../config/debug.yaml"))
        if len(data) > 0:
            print("执行调试用例===用例有数据")
        else:
            print("执行调试用例==用例无法数据")
        return data
    elif run_model == 2:
        data = get_yaml(PATH("../config/fail.yaml"))
        if  len(data) > 0:
            print("执行失败用例===用例有数据")
        else:
            print("执行失败用例==用例无法数据")
        return data
    else:
        print("请传入正确的运行模式")
        return []
