# -*- coding: utf-8 -*-
from datetime import datetime

from email6.mime.text import MIMEText

from email6.header import Header
from email6.mime.text import MIMEText
from email6.utils import parseaddr, formataddr
from email6.mime.multipart import MIMEMultipart
from email6.mime.application import MIMEApplication
import smtplib

# 第三方 SMTP 服务
mail_host = "smtp.126.com"  # 设置服务器
mail_user = "ashikun@126.com"  # 用户名
mail_pass = "XXXXX"  # 口令


class SendEmail():

    def format_addr(sefl, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    @classmethod
    def send(cls, f, to_addr):
        '''
        发送邮件
        :param f: 附件路径
        :param to_addr:发给的人 []
        :return:
        '''
        from_addr = mail_user
        password = mail_pass
        smtp_server = mail_host

        msg = MIMEMultipart()

        msg['From'] = cls().format_addr('自动化测试报告<%s>' % from_addr)
        msg['To'] = cls().format_addr('自动化测试报告 <%s>' % to_addr)
        msg['Subject'] = Header('自动化测试报告' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), 'utf-8').encode()

        msg.attach(MIMEText('自动化测试报告.', 'plain', 'utf-8'))
        part = MIMEApplication(open(f, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename="report.zip")
        msg.attach(part)

        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()


if __name__ == "__main__":
    file_s = r"E:\project\trade-auto\report.zip"
    SendEmail.send(file_s, ["284772894@qq.com", "ashikun@126.com"])
