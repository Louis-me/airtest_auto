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
from util.common1 import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def run_case(root_dir):
    devices = attached_devices()
    if not devices:
        print("无可用设备")
    else:
        test = CustomAirtestCase()
        device = ['Android://127.0.0.1:5037/%s?touch_method=ADBTOUCH' % devices[0]]  # 这里只取一台设备
        test.run_air(root_dir, device)


def run(root_dir, test_case, device):
    if type(test_case) == dict and test_case.get("module"):
        script = os.path.join(root_dir, test_case["module"], test_case["case"])
        log = os.path.join(root_dir, 'log', test_case["module"], test_case["case"].replace('.air', ''))
    else:
        script = os.path.join(root_dir, test_case)
        # log = os.path.join(root_dir, 'log' + '\\' + airName.replace('.air', ''))
        log = os.path.join(root_dir, 'log' , test_case.replace('.air', ''))

    if os.path.isdir(log):
        shutil.rmtree(log)
    else:
        os.makedirs(log)
        print(str(log) + 'is created')
    output_file = log + '\\' + 'log.html'
    args = Namespace(device=device, log=log, compress=None, recording=None, script=script)
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
        self.results = []
        super().__init__()

    def setUp(self):
        print("custom setup")
        super(CustomAirtestCase, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        # self.exec_other_script("teardown.owl")
        super(CustomAirtestCase, self).setUp()

    def run_air(self, root_dir, device):
        root_log = root_dir + '\\' + 'log'
        if os.path.isdir(root_log):
            shutil.rmtree(root_log)
        else:
            os.makedirs(root_log)
            print(str(root_log) + 'is created')
        # 获取用例列表
        get_data_list = get_test_case(root_dir)
        if not get_data_list[0]:
            return
        # 预留位置1：此处可以放卸载安装应用
        # 预留位置2：获取手机验证码，登录；可以采用打开手机短信应用获取后，输入到验证码，最好是用一个万能验证码

        # 直接循环用例
        for i in get_data_list[1]["airs"]:
            st_date = datetime.datetime.now()
            start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            get_run = run(root_path, i, device)
            end_date = datetime.datetime.now()
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sum_time = str(end_date - st_date).split(".")[0]
            rpt = report.LogToHtml(get_run["script"], get_run["log"])
            rpt.report("log_template.html", output_file=get_run["output_file"])
            result = {"name": i.replace(".air", ""), "result": get_run["is_success"], "start_time": start_time,
                      "end_time": end_time, "sum_time": sum_time}
            # 记录测试结果
            self.results.append(result)
        # 执行模块下用例
        for j in get_data_list[1]["module_airs"]:
            st_date = datetime.datetime.now()
            start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            get_run = run(root_path,j, device)
            end_date = datetime.datetime.now()
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sum_time = str(end_date - st_date).split(".")[0]
            rpt = report.LogToHtml(get_run["script"], get_run["log"])
            rpt.report("log_template.html", output_file=get_run["output_file"])
            result = {"name": j["case"].replace(".air", ""), "result": get_run["is_success"], "start_time": start_time,
                      "end_time": end_time, "sum_time": sum_time, "module": j["module"]}
            self.results.append(result)

            # 设置失败用例
            # if not get_run:
            #     self.fail_data.append(i)

        # 生成测试报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(root_dir),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", root_dir)
        html = template.render({"results":self.results})
        output_file = os.path.join(root_dir, "summary.html")
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print(output_file)

        # # 存储失败用例
        # set_yaml(PATH("config/fail.yaml"), self.fail_data)
        # if not self.fail_data:
        #     print("存在失败用例：%s" % self.fail_data)


if __name__ == '__main__':
    root_path = PATH("air_case")
    run_case(root_path)
