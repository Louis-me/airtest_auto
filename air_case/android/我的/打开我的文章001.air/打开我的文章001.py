# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *
import sys

# 得到绝对路径
abs_path = os.path.abspath(os.path.dirname(__file__))
# 得到公共用例目录
common_path = os.path.join(abs_path.split("airtest_auto")[0], "airtest_auto", "util")
sys.path.append(common_path)
from app_util import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


def operate():
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    try:
        # 初始化用例
        init_app()
        poco(text="取消").click() if poco(text="取消").exists() else print("")
        # 点击我的
        poco("com.jianshu.haruki:id/tv_more_menu").wait(5).click()
        # 点击我的文章
        poco(text="我的文章").wait(5).click()
        # 向上滑动
        poco("com.jianshu.haruki:id/refresh_view").focus([0.5, 0.5]).swipe([0.5, -0.5])
    except Exception as e:
        snapshot(msg="报错后截图")
        raise e


operate()
