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
        # 得到上级目录
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        # 得到用例名称,用例配置文件一般和用例名字保持一致
        case_name = os.path.basename(__file__).strip(".py") + ".yml"
        # 得到用例目录
        case_path = os.path.join(path, "yml", case_name)
        # 执行用例
        operate_test_case(poco, case_path)
    except Exception as e:
        snapshot(msg="报错后截图")
        raise e


operate()
