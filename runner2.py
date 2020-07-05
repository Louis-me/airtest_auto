#!/usr/bin/env python
# -*- coding=utf-8 -*-
import datetime

__author__ = 'shikun'
__CreateAt__ = '2020/4/19-17:34'

from airtest.cli.runner import AirtestCase, run_script
from argparse import *
import airtest.report.report as report
import jinja2
import shutil
import os
import io
from util.android_util import attached_devices
from util.common import get_test_case_runner2, get_case_total_time, get_test_modules
from datetime import datetime
import time

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def run_case(data):
    devices = attached_devices()
    if not devices:
        print("无可用设备")
    test = CustomAirtestCase()
    device = ['Android://127.0.0.1:5037/%s?touch_method=ADBTOUCH' % data["dev"]]  # 这里只取一台设备
    data["air_device"] = device
    test.run_air(data)


def run(root_dir, test_case, air_device, log_date):
    script = os.path.join(root_dir, test_case)
    log = os.path.join(root_dir, 'log', log_date, test_case.replace('.air', ''))
    if os.path.isdir(log):
        shutil.rmtree(log)
    else:
        os.makedirs(log)
        print(str(log) + ' is created')
    output_file = os.path.join(log, 'log.html')
    args = Namespace(device=air_device, log=log, compress=None, recording=True, script=script)
    try:
        run_script(args, AirtestCase)
        is_success = True
    except:
        is_success = False
    return {"is_success": is_success, "output_file": output_file, "script": script, "log": log}


class CustomAirtestCase(AirtestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super(CustomAirtestCase,cls).setUpClass()

    def __init__(self):
        self.fail_data = []
        self.results = {"dev": "", "modules": [], "total_time": "", "data": []}
        super().__init__()

    def setUp(self):
        print("custom setup")
        super(CustomAirtestCase, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        # self.exec_other_script("teardown.owl")
        super(CustomAirtestCase, self).setUp()

    def run_air(self, data):
        root_log = os.path.join(data["root_path"], "log")
        if os.path.isdir(root_log):
            # shutil.rmtree(root_log)
            pass
        else:
            os.makedirs(root_log)
            print(str(root_log) + ' is created')
        # 获取用例列表
        get_data_list = get_test_case_runner2(data)
        if not get_data_list:
            print("无可用用例")
            return
        # 预留位置1：此处可以放卸载安装应用
        # 预留位置2：获取手机验证码，登录；可以采用打开手机短信应用获取后，输入到验证码，最好是用一个万能验证码

        # 整个用例开始执行时间
        start_time = datetime.now().strftime("%H:%M:%S")

        for j in get_data_list:
            # 日志按照日期格式生成
            log_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # 用例开始执行日期
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 用例开始执行时间
            s_time = datetime.now().strftime("%H:%M:%S")
            # 循环运行用例
            get_run = run(data["root_path"], j, data["air_device"], log_date)
            # 用例结束执行日期
            end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 用例结束执行时间
            e_time = datetime.now().strftime("%H:%M:%S")
            # 用例耗时时间
            sum_time = get_case_total_time(s_time, e_time)
            # 生成测试用例的详情报告
            rpt = report.LogToHtml(get_run["script"], get_run["log"])
            rpt.report("log_template.html", output_file=get_run["output_file"])
            # 记录测试结果
            result = {"name": j.replace(".air", ""), "result": get_run["is_success"], "start_date": st_date,
                      "end_date": end_date, "sum_time": sum_time, "log_date": log_date}
            self.results["data"].append(result)
            # 记录失败用例
            if not get_run["is_success"]:
                self.fail_data.append({"case": j["case"]})

        # 整个用例结束执行时间
        end_time = datetime.now().strftime("%H:%M:%S")
        # 以小时，分钟，秒钟的方式记录所有用例耗时时间
        total_time = get_case_total_time(start_time, end_time)
        self.results["total_time"] = total_time
        # 记录测试模块
        self.results["modules"] = ""
        # 记录设备名字
        self.results["phone"] = data["phone"]
        # 打印失败用例
        if self.fail_data:
            print("存在失败用例")
            print(self.fail_data)

        # 生成测试报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(data["root_path"]),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", data["root_path"])
        html = template.render({"results": self.results})
        output_file = os.path.join(data["root_path"],
                                   "summary_%s.html" % datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        # print(output_file)


if __name__ == '__main__':
    root_path = PATH("air_case/我的")
    test_plan = 1  # 0表示运行模块下所有用例,1表示运行模块下的test_data里面的用例
    test_data = ["打开我的文章.air"]
    run_case({"root_path": root_path, "test_plan": test_plan, "test_data": test_data,  "dev": "TPG5T18130013404",
              "phone": "Nova2s"})
