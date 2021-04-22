# -*- coding: utf-8 -*-
import configparser
import os
import json

"""
读取ini文件
"""


class ReadIni():
    def __init__(self, path):
        if not os.path.exists(path):
            print("请检查配置文件是否存在:%s" % path)
        self.config = configparser.ConfigParser()
        self.config.read(path, encoding='utf-8')

    def get_ini_list(self):
        pkg = self.config['default']['pkg']
        # udid = self.config['default']['udid']
        recording = self.config['default']['recording']
        phone = self.config['default']['phone']
        dev_connect = self.config['default']['dev_connect']
        root_path = self.config['default']['root_path']
        test_plan = int(self.config['default']['test_plan'])
        test_module = json.loads(self.config['default']['test_module'])
        remove_log = self.config['default']['remove_log']

        recipient = json.loads(self.config['mail']['recipient'])
        mail_host = self.config['mail']['mail_host']
        mail_user = self.config['mail']['mail_user']
        mail_pass = self.config['mail']['mail_pass']
        port = int(self.config['mail']['port'])

        enable = self.config["mail"]["enable"]
        data = {"pkg": pkg, "phone": phone, "dev_connect": dev_connect, "root_path": root_path, "test_plan": test_plan,
                "test_module": test_module, "remove_log": remove_log, "enable": enable, "recipient": recipient,
                "port": port,
                "mail_host": mail_host, "mail_user": mail_user, "mail_pass": mail_pass, "recording": recording}

        return data

    def get_pkg(self):
        return self.config['default']['pkg']


if __name__ == "__main__":
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )
    path = PATH("../config/setting.ini")
    s = ReadIni(path).get_ini_list()
    print(s)
    # print(s)
    # print(type(s))
# t = ReadIni(Br('conf.ini')).get_host()
