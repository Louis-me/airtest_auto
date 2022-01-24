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

from http_server import HttpServer
from read_ini import ReadIni
from util.android_util import attached_devices
from util.common import get_test_case_runner2, get_case_total_time, get_test_modules, Runner3Common
from datetime import datetime
import time

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def run_case(data):
    dev_connect = None
    # 当平台为安卓时，检查是否连接成功
    if data.get("platform", "1") == "android":
        print("启动安卓启动器")
        devices = attached_devices()
        if not devices:
            print("无可用设备")
            return
        dev_connect = data["dev_connect"]
    elif data.get("platform", "1") == "ios":
        pass
    elif data.get("platform", "1") == "web":
        print("启动web启动器")
    test = CustomAirtestCase(data["root_path"], dev_connect)
    test.run_air(data)


def run(root_dir, test_case, device, dev_connect, local_host_path, log_date, recording, report_host, phone):
    if device == "web":
        air_device = None
    else:
        air_device = [dev_connect + device]  # 取设备
    script = os.path.join(root_dir, test_case["module"], test_case["case"])
    log_host_path = os.path.join(test_case["module"], test_case["case"].replace('.air', ''))
    log = os.path.join(local_host_path, log_host_path)
    os.makedirs(log)
    print(str(log) + ' 创建日志文件成功')
    output_file = os.path.join(log, 'log.html')
    args = Namespace(device=air_device, log=log, compress=None, recording=recording, script=script, no_image=None)
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
    rpt = report.LogToHtml(script, log, report_host + "/report",
                           log_host=report_host + "/log/" + log_date + "/" + log_host_path)

    rpt.report("log_template.html", output_file=output_file)
    # 记录测试结果
    s_name = test_case["case"].replace(".air", "")
    s_log = os.path.join(report_host, "log", log_date, test_case["module"], s_name)
    result = {"result": is_success, "start_date": st_date, "end_date": end_date, "sum_time": sum_time,
              "log": s_log, "name": s_name, "phone": phone, "dev": device}

    Runner3Common.set_result_json(result)

    if not is_success:
        print("存在失败用例")
        print(test_case)


class CustomAirtestCase(AirtestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super(CustomAirtestCase,cls).setUpClass()

    def __init__(self, root_path, dev_connect):
        self.fail_data = []
        self.root_path = root_path  # 用例目录
        self.dev_connect = dev_connect  # 设备连接 如：Android://127.0.0.1:5037/
        self.log_date = ""  # 报告的跟目录 /log/201201201201
        self.local_host_path = ""  # 服务器报告目录
        self.recording = ""  # 是否录屏
        self.report_host = ""  # 服务器远程地址，如http://172.31.105.196:8000
        self.dev = "设备id号" # adb device 获取
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
        self.dev = data_item["dev"]
        # 记录测试设备
        Runner3Common.set_case_module_dev({"test_dev": self.dev})
        # 记录测试模块
        for i in data_item["test_module"]:
            Runner3Common.set_case_module_dev({"test_modules": i})

        get_case_data = Runner3Common.get_cases(data_item, self.dev, self.root_path)
        # 循环执行用例
        for i in get_case_data:
            run(root_dir=self.root_path, test_case=i, device=self.dev, dev_connect=self.dev_connect,
                local_host_path=self.local_host_path,log_date=self.log_date,
                recording=self.recording, report_host=self.report_host, phone=data_item["phone"])

    def run_air(self, data):
        self.recording = data["recording"]
        self.report_host = "http://" + data["report_host"] + ":" + data["local_host_port"]
        # 开启本地http服务器
        thread_http = threading.Thread(target=HttpServer.start, args=(),
                         kwargs={"local_host_path": data["local_host_path"], "port": data["local_host_port"]})
        thread_http.start()
        time.sleep(2)
        # 日志按照日期格式生成
        self.log_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # 生成本地的测试目录
        log_path = os.path.join(data["local_host_path"], "log")
        self.local_host_path = os.path.join(log_path, self.log_date)
        # remove_log表示如果传值就会删除整个log文件夹，删除后无法查看历史报告
        if data["remove_log"] and os.path.isdir(log_path):
            shutil.rmtree(log_path)

        os.makedirs(self.local_host_path)
        print(str(self.local_host_path) + ' 日志根目录创建')

        # 预留位置1：此处可以放卸载安装应用
        # 预留位置2：获取手机验证码，登录；可以采用打开手机短信应用获取后，输入到验证码，最好是用一个万能验证码

        # 整个用例开始执行时间
        start_time = datetime.now().strftime("%H:%M:%S")
        pool = Pool()
        pool.map(self.run_case1, data["test_case"])
        # 整个用例结束执行时间
        end_time = datetime.now().strftime("%H:%M:%S")
        # 以小时，分钟，秒钟的方式记录所有用例耗时时间
        total_time = get_case_total_time(start_time, end_time)
        test_modules_dev = Runner3Common.get_case_module_dev(PATH("config/case_data.json"))
        print("==设备=%s" % test_modules_dev)

        # 计算用例成功，失败,总数
        get_case_data = Runner3Common.get_result_json()
        success = 0
        s_count = len(get_case_data["data"])
        for j in get_case_data["data"]:
            if j.get("result"):
                success += 1

        # 记录用例结果
        Runner3Common.set_result_summary_json({"start_time": self.log_date, "success": success, "count": s_count,
                                               "total_time": total_time, "phone": test_modules_dev["test_dev"],
                                               "modules": test_modules_dev["test_modules"], "dev": self.dev})

        # 生成测试报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.local_host_path),
            extensions=(),
            autoescape=True
        )
        print("测试结果:%s" % Runner3Common.get_result_json())
        # 先删除模板文件，然后拷贝进去，防止模板文件更新不及时
        t = os.path.join(self.local_host_path, "multi_summary_template.html")
        if os.path.exists(t):
            shutil.rmtree(t)
        shutil.copy(PATH("util/multi_summary_template.html"), self.local_host_path)

        template = env.get_template("multi_summary_template.html", self.local_host_path)
        html = template.render({"results": Runner3Common.get_result_json()})
        put_html = os.path.join("summary_%s.html" % datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        output_file = os.path.join(self.local_host_path, put_html)
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        # 按日期生成测试报告,方便对比历史报告，但是程序入口字段需要设置为"remove_log": False
        print("测试报告本地路径为：%s" % output_file)
        print("测试报告访问服务器为：%s/%s/%s/%s" % (self.report_host, "log", self.log_date, put_html))
        thread_http.join()

def multi_runner(data1):
    fun_path = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    # 初始化记录数据的json
    Runner3Common.init_result(fun_path("config/result_data.json"), fun_path("config/case_data.json"))

    run_case(data1)


if __name__ == '__main__':
    pass
    # PATH = lambda p: os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), p)
    # )
    # path = PATH("config/setting1.ini")
    # data1 = ReadIni(path).get_ini_list()
    # if data1["boot"] == "multi":
    #     # 初始化记录数据的json
    #     Runner3Common.init_result(PATH("config/result_data.json"), PATH("config/case_data.json"))
    #     run_case(data1)
    # else:
    #     pass
