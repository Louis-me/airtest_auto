#!/usr/bin/env python
# -*- coding=utf-8 -*-
__CreateAt__ = '2020/6/9-21:39'

import os
from airtest_selenium.proxy import WebChrome


def init_web():
    """
    初始化数据,根据需求来定制
    :return:
    """

    path = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    driver_path = path("../exe/chromedriver.exe")
    driver = WebChrome(driver_path)
    driver.implicitly_wait(20)
    return driver


def open_home_url(url):
    driver = init_web()
    driver.get(url)
    return driver
