#  概述
- 用airtest做移动端自动化
- 支持安卓，ios,web
- 基于yml编写用例


## 开始运行
- 编写配置文件
```buildoutcfg
[default]
# 包名
pkg = com.jianshu.haruki
# 手机名字
phone=雷电模拟器
# 设备连接名字
dev_connect=Android://127.0.0.1:5037/
# 设备id,adb devices 获取，如果启动多设备，这里无效
dev=emulator-5554
# 用例目录
root_path=E:\proj\airtest_auto\air_case\android
 # test_plan=1 表示调试用例需要配合test_module使用，0表示全部用例;如果启动多设备,test_plan默认为0,设置1也无效
test_plan=1
test_module=["他的"]
# false|true 表示是否运行用例之前，删除log文件夹，删除后会影响查看历史报告
remove_log=true
# false|true 是否开启录屏,若传true就会自动录屏，但是在模拟器上录屏失败，只使用于真机
recording=false
# android|ios|web，当填如web时，需要填写驱动文件位置
platform =android
# driver_path=E:\proj\airtest_auto\exe\chromedriver.exe
driver_path=
# 服务器信的信息，比如本地的ip，用来展示报告
report_host=172.31.105.196
# 本地服务器路径，我把源代码中的report也放在里面了
local_host_path=E:\proj\aritest
# 本地服务器端口
local_host_port=8000
# 启动什么模式，单机和多机
# 如果指定multi就是多机并行，读取multi的配置，否则就为单机模式
boot=multi
[multi]
# 给不同的设备分配测试模块,dev中的设备id一定要填对
test_case = [{"dev":"ZL9LC685V86DNNMN","test_module": ["我的"],"phone":"真机1"}, {"dev":"emulator-5554","test_module":["他的"],"phone":"雷电"}]
#test_case = [{"dev":"emulator-5554","test_module":["他的"],"phone":"雷电"}]

```

## 测试报告
![summary.png](img/summary.png "report2.png")
![detail.png](img/detail.png "report2.png")
 
   
## 其他
[查看我的changelog](changelog.MD)
