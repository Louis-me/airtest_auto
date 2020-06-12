#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2020/6/9-21:39'
from airtest.core.api import *
import yaml


def init_app(extend=None):
    """
    初始化数据,根据需求来定制
    :param extend:
    :return:
    """
    auto_setup(__file__)
    stop_app("com.jianshu.haruki")
    start_app("com.jianshu.haruki")


def operate_test_case(poco, yml):
    """
    读取yml用例文件,执行用例
    :param poco:
    :param yml:
    :return:
    """
    with open(yml, encoding='utf-8') as f:
        d = yaml.safe_load(f)
    # 启动应用后的容错
    handing_error(poco)
    for i in d:
        event = i.split(".click()")
        # 如果是点击
        if len(event) > 1:
            # 智能等待
            eval(event[0] + ".wait_for_appearance(60)")
        # 执行用例
        eval(i)
        # 操作元素后的容错
        handing_error(poco)


def handing_error(poco):
    """
    容错处理
    :param poco:
    :return:
    """
    # 自定义容错处理,比如系统的授权
    for j in ["跳过广告", "我知道了", "始终运行"]:
        if poco(text=j).exists():
            # package = poco(text=j).attr("package")
            # # 只容错非测试应用包的数据
            # if package.find("jianshu") < 0:
            poco(text=j).click()
            print("进入了容错")
            sleep(2)
