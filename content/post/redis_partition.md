---
title: redis分片相关
author: hackrole
email: hack.role@gmail.com
date: 2015-12-30 15:37:33
series: redis
draft: false
tags: ["redis"]
category: ["programming"]
---




介绍redis分片相关内容.

# 分片相关

分片是将数据分布到不同的redis实例上, 让每个redis服务实例只保存部分数据。

## 为何需要分片

1) 突破单机的内存和磁盘存储限制.

2) 复用多机的cpu计算和网络传输能力。

## 分片方法

分片有不同的实现方式, 如

1) 范围分片, R0(1-10000), R1(10001-2000)...
   缺点: 需要记录键的对应情况，所以比较低效, redis中不建议这种方式.

2) hash分片. 对每个key通过hash函数，计算到对应的实例。
   redis中部分client和proxy实现了一致性hash来做分片处理。

## 分片实现层面

分片可以做不同层面实现.

1) 客户端, 直接在客户端选择正确的实例完成操作。部分redis-client库实现这一功能.

2) proxy, 类似mogos. 客户端链接到proxy, 由proxy代为转发到正确的redis实例上. 比如twemproxy::

    https://github.com/twitter/twemproxy

3) 查询路由. 查询被发到集群中任一台实例上, 由实例来转发到正确的实例上.
   redis集群实现了一个混合风格的查询路由，需要配合client端使用(不是由redis来做定位，而是重定向client来实现).

## 分片的缺点

1) 跨越多个key的操作通常都不能使用, 部分操作可以通过间接的方式实现.

2) 跨越多个key的事务无法被支持.

3) XXX 以key的粒度来做分片，所以无法通过很多的key来共享一个大数据集，比如一个很大的sortedSet.

4) 使用分片会让业务逻辑更加复杂，包括运维工作。

5) 增加和删除节点/容量比较麻烦，是要平衡重新分片。redis集群支持这一个特性。
   client/proxy实现需要通过Pre-sharding来支持。

## 数据库还是缓存

redis作为缓存和数据库时，对待分片的策略有所不同.

缓存可以容忍定位失败。而数据库不允许。
所以在增加和删除节点时，或是部分节点失败时，数据库要良好的处理再分片/再路由操作。

# redis分片

1) redis集群是自动分片和高可用的首选方案. 具体参见 redis_cluster::

    http://redis.io/topics/cluster-tutorial

2) Twemproxy, 更易用,速度很快。 具体参见 

   http://antirez.com/news/44

3) 客户端分片库： Redis-rb / Predis.
