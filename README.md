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


1、安装依赖
```bash
pip3 install -r requirements.txt
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



# 赞赏作者
如果您觉得HealthMate对你有帮助，可以请作者喝杯咖啡哦～


![code](app/yuanmoc_code.png)


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