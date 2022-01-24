# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *
import sys
# pip3 install pynput
# pip3 install airtest-selenium
abs_path = os.path.abspath(os.path.dirname(__file__))
common_path = os.path.join(abs_path.split("airtest_auto")[0], "airtest_auto", "web_util")
sys.path.append(common_path)
from web_util import *

driver = get_driver()
# auto_setup(__file__)
try:
    driver.get("http://www.baidu.com")
except Exception as e:
    snapshot(msg="报错后截图")
    raise e
finally:
    driver.close()
