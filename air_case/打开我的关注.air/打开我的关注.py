# -*- encoding=utf8 -*-
from util.app_util import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


def operate():
    try:
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        init_app()
        # 点击我的关注
        poco("com.jianshu.haruki:id/tv_guanzhu").click()
        # 点击动态下最近更新的作者第一条数据
        poco("com.jianshu.haruki:id/userIcon").click()

    except Exception as e:
        snapshot(msg="报错后截图")
        raise e


operate()
