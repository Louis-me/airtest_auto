# -*- coding=utf-8 -*-
import os
import platform
import subprocess
import threading

# pip install Twisted


class HttpServer(object):
    """
    启动http服务器，linux上待适配
    """

    @classmethod
    def start(cls, local_host_path, port):
        cls.stop(port)
        cmd = "twistd web --listen=tcp:%s --path=%s &" % (port, local_host_path)
        subprocess.Popen(cmd, shell=True)
        print("如果无法访问http服务请手动执行命令 %s" % cmd)

    @classmethod
    def stop(cls, port):
        os_name = platform.system()
        if os_name == "Windows":
            with os.popen('netstat -aon|findstr "%s"' % port) as res:
                res = res.read().split('\n')
            result = []
            for line in res:
                temp = [i for i in line.split(' ') if i != '']
                if len(temp) > 4:
                    result.append({'pid': temp[4], 'address': temp[1], 'state': temp[3]})
            for i in result:
                os.popen("taskkill -pid %s -f" % i["pid"])
        else:
            pass
if __name__ =="__main__":
    # HttpServer.start(r" E:\proj\aritest",'172.31.105.196', '8000')
    tt = threading.Thread(target=HttpServer.start, args=(), kwargs={"local_host_path": r"E:\proj\aritest", "port":"8000"})
    tt.start()
    print("21212121")