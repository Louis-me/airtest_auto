# -*- encoding=utf8 -*-
from airtest.core.api import *
import sys
# pip3 install pynput
# pip3 install airtest-selenium
# 得到绝对路径

abs_path = os.path.abspath(os.path.dirname(__file__))
# 得到公共用例目录
common_path = os.path.join(abs_path.split("airtest_auto")[0], "airtest_auto", "web_util")
sys.path.append(common_path)
from web_util import *

driver = get_driver()
try:
    driver.get("http://www.baidu.com")
    driver.find_element_by_id("kw").send_keys("test")
    driver.find_element_by_id("su").click()
except Exception as e:
    snapshot(msg="报错后截图")
    raise e
finally:
    driver.close()