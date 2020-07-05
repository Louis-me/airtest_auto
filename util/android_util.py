#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
__CreateAt__ = '2020/4/19-17:44'


def attached_devices():
    command_result = ''
    command_text = 'adb devices'
    results = os.popen(command_text, "r")
    while 1:
        line = results.readline()
        if not line: break
        command_result += line
    results.close()
    devices = command_result.partition('\n')[2].replace('\n', '').split('\tdevice')
    return [device for device in devices if len(device) > 2]