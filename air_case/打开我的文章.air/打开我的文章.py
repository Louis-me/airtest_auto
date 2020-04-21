# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)

start_app("com.jianshu.haruki")
poco("com.jianshu.haruki:id/tab_mine").click()
poco("com.jianshu.haruki:id/user_mine_article").click()
stop_app("com.jianshu.haruki")