#!/usr/bin/env python
# -*- coding=utf-8 -*-

__CreateAt__ = '2020/4/19-17:34'

import shutil
from airtest.cli.runner import AirtestCase, run_script
from argparse import *
from air_case.report import report
import jinja2
import io
from util.send_email import SendEmail
from util.compress_file import copy_and_zip

from util.android_util import attached_devices
from util.common import *
from util.read_ini import ReadIni

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def run_case(data):
    devices = attached_devices()
    if not devices:
        print("无可用设备")
        return
    test = CustomAirtestCase(data["root_path"])
    device = [data["dev_connect"]]
    test.run_air(device, data)


def run(root_path, test_case, device, log_date, recording=None):
    """

    :param root_path: 用例目录 E:\project\airtest_auto\air_case
    :param test_case: 具体用例 我的\XXX.air
    :param device: 设备连接串 [android:///]
    :param log_date: 记录用例的目录
    :param recording: 是否开启录屏
    :return:
    """
    script = os.path.join(root_path, test_case["module"], test_case["case"])
    log = os.path.join(root_path, 'log', test_case["module"], log_date, test_case["case"].replace('.air', ''))
    if os.path.isdir(log):
        shutil.rmtree(log)
    else:
        os.makedirs(log)
        print(str(log) + 'is created')
    output_file = os.path.join(log, 'log.html')
    if recording == "true":
        recording = True
        print("开启录屏")
    else:
        recording = None
    args = Namespace(device=device, log=log, compress=None, recording=recording, script=script, no_image=None)
    try:
        run_script(args, AirtestCase)
        is_success = True
    except:
        is_success = False
    return {"is_success": is_success, "output_file": output_file, "script": script, "log": log}


class CustomAirtestCase(AirtestCase):
    @classmethod
    def setUpClass(cls):
        super(CustomAirtestCase, cls).setUpClass()

    def __init__(self, root_dir):
        self.fail_data = []
        self.results = {"dev": "", "modules": [], "total_time": "", "data": []}
        self.log_list = []
        super().__init__()

    def setUp(self):
        super(CustomAirtestCase, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        super(CustomAirtestCase, self).setUp()

    def run_air(self, device, data):
        root_log = os.path.join(data["root_path"], "log")
        # remove_log表示如果传值就会删除整个log文件夹，删除后无法查看历史报告
        if os.path.isdir(root_log):
            if data.get("remove_log"):
                shutil.rmtree(root_log, ignore_errors=True)
                print("删除log文件夹")
                for i in os.listdir(data["root_path"]):
                    # 删除所有html报告文件，但是不删除模板文件
                    if i.find(".html") != -1 and i.find("summary_template") == -1:
                        os.remove(os.path.join(data["root_path"], i))
                print("删除所有html报告文件文件")
        else:
            os.makedirs(root_log)
        get_data_list = get_test_case(data)
        if not get_data_list:
            print("无可用用例")
            return
        # 整个用例开始执行时间
        start_time = datetime.now().strftime("%H:%M:%S")
        modules = []
        # 日志按照日期格式生成
        log_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        for j in get_data_list:
            # 用例开始执行日期
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 用例开始执行时间
            s_time = datetime.now().strftime("%H:%M:%S")
            # 循环运行用例
            get_run = run(data["root_path"], j, device, log_date, data["recording"])
            # 用例结束执行日期
            end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 用例结束执行时间
            e_time = datetime.now().strftime("%H:%M:%S")
            # 用例耗时时间
            sum_time = get_case_total_time(s_time, e_time)
            # 生成测试用例的详情报告
            rpt = report.LogToHtml(get_run["script"], get_run["log"], "../../../../report")
            rpt.report("log_template.html", output_file=get_run["output_file"])
            # 记录测试结果
            result = {"name": j["case"].replace(".air", ""), "result": get_run["is_success"], "start_date": st_date,
                      "end_date": end_date, "sum_time": sum_time, "module": j["module"], "log_date": log_date}
            modules.append(j["module"])
            self.results["data"].append(result)
            self.log_list.append(get_run["log"])
            # 记录失败用例
            if not get_run["is_success"]:
                self.fail_data.append({"module": j["module"], "case": j["case"]})
        # 整个用例结束执行时间
        end_time = datetime.now().strftime("%H:%M:%S")
        # 以小时，分钟，秒钟的方式记录所有用例耗时时间
        total_time = get_case_total_time(start_time, end_time)
        self.results["total_time"] = total_time
        # 记录测试模块
        self.results["modules"] = get_test_modules(modules)
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
        print("用例结果为：%s" % self.results)
        t = os.path.join(data["root_path"], "summary_template.html")
        if not os.path.exists(t):
            shutil.copy(PATH("util/summary_template.html"), data["root_path"])
        template = env.get_template("summary_template.html", data["root_path"])
        html = template.render({"results": self.results})
        output_file = os.path.join(data["root_path"], "summary_%s.html" % datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        # 按日期生成测试报告,方便对比历史报告，但是程序入口字段需要设置为"remove_log": False
        print("测试报告为：%s" % output_file)

        # 固定输出给CI
        output_file = os.path.join(data["root_path"], "summary.html")
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        # 当发送邮件参数为真，就对文件进行压缩并发送测试报告到指定邮箱
        if data.get("enable") == "true":
            print("邮件发送测试报告")
            # 压缩测试报告
            report_file = os.path.join(data["root_path"], "report")
            case_log = os.path.join(data["root_path"], "log")
            case_html = output_file
            zip_list = [report_file, case_log, case_html]
            zip_path = copy_and_zip(zip_list, "report")
            # 发送测试报告邮件
            # SendEmail.send(file_path=zip_path, mail_user=data["mail_user"], recipient=data["recipient"], mail_pass=data["mail_pass"],
            #                mail_host=data["mail_host"], port=data["port"])


if __name__ == '__main__':
    """
    python E:/project/trade-auto/runner1.py
    """
    path = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    ini_path = path("config/setting.ini")
    get_ini_data = ReadIni(ini_path).get_ini_list()
    run_case(get_ini_data)
