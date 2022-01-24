# -*- coding=utf-8 -*-
import shutil
import threading

from airtest.cli.runner import AirtestCase, run_script
from argparse import *
import jinja2
import io
from airtest.report import report
from util.send_email import SendEmail
from util.compress_file import copy_and_zip
from util.read_ini import ReadIni
from util.android_util import attached_devices
from util.common import *
from util.http_server import HttpServer

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def run_case(data):
    # 当平台为安卓时，检查是否连接成功
    device = None
    if data.get("platform", "1") == "android":
        print("启动安卓启动器")
        devices = attached_devices()
        if not devices:
            print("无可用设备")
            return
        device = [data["dev_connect"] + data["dev"]]

    elif data.get("platform", "1") == "ios":
        pass
    elif data.get("platform", "1") == "web":
        print("启动web启动器")
        pass

    test = CustomAirtestCase(data["root_path"])
    test.run_air(device, data)


def run(root_path, test_case, device, local_host_path, recording=None):
    # 具体的用例
    script = os.path.join(root_path, test_case["module"], test_case["case"])

    log_host_path = os.path.join(test_case["module"], test_case["case"].replace('.air', ''))
    log = os.path.join(local_host_path, log_host_path)
    os.makedirs(log)
    print(str(log) + '日志文件目录创建成功')
    output_file = os.path.join(log, 'log.html')
    args = Namespace(device=device, log=log, compress=None, recording=recording, script=script, no_image=None)
    try:
        run_script(args, AirtestCase)
        is_success = True
    except:
        is_success = False
    return {"is_success": is_success, "output_file": output_file, "script": script, "log": log,
            "log_host_path": log_host_path}


class CustomAirtestCase(AirtestCase):
    @classmethod
    def setUpClass(cls):
        super(CustomAirtestCase, cls).setUpClass()

    def __init__(self, root_dir):
        self.fail_data = []
        self.results = {"dev": "", "modules": [], "total_time": "", "data": [], "start_time": "", "success": "",
                        "count": ""}
        # self.log_list = []
        super().__init__()

    def setUp(self):
        super(CustomAirtestCase, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        super(CustomAirtestCase, self).setUp()

    def run_air(self, device, data):
        get_data_list = get_test_case(data)
        if not get_data_list:
            print("无可用用例")
            return
        # 开启本地http服务器
        threading.Thread(target=HttpServer.start, args=(),
                         kwargs={"local_host_path": data["local_host_path"],"port": data["local_host_port"]}).start()
        # 整个用例开始执行时间
        start_time = datetime.now().strftime("%H:%M:%S")
        data['report_host'] = "http://" + data["report_host"] + ":" + data["local_host_port"]
        modules = []
        # 日志按照日期格式生成
        log_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # 生成本地的测试目录
        log_path = os.path.join(data["local_host_path"], "log")
        local_host_path = os.path.join(log_path, log_date)
        # remove_log表示如果传值就会删除整个log文件夹，删除后无法查看历史报告
        if data["remove_log"] and os.path.isdir(log_path):
            shutil.rmtree(log_path)

        os.makedirs(local_host_path)
        print(str(local_host_path) + '日志跟目录创建成功')
        for j in get_data_list:
            # 用例开始执行日期
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 用例开始执行时间
            s_time = datetime.now().strftime("%H:%M:%S")
            # 循环运行用例
            get_run = run(data["root_path"], j, device, local_host_path, data["recording"])
            # 用例结束执行日期
            end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 用例结束执行时间
            e_time = datetime.now().strftime("%H:%M:%S")
            # 用例耗时时间
            sum_time = get_case_total_time(s_time, e_time)
            # 生成测试用例的详情报告
            rpt = report.LogToHtml(get_run["script"], get_run["log"], data["report_host"] + "/report", log_host=
            data["report_host"] + "/log/" + log_date + "/" + get_run["log_host_path"])
            rpt.report("log_template.html", output_file=get_run["output_file"])
            # 记录测试结果
            s_name = os.path.join(j["case"].replace(".air", ""))
            s_log = os.path.join(data["report_host"], "log", log_date, j["module"], s_name)
            result = {"result": get_run["is_success"], "start_date": st_date, "end_date": end_date,
                      "sum_time": sum_time,
                      "log": s_log, "name": s_name}
            modules.append(j["module"])
            self.results["data"].append(result)
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
        # 计算用例成功，失败,总数
        get_case_data = self.results["data"]
        success = 0
        s_count = len(get_case_data)
        for j in get_case_data:
            if j.get("result"):
                success += 1
        self.results["start_time"] = log_date
        self.results["success"] = success
        self.results["count"] = s_count
        self.results["dev"] = data["dev"]

        # 打印失败用例
        if self.fail_data:
            print("存在失败用例")
            print(self.fail_data)

        # 生成测试报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(local_host_path),
            extensions=(),
            autoescape=True
        )
        print("用例结果为：%s" % self.results)
        # 可能模板文件已经更新，所以要先删除模板文件
        t = os.path.join(local_host_path, "summary_template.html")
        if os.path.exists(t):
            shutil.rmtree(t)
        shutil.copy(PATH("util/summary_template.html"), local_host_path)
        template = env.get_template("summary_template.html", local_host_path)
        html = template.render({"results": self.results})
        put_html = os.path.join("summary_%s.html" % datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        output_file = os.path.join(local_host_path, put_html)
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        # 按日期生成测试报告,方便对比历史报告，但是程序入口字段需要设置为"remove_log": False
        print("测试报告本地路径：%s" % output_file)
        print("测试报告访问服务器：%s/%s/%s/%s" % (data['report_host'], "log", log_date, put_html))

        # # 固定输出给CI
        # output_file = os.path.join(data["root_path"], "summary.html")
        # with io.open(output_file, 'w', encoding="utf-8") as f:
        #     f.write(html)
        # 当发送邮件参数为真，就对文件进行压缩并发送测试报告到指定邮箱，此功能暂时不做适配
        if data.get("send_email"):
            # 压缩测试报告
            # report_file = os.path.join(data["root_path"], "report")
            # case_log = os.path.join(data["root_path"], "log")
            # case_html = output_file
            # zip_list = [report_file, case_log, case_html]
            # zip_path = copy_and_zip(zip_list, "report")
            # # 发送测试报告邮件
            # to_addr = data["to_addr"]
            # SendEmail.send(zip_path=zip_path, to_addr=to_addr)
            pass


def single_runner(data1):
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    path = PATH("config/setting1.ini")
    data = ReadIni(path).get_ini_list()
    run_case(data)


if __name__ == '__main__':
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    path = PATH("config/setting1.ini")
    data = ReadIni(path).get_ini_list()
    run_case(data)
