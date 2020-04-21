# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)

start_app("com.jianshu.haruki")
poco("com.jianshu.haruki:id/tab_subscribe").click()
poco("com.jianshu.haruki:id/follow_list_recyclerView").click()
stop_app("com.jianshu.haruki")
           