---
title: elk note
date: 2019-04-09
weight: 5
author: hackrole
email: hack.role@gmail.com
draft: true
tags: ["ELK", "elasticsearch"]
---

# elastic stack

## elasticsearch

the core component used to store data.

## logstash or fluentd

log forwarder and aggregation


## kibana

the frontend for elastchsearch.
support search/dashboard and so on.

## beats

metricsbeat/filebeat and so on.
used to send data to logstash/fluent or elasticsearch directly.

## others

1) you may use kafka to buffer log data.

2) you may need nginx to server kibana and add auth to kibana service.


# elasticsearch detail

## elasticsearch concepts

### Documents
are json objects.

be compared to a row in a table in the world of relational database.

### types
XXX this is Depresed.

used to save similar types of data in a single index.
in elasticsearch 6 and future, this would be remove.

### mapping

the schema in world of relational databases.

### index

the database in world of relational databse.

### shards

shareds of data.

## api category

1) docuement api: update/create/get/delete

2) search api: _search

3) indices api: get/delete/update/create indices

4) cluster api: get cluster status


# logstash detail

[5 logstash pitfalls](https://logz.io/blog/5-logstash-pitfalls-and-how-to-avoid-them/)

## plugin

1) input plugin: file/beats/syslog/http/tcp/udp/stdin

2) filter plugin: grok/date/mutate/drop/...

3) output plugin: file/s3/csv/rabbitmq/...

4) codecs: decode/encode data in input or output, plain/json/json_lines/rubydebug/...


# kibana detail

## visualization types

1) basic charts: (Area/Heat Map/Horizontal Bar/Line/Pie/Vertical Bar)

2) Data: (data table, Gauge, Goal, Metric)

3) Maps: (Coordinate Map, Region Map)

4) Time series: (Timelion, Visual Builder)

5) Other: (Controls, Markdown, Tag Cloud)

## saved objects

1) saved index patterns

2) saved searches

3) saved visualizations/dashboards

# beat detail

[5 filebeat pitfalls](https://logz.io/blog/filebeat-pitfalls/)

## beat module
used to parse the log, for example nginx/mysql



[^1]: [logz ELK](https://logz.io/learn/complete-guide-elk-stack/) 
