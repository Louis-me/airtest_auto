# -*- coding: utf-8 -*-
import configparser
import os
import json

"""
读取ini文件
"""


class ReadIni(object):
    def __init__(self, path):
        if not os.path.exists(path):
            print("请检查配置文件是否存在:%s" % path)
        self.config = configparser.ConfigParser()
        self.config.read(path, encoding='utf-8')

    def get_ini_list(self):
        pkg = self.config['default']['pkg']
        # udid = self.config['default']['udid']
        recording = True if self.config['default']['recording'] == 'true' else False
        phone = self.config['default']['phone']
        dev_connect = self.config['default']['dev_connect']
        root_path = self.config['default']['root_path']
        test_plan = int(self.config['default']['test_plan'])
        test_module = json.loads(self.config['default']['test_module'])
        remove_log = True if self.config['default']['remove_log'] == 'true' else False
        platform = self.config['default']['platform']
        driver_path = self.config['default']['driver_path']
        report_host = self.config['default']['report_host']
        local_host_path = self.config['default']['local_host_path']
        local_host_port = self.config['default']['local_host_port']

        recipient = json.loads(self.config['mail']['recipient'])
        mail_host = self.config['mail']['mail_host']
        mail_user = self.config['mail']['mail_user']
        mail_pass = self.config['mail']['mail_pass']
        port = int(self.config['mail']['port'])
        enable = True if self.config["mail"]["enable"] == 'true' else False

        data = {"pkg": pkg, "phone": phone, "dev_connect": dev_connect, "root_path": root_path, "test_plan": test_plan,
                "test_module": test_module, "remove_log": remove_log, "enable": enable, "recipient": recipient,
                "port": port, "mail_host": mail_host, "mail_user": mail_user, "mail_pass": mail_pass,
                "recording": recording,"local_host_path":local_host_path,"local_host_port":local_host_port,
                "platform": platform, "driver_path": driver_path, "report_host": report_host}

        return data

    def get_pkg(self):
        return self.config['default']['pkg']


if __name__ == "__main__":
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    path = PATH("../config/setting1.ini")
    s = ReadIni(path).get_ini_list()
    print(s)
    # print(s)
    # print(type(s))
# t = ReadIni(Br('conf.ini')).get_host()
