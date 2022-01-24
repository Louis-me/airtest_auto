# -*- coding=utf-8 -*-
import os

from airtest.core.api import auto_setup
from airtest_selenium.proxy import WebChrome

from read_ini import ReadIni


def get_driver():
    path = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    ini_path = path("../config/setting1.ini")
    driver_path = ReadIni(ini_path).get_web_driver_path()
    if not os.path.exists(driver_path):
        print("请检查驱动文件是否存在：%s" % driver_path)
        return
    driver = WebChrome(driver_path)
    driver.implicitly_wait(20)
    auto_setup(__file__)
    return driver



# def open_home_url(url):
#     driver = get_driver()
#     driver.get(url)
#     return driver
