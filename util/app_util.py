#!/usr/bin/env python
# -*- coding=utf-8 -*-
__CreateAt__ = '2020/6/9-21:39'

from airtest.core.api import *
import yaml
from datetime import datetime

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from read_ini import ReadIni


def init_app():
    """
    初始化数据,根据需求来定制
    :return:
    """

    path = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    ini_path = path("../config/setting1.ini")
    pkg = ReadIni(ini_path).get_pkg()
    auto_setup(__file__)
    # end_mp4()
    # start_mp4()
    stop_app(pkg)
    sleep(2)
    start_app(pkg)

def end_mp4():
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    start_app("com.netease.nie.yosemite")
    if poco(text="结束录屏").exists():
        print("结束录屏")
        poco(text="结束录屏").click()
    stop_app("com.netease.nie.yosemite")


def start_mp4():
    stop_app("com.netease.nie.yosemite")
    start_app("com.netease.nie.yosemite")
    sleep(2)
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

    if poco("com.android.systemui:id/remember").exists():
        poco("com.android.systemui:id/remember").click()
    if poco(text="确定").exists():
        poco(text="确定").click()

    if poco("android:id/button1").exists():
        poco("android:id/button1").click()
    if poco(text="开始录屏").exists():
        print("开始录屏")
        poco(text="开始录屏").click()


def operate_test_case(poco, yml):
    """
    读取yml用例文件,执行用例
    :param poco:
    :param yml:
    :return:
    """
    handing_error(poco)
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
            eval(event_click[0] + ".wait_for_appearance(5)")
            # 执行用例
            eval(i)
        else:
            # 其他的poco事件
            sleep(2)
            eval(i)
        print("操作元素结束时间：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # 操作元素后的容错
        handing_error(poco)


def handing_error(poco):
    """
    容错处理
    :param poco:
    :return:
    """
    if poco(textMatches="^跳过.*$").exists():
        poco(textMatches="^跳过.*").click()
    # 自定义容错处理,比如系统的授权
    for j in ["我知道了", "始终运行"]:
        if poco(text=j).exists():
            # package = poco(text=j).attr("package")
            # # 只容错非测试应用包的数据
            # if package.find("jianshu") < 0:
            poco(text=j).click()
            print("进入第一次容错")
            sleep(2)
init_app()