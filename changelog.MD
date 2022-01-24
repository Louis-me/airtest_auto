# 2022-1-24
- 使用自带的http.server造成阻塞，修改为Twisted
- 修改多机并行，安卓真机和雷电模拟器测试通过
- 适配单机和多设备web测试，本次测试为谷歌浏览器

# 2022-1-20
- 新增测试报告查看采用本地服务器查看，本次代码在runner5.py
- 测试报告和项目剥离
- 删除其他不用的启动器代码
- 由于修改了report.py源代码，也已经拷贝到根目录可供参考


# 2021-5-15
- 修复录屏不展示问题
- 新增删除历史html报告


# 2021-4-22
- 本次使用雷电模拟器
- 使用夜神模拟器无法截图，连接airtestide出现黑屏
- 打开夜神模拟器的开发者模式-usb调试，adb deivces就能获取到设备列表，若无法获取请重启模拟器
- 使用config/setting.ini进行配置,理论上支持配置ios
- 本次使用代码入口是runner0.py

    


# 2021-3-6 
- runner1.py新增发送压缩测试报告到指定邮箱
- 新增是否删除log文件字段，若删除会影响到历史报告查看
# 2020-9-26 
- runner1.py中新增summary.html给CI使用
- 优化手机录屏失败问题
- 剥离测试报告，摆脱本地依赖
- windows的CI简单运用
# 2020-8-29
- 优化日志记录方式
- 引入selenium，在runner4.py

# 2020-7-12
- 新增多设备并行，代码在runner3.py中
- config/case_data.json 记录测试设备和测试手机
- result_data 记录所有测试用例运行情况
- 修复某些手机测试报告无录像回放

# 2020-7-5
## 调整逻辑
- 重构所有代码
- 读取用例模式改变，修改为testcae/module/test.air的方式
- ```runner1.py```
```buildoutcfg
  # test_plan=1 表示调试用例，运行某几个模块用例；0表示全部用例，运行全部模块用例
    data = {"root_path": root_path, "test_plan": 0, "test_module": [], "dev": "TPG5T18130013404", "phone": "Nova2s"}
    # data = {"root_path": root_path, "test_plan": 1, "test_module": ["他的"], "dev": "TPG5T18130013404", "phone": "Nova2s"}
    run_case(data)
```
- 新增调试单个模块下用例
- ```runner2.py```
```buildoutcfg
    root_path = PATH("air_case/我的")
    test_plan = 1  # 0表示运行模块下所有用例,1表示运行模块下的test_data里面的用例
    test_data = ["打开我的文章.air"]
    run_case({"root_path": root_path, "test_plan": test_plan, "test_data": test_data,  "dev": "TPG5T18130013404",
              "phone": "Nova2s"})
```
## 注意事项
- **windows中用pycharm若出现adb命令异常**
    - 如无法获取到设备尽量需要和airtestIDE的adb保持一致，详细参考[官方文档](https://airtest.netease.com/docs/cn/2_device_connection/2_android_faq.html)
- **测试详细报告中，如果没有视频回放**
    - 手动打开手机端的yosemite，点击开始录屏，给予权限，最好是和PocoService一样，用手动管理，所有启动全部打开
- **想同时允许多个设备**
    - 只要在runner1/runner2中，修改不同的参数，然后在pycharm中多次运行，就能启动多设备
    - 后续新增多进程多机并发
# 2020-6-12
- 代码在runner2.py
- 支持用例采用yml编写方式
    - 自定义，如：不用再到每个用例步骤填写等待时间
    - 灵活
    - 容错
- 支持用例文件夹下读取模块下用例，如testcase/me/case001_me_打开个人中心.air
- 测试报告向新增时间
### 待完成
- 测试报告详情新增视频回放

# 2020-4
## 1.0 特性
- runner.py
    - 支持安卓批量执行用例
    - 执行失败重测
    - 支持指定部分用例进行调试
    - 支持只运行失败用例
- runner1.py
    - 支持多机并行