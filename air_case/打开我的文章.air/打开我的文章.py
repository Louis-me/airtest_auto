# -*- encoding=utf8 -*-
__author__ = "Administrator"
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from util.app_util import *


def operate():
    try:
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        init_app()
        # 点击我的
        poco("com.jianshu.haruki:id/tv_more_menu").click()
        # 点击我的文章
        poco(text="我的文章").click()
        # 向上滑动
        poco("com.jianshu.haruki:id/refresh_view").focus([0.5, 0.5]).swipe([0.5, -0.5])
    except Exception as e:
        snapshot(msg="报错后截图")
        raise e


operate()
