---
title: python中使用with来减少代码重复
author: hackrole
email: hack.role@gmail.com
date: 2015-09-10 15:36:07
draft: true
tags: ["python"]
category: ["programming"]
---




python with的执行流程
---------------------

.. code-block:: python

    with <context> as <v>:
        <do things or raise Exception>

with <context> as v:

1) 先加载__exit__函数，如果context里没有实现，会在这里报错的

2) 执行__enter__方法,并把结果传给v

3) 执行用户代码,如果正常推出,使用(None, None, None)调用__exit__,
   如果代码抛出异常，使用(type, exception, traceback)调用__exit__

由上可以看出通过在代码里抛出特定异常，在__exit__里在下异常检测，
可以实现重用户代码向__exit__传递参数的作用.

例子
----

.. code-block:: python

   pass
