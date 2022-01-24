# -*- coding=utf-8 -*-
import os
import threading

from common import init_runner
from read_ini import ReadIni
from runner3 import multi_runner
from runner5 import single_runner

if __name__ == "__main__":
    fun_path = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    path = fun_path("config/setting1.ini")
    data = ReadIni(path).get_ini_list()
    if data["boot"] == "multi":
        print("多机启动器启动")
        multi_runner(data)
    else:
        print("单机启动器启动")
        single_runner(data)
