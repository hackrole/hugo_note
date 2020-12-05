---
title: debug pytest hangs on request proxy
author: hackrole
email: hackrole.me@gmail.com
date: 2020-12-02 14:32:47
draft: true
tags: ["pytest", "python"]
category: ["programming"]
---


python 单元测试在mock requests后发现请求依旧会慢，但是最终会返回mock后的内容。

断点debug跟踪后发现是因为，request的url是一个 lain.local的内网地址。

requests在处理请求过程会先 去拿到host对应的IP，然后决定是否需要走代理，之后才是实际发送请求部分.

通过host获取ip导致卡住，到时这里是否不会抛异常或打日志。


- [] TODO pytest-profiling 模块使用
- [] TODO profiling prof文件分析
- [] TODO line-profiling
- [] TODO request代理部分代码

