# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *
import sys

# pip3 install pynput
# pip3 install airtest-selenium
# 得到绝对路径

abs_path = os.path.abspath(os.path.dirname(__file__))
# 得到公共用例目录
common_path = os.path.join(abs_path.split("airtest_auto")[0], "airtest_auto", "util")
sys.path.append(common_path)
from web_util import open_home_url
from airtest_selenium.proxy import WebChrome

# driver = WebChrome(os.path.join(common_path, "chromedriver.exe"))
try:
    driver = open_home_url("http://www.baidu.com")
    driver.find_element_by_id("kw").send_keys("baidu")
    driver.find_element_by_id("su").click()


except Exception as e:
    # snapshot(msg="报错后截图")
    raise e
finally:
    driver.close()
    driver.quit()

