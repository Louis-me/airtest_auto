#!/usr/bin/env python
# -*- coding=utf-8 -*-

__author__ = 'shikun'
__CreateAt__ = '2020/4/19-17:34'
from multiprocessing.pool import Pool
from airtest.cli.runner import AirtestCase, run_script
from argparse import *
import airtest.report.report as report
import jinja2
import shutil
import os
import io
from util.AndroidUtil import attached_devices
from util.common import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
play_back = - 1 # 1是开启失败重测，-1不开启


def run_case(root_dir):
    devices = attached_devices()
    if not devices:
        print("无可用设备")
    else:
        test = CustomAirtestCase(root_dir)
        dev_data = []
        for i in devices:
            dev_data.append("android:///%s" % i)
        test.run_air(dev_data)


def run(root_dir, test_case, device, play_back):
    if play_back > 0:
        airName = test_case + "失败重测"
    else:
        airName = test_case

    script = os.path.join(root_dir, test_case)
    print(script)
    log = os.path.join(root_dir, 'log' + '\\' + airName.replace('.air', ''))
    print(log)
    if not os.path.isdir(log):
        os.makedirs(log)

        # if os.path.isdir(log):
        #     shutil.rmtree(log)
        # else:
        #     os.makedirs(log)
        #     print(str(log) + 'is created')
    output_file = log + '\\' + 'log.html'
    args = Namespace(device=device, log=log, compress=None, recording=None, script=script)
    try:
        run_script(args, AirtestCase)
        is_success = True
    except:
        is_success = False
    # finally:
    rpt = report.LogToHtml(script, log)
    rpt.report("log_template.html", output_file=output_file)
    result = {"name": airName.replace('.air', ''), "result": rpt.test_result}
    setting_result(result)
    return is_success


class CustomAirtestCase(AirtestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super(CustomAirtestCase,cls).setUpClass()

    def __init__(self, root_dir):
        self.fail_data = []
        self.results = []
        self.root_dir = root_dir
        super().__init__()

    def setUp(self):
        print("custom setup")
        super(CustomAirtestCase, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        # self.exec_other_script("teardown.owl")
        super(CustomAirtestCase, self).setUp()

    def run_case(self, device):
        _dev = device.split("/")[3]
        data_list = get_yaml(PATH("config/mulit_case.yaml"))
        # 读取当前手机是否在配置文件中
        if data_list.get(_dev):
            get_data = data_list[_dev]
            for i in get_data:
                get_run = run(self.root_dir, i, device, -1)
                if not get_run:
                    self.fail_data.append(i)
        self.run_play_back(self.root_dir, device, play_back)

    def run_air(self, device):
        root_log = self.root_dir + '\\' + 'log'
        if os.path.isdir(root_log):
            shutil.rmtree(root_log)
        else:
            os.makedirs(root_log)
            print(str(root_log) + 'is created')

        pool = Pool()
        pool.map(self.run_case, device)

        # 生成测试报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.root_dir),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", self.root_dir)
        html = template.render({"results": get_yaml(PATH("config/result.yaml"))["result"]})
        output_file = os.path.join(self.root_dir, "summary.html")
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print(output_file)

        # 存储失败用例
        set_yaml(PATH("config/fail.yaml"), self.fail_data)
        if not self.fail_data:
            print("存在失败用例：%s" % self.fail_data)

    def run_play_back(self, root_dir, device, play_back):
        """
        失败重测
        :param play_back:
        :param root_dir:
        :param device:
        :return:
        """
        if play_back > 0:
            # 获取失败的用例
            play_data = self.fail_data
            play_data_len = len(play_data)
            print("开启失败重测用例")
            if play_data_len:
                print("开启失败重测成功")
                for j in play_data:
                    if play_data_len == 0:
                        break
                    get_run1 = run(root_dir, j, device, play_back)
                    play_data_len = play_data_len - 1
                    if not get_run1:
                        self.fail_data.append(j + "失败重测")
            else:
                print("无失败用例,开始重测失败")


if __name__ == '__main__':
    init_data()
    root_path = PATH("air_case")
    run_case(root_path)
