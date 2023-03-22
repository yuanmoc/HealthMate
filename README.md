# HealthMate
![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![python version](https://img.shields.io/badge/python-v3.7-blue)


# 申明
本项目仅供学习研究，禁止商用！


# 功能
- [X] 登录
- [X] 可指定多个医生
- [X] 可指定就诊人
- [X] 可指定多个挂号时间
- [X] 可指定抢号频率
- [X] 定时抢号
- [X] 定时抢号时间范围
- [X] 脚本刷号
- [ ] MAC桌面端APP
- [ ] Windows桌面端APP



# 使用方式一，命令行

1、打包子模块
```bash
cd package
# 把子项目打包
python ./setup.py bdist_wheel
# 把打包好的模块安装到本地
pip install ./disk/HealthMate-1.0.0-py3-none-any.whl
# 返回主目录
cd ../
```

2、查看基本命令
```bash
python3 main.py --help
```

```text
  clear         清除信息
  init          初始化信息
  init-cron     设置定时挂号信息
  init-reg      初始化挂号信息
  init-reg-day  设置挂号时间
  start         启动挂号
  version       版本号
```

3、登录，按照提示进行操作
```bash
python3 main.py init
```
```text
请输入用户名: xxx
请输入密码: xxx
请输入医院城市名称: xxx
......
```

4、启动挂号,挂号成功后，会自动退出，或者使用ctrl+c退出
```bash
python3 main.py start
```

# 使用方式二，打包MAC桌面应用程序（以mac m1为例）
1、同样需要打包安装子模块
```bash
cd package
# 把子项目打包
python ./setup.py bdist_wheel
# 把打包好的模块安装到本地
pip install ./disk/HealthMate-1.0.0-py3-none-any.whl
# 返回主目录
cd ../
```
2、安装打包应用程序工具
```bash
pip install pyinstaller
pip install Pillow
```

3、打包

3.1 修改配置文件

修改HealthMate.spec文件中的项目路径，修改成你本地的绝对路径。

3.2 进行打包
```bash
pyinstaller  HealthMate.spec  
```

3.3 打包之后的位置

在项目工程目录下的dist文件下，有一个HealthMate.app文件，这个就是打包出来的应用程序，可以直接运行使用。





# 赞赏作者
如果您觉得HealthMate对你有帮助，可以请作者喝杯咖啡哦～


![code](./img/yuanmoc_code.png)


# More
如果有好的想法和建议，请联系作者


# LICENSE
```text
MIT License

Copyright (c) 2023 yuanmoc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```