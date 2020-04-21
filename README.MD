#  概述
- 用airtest做移动端自动化

## 特性
- 支持安卓批量执行用例
- 执行失败重测
- 支持指定部分用例进行调试
- 支持只运行失败用例

## 开始运行

### 设置单机配置：
- 打开```runner.py```

```buildoutcfg
if __name__ == '__main__':
    run_model = 0  # 0执行全部用例|1执行调试用例，数据来源为debug.yaml|2执行失败用例,数据来源fail.yaml
    play_back = 1  # 1 表示支持失败重测,-1表示不重测
    init_data()
    root_path = PATH("air_case")
    run_case(root_path, run_model, play_back)

```
- 当然，如果你的多机执行相同的用例，也可以修改下runner.py的部分代码：

```buildoutcfg
def run_case(root_dir, run_model, play_back):
    devices = attached_devices()
    if not devices:
        print("无可用设备")
    else:
        test = CustomAirtestCase()
        device = ['Android://127.0.0.1:5037/%s?touch_method=ADBTOUCH' % devices[0]]  # 这里只取一台设备
        # 这里改成多台即可
        test.run_air(root_dir,  run_model, play_back, device)

```

### 多机不同用例


- 设置config/muilt_case.yaml

```buildoutcfg
TPG5T18130013404:
  - 打开互动消息.air
df20fed3:
  - 打开我的关注.air
  - 打开我的文章.

```
- 如下runner1.py

- 如果你想打开失败重测，只要把runner1.py顶部的play_back 改为1



## 测试报告
![report2.png](img/report2.png "report2.png")

## 总结
- 这个简单的demo版本，该有的功能基本都有，后续版本或许会有，数据持久化改为数据库
- 测试报告优化
- 持续集成

 
   

