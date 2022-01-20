# -*- coding=utf-8 -*-
import os
import platform


class HttpServer(object):
    """
    启动http服务器，linux上待适配
    """

    @classmethod
    def start(cls, http_path, port):
        cls.stop(port)
        driver = http_path.split(":")[0] + ":"
        print("cd %s && %s && python -m http.server %s" % (http_path, driver, port))
        os.popen("cd %s && %s && python -m http.server %s" % (http_path, driver, port))

    @classmethod
    def stop(cls, port):
        os_name = platform.system()
        if os_name == "Windows":
            find_port = 'netstat -aon | findstr %s' % port
            result = os.popen(find_port)
            text = result.read()
            pid = text[-5:-1]
            # 占用端口的pid
            find_kill = 'taskkill -f -pid %s' % pid
            print(find_kill)
            result = os.popen(find_kill)
            return result.read()
        else:
            pass


if __name__ == "__main__":
    HttpServer.start(r"E:\proj\aritest", "8000")
