#!/usr/bin/env python
# -*- coding=utf-8 -*-
__CreateAt__ = '2020/6/9-21:39'

from airtest.core.api import *
import yaml
from datetime import datetime


def init_app(extend={}):
    """
    初始化数据,根据需求来定制
    :param extend:
    :return:
    """
    auto_setup(__file__)
    if extend.get("poco"):
        print("====进入操作yousemite=======")
        poco = extend["poco"]
        start_app("com.netease.nie.yosemite")
        sleep(2)
        if poco("com.android.systemui:id/remember").exists():
            poco("com.android.systemui:id/remember").click()
        if poco(text="确定").exists():
            poco(text="确定").click()

        if poco("android:id/button1").exists():
            poco("android:id/button1").click()
    stop_app("com.jianshu.haruki")
    sleep(2)
    start_app("com.jianshu.haruki")


def destory(extend={}):
    """
    用例结束后的其他操作
    :param extend:
    :return:
    """
    stop_app("com.netease.nie.yosemite")


def operate_test_case(poco, yml):
    """
    读取yml用例文件,执行用例
    :param poco:
    :param yml:
    :return:
    """
    # handing_error(poco)
    skip_adv(poco)
    with open(yml, encoding='utf-8') as f:
        d = yaml.safe_load(f)
    # 启动应用后的容错
    for i in d:
        event_click = i.split(".click()")
        event_if = i.split("if")
        print("元素为：%s" % i)
        print("操作元素开始时间：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # 非if语句的click事件
        if len(event_click) > 1 and len(event_if) == 1:
            # 智能等待
            eval(event_click[0] + ".wait_for_appearance(60)")
            # 执行用例
            eval(i)
        else:
            # 其他的poco事件
            sleep(2)
            eval(i)
        print("操作元素结束时间：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # 操作元素后的容错
        handing_error(poco)


def skip_adv(poco):
    """
    跳过广告
    :param poco:
    :return:
    """
    num = 0
    while True:
        sleep(1)
        if poco(textMatches="^.*跳过$").exists():
            poco(textMatches="^.*跳过$").click()
            print("已经点击跳过广告按钮")
            break
        num += 1
        if num > 5:
            print("没有找到跳过广告按钮")
            break


def handing_error(poco):
    """
    容错处理
    :param poco:
    :return:
    """
    # 自定义容错处理,比如系统的授权
    for j in ["我知道了", "始终运行", "取消"]:
        if poco(text=j).exists():
            # package = poco(text=j).attr("package")
            # # 只容错非测试应用包的数据
            # if package.find("jianshu") < 0:
            poco(text=j).click()
            print("进入第一次容错")
            sleep(2)
        for k in ["我知道了", "始终运行", "取消"]:
            if poco(text=j).exists():
                poco(text=k).click()
                print("进入二次容错")
                sleep(2)
