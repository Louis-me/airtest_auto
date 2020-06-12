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

### 多机执行相同用例
- runner1.py 使用run_same_case函数运行即可

```buildoutcfg
    def run_same_case(self, device):
        """
        多设备相同用例
        :param device:
        :return:
        """
        _dev = device.split("/")[3]
        data_list = get_test_case(self.root_dir, 0)  # 多设备执行相同用例
        for i in data_list:
            get_run = run(self.root_dir, i, device, -1)
            if not get_run:
                self.fail_data.append(i)
        self.run_play_back(self.root_dir, device, play_back)


```


## 测试报告
![report2.png](img/report2.png "report2.png")
 
   
## 其他
[查看我的changelog](changelog.MD)
