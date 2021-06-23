#!/usr/bin/env python
# -*- coding=utf-8 -*-
import datetime

__CreateAt__ = '2020/4/19-17:34'

import threading
from multiprocessing import Pool

from airtest.cli.runner import AirtestCase, run_script
from argparse import *
import airtest.report.report as report
import jinja2
import shutil
import os
import io
from util.common import get_case_total_time, Runner3Common, Runner4Common
from datetime import datetime
import time
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def run_case(data):
    Runner3Common.init_result(PATH("config/result_data.json"), PATH("config/case_data.json"))
    test = CustomAirtestCase(data["root_path"])
    test.run_air(data)


def run(root_dir, test_case):
    # 日志按照日期格式生成
    log_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    script = os.path.join(root_dir, test_case["module"], test_case["case"])
    log = os.path.join(root_dir, 'log', test_case["module"], log_date, test_case["case"].replace('.air', ''))
    if not os.path.isdir(log):
        os.makedirs(log)
    # if os.path.isdir(log):
    #     shutil.rmtree(log)
    # else:
    #     os.makedirs(log)
    #     print(str(log) + ' is created')
    output_file = os.path.join(log, 'log.html')
    args = Namespace(device=None, log=log, compress=None, recording=None, script=script, no_image=None)
    # 用例开始执行日期
    st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 用例开始执行时间
    s_time = datetime.now().strftime("%H:%M:%S")
    try:
        run_script(args, AirtestCase)
        is_success = True
    except:
        is_success = False
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 用例结束执行时间
    e_time = datetime.now().strftime("%H:%M:%S")
    # 用例耗时时间
    sum_time = get_case_total_time(s_time, e_time)
    # 生成测试用例的详情报告
    rpt = report.LogToHtml(script, log, plugins=['airtest_selenium.report'])
    rpt.report("log_template.html", output_file=output_file)
    # 记录测试结果
    result = {"name": test_case["case"].replace(".air", ""), "result": is_success, "start_date": st_date,
              "end_date": end_date, "sum_time": sum_time, "log_date": log_date, "module": test_case["module"]}
    Runner3Common.set_result_json(result)

    if not is_success:
        print("存在失败用例")
        print(test_case)


class CustomAirtestCase(AirtestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super(CustomAirtestCase,cls).setUpClass()

    def __init__(self, root_path):
        self.fail_data = []
        self.root_path = root_path
        super().__init__()

    def setUp(self):
        print("custom setup")
        super(CustomAirtestCase, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        # self.exec_other_script("teardown.owl")
        super(CustomAirtestCase, self).setUp()

    def run_case1(self, data_item):
        print("==dataitem=")
        print(data_item)
        _dev = "谷歌浏览器"
        # 记录测试设备
        Runner3Common.set_case_module_dev({"test_dev": _dev})
        # 记录测试模块
        for j in data_item["test_module"]:
            Runner3Common.set_case_module_dev({"test_modules": j})

        get_case_data = Runner4Common.get_cases(data_item, self.root_path)
        for k in get_case_data:
            run(root_dir=self.root_path, test_case=k)

    def run_air(self, data):
        root_log = os.path.join(self.root_path, "log")
        if os.path.isdir(root_log):
            # shutil.rmtree(root_log)
            pass
        else:
            os.makedirs(root_log)
            print(str(root_log) + ' is created')
        # 整个用例开始执行时间
        start_time = datetime.now().strftime("%H:%M:%S")

        pool = Pool()
        pool.map(self.run_case1, data["test_case"])
        # 整个用例结束执行时间
        end_time = datetime.now().strftime("%H:%M:%S")
        # 以小时，分钟，秒钟的方式记录所有用例耗时时间
        total_time = get_case_total_time(start_time, end_time)
        test_modules_dev = Runner3Common.get_case_module_dev(PATH("config/case_data.json"))
        Runner3Common.set_result_summary_json({"total_time": total_time, "dev": test_modules_dev["test_dev"],
                                               "modules": test_modules_dev["test_modules"]})

        # 生成测试报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.root_path),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", self.root_path)
        html = template.render({"results": Runner3Common.get_result_json()})
        output_file = os.path.join(self.root_path,
                                   "summary_%s.html" % datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print("测试报告为%s" % output_file)
        # 固定输出给CI
        output_file1 = os.path.join(data["root_path"], "summary.html")
        with io.open(output_file1, 'w', encoding="utf-8") as f:
            f.write(html)
        # print("测试报告为%s" % output_file1)


test_data = {"root_path": PATH("air_case"), "test_case":
    [
        {"test_module": ["home"]},
        {"test_module": ["home1"]}
    ]
             }
if __name__ == '__main__':
    run_case(test_data)
