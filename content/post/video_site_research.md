+++
title = "视频站点架构探索"
author = ["代鹏"]
lastmod = 2021-07-01T13:21:37+08:00
draft = false
+++

## video site or OBS site {#video-site-or-obs-site}


### how to write a video-site or OBS-site {#how-to-write-a-video-site-or-obs-site}


#### <span class="org-todo todo TODO">TODO</span> ref site page {#ref-site-page}

<!--list-separator-->

-  AcFun A站

    [A站架构](https://blog.qiniu.com/archives/5786)

    业务层面: 用户上传体验，举报自动审核等流程
    技术探索: P2P技术?，视频编码切分，视频缩略图存储挑战, 最初的盗链站实现?

<!--list-separator-->

-  youku, youtube

    [youku,youtube,twitter,justinTV 架构](https://cloud.tencent.com/developer/article/1074238)

    <!--list-separator-->

    -  youku

        数据库mysql的一般进化路线: 读写分离 -> 水平sharding, 考虑NoSql,NewSql??
        缓存和CDN的使用

    <!--list-separator-->

    -  youtube

        psyco（dead), pypy JIT编译
        热门内容和非热门内容处理方式的分化

        保持简单和廉价
        保持网络路径简单
        使用常用设备
        使用自架的存储，要考虑文件系统限制 ext3 vs oss, 小文件存储优化

        <!--list-separator-->

        -  learning

            stall for time, 创造性和风险性的技巧让你短期内解决问题并让你发现长期解决方案
            Proioritize, 找出服务核心价值，对资源划分优先级
            pick your battle, 别怕将你的核心服务分出去，CDN
            keep it simple, 简单允许你重新架构
            shard, sharding帮助隔离,不只是性能
            constant iteration on bottlenecks: 软件(DB, 缓存), OS(磁盘I/O), 硬件(内存/RAID)
            you succeed as a team. 拥有一个跨越条律，了解总个系统并知道系统内容细节的团队

    <!--list-separator-->

    -  twitter

        架构图？？ 搜索其他文章

        <!--list-separator-->

        -  learning

            数据库一定要进行合理的索引,(监控慢查询来补全?,一查询一表模式?)
            要尽可能快的认知你的系统，这要求你灵活的运用各种工具
            缓存x3,缓存一切可以缓存的,让你的系统飞起来

    <!--list-separator-->

    -  justin.TV

        p2p和CDN结合
        100%可能与维护的矛盾?
        Usher与负载均衡
        服务器形成加权树??
        从AWS到自己的数据中心:(成本,可靠稳定独享的网络而不是动态伸缩的能力)
        存储?
        实时转码?

        <!--list-separator-->

        -  learning

            自己开发还是购买
            关注自己做的事情，不要在意别人怎么干
            不要外包?
            把一切当作实验来做,对所有东西进行测量，追踪
            最重要的是理解你的网站如何共享,增长黑客??
            对不重要的事情，不要浪费时间
            为负载峰值做设计
            让网络结构保持简单
            and so on...

<!--list-separator-->

-  直播架构

    <https://blog.csdn.net/zgpeace/article/details/108552358>


#### problem {#problem}

<!--list-separator-->

-  RTMP协议??

<!--list-separator-->

-  盗链与防盗链

    链接有效期等配合CDN做防盗连?
    简单的HTTP refer, UA等判断

<!--list-separator-->

-  视频存储和转码

    视频格式: FLV, MP4
    码率: 480P 720P, 1080P, 原画

    视频切片，涉及到视频编码格式问题

<!--list-separator-->

-  直播使用云解决方案

    云解决方案架构

<!--list-separator-->

-  流媒体服务器??

<!--list-separator-->

-  P2P技术的可能性?

    基于web的p2p技术的可能性

    参考实现: 快播?

<!--list-separator-->

-  内容审核，涉黄涉政

<!--list-separator-->

-  CDN技术

<!--list-separator-->

-  线路带宽，费用问题
