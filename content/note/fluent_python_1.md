---
title: "Fluent_python: python data model"
date: 2019-03-26T19:21:13+08:00
auther: hackrole
email: hack.role@gmail.com
draft: true
series: "fluent_python"
tags: ["python"]
---

# desc

这一部分主要是讲解python内部magic-method.

## magic method 
TODO
### math

### str/format

### container/sequence

### 


# tips

## __repr__ vs __str__

## why __len__ is not normal method

python built-in class can be much faster by get length from `PyObject.ob_size`

the user-defined class has the same interface with built-in class.


# zen of python

1) 实用胜于纯粹

2) 不能让特例特殊到开始破坏既定规则

# TODO

python offical doc for datamodel
the zen of python


[^1]: [the zen of python](https://www.python.org/doc/humor/#the-zen-of-python) 

[^2]: <https://docs.python.org/3/reference/datamodel.html> 

[^3]: Alex Martelli(python技术手册) 关于数据模型

[^4]: Gregor Kiczales<the Art of Metaobject Protocol>

[^5]: AOP(面向切面编程) http://docs.zope.org/zope.interface/
