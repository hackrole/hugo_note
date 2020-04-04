---
title: kafka lost data note
date: 2020-04-04
author: hackrole
email: hackrole.me@gmail.com
tags: ['kafak', 'note']
category: ['programing'']
draft: true
---

# the story

there was one porject named prism which I worked on. Its work is to listen from mulitple kafka topics,
then standardizing the data and send them to one certain kafka topic, there was another worker which will 
cosumer this topic and write the data to elasticsearch by batch. It use protobuf and avro as message serializer.

One day, I was telled the prism was stopped, after check it I found it was because the kafak producer has
change there schema which was not compatibility to old schema, this make the prism worker stop to work.
After update the prism proto schema, and restart it. 

One more worse things happened, It seems the prism have lost two days data. why?
after check the system, the reason is that. We are using kafka 0.11 which will save the group consumer offset
for 24 hours, but the prism was not configed with notification for failed, which make it stop work for more than 
one days, which leader the group offset delete in kafka, after restart the project, we use the default kafka-offset policy latest,
which just jump over the lost data.

then we try to reset the kafka topic to certain offset in the date by group, which failed.

As we only store 7 days date in kafka, We design to use a new kafka group name to consume from beginning,
and write to a new elasticsearch search, which take half a days to finish. Than we check back to the old prism worker.
And make a elasticsearch index alias to the new index. the problems was solved.

But one another problem comes, the stats api which read from the elastichsearch to produce daily-aggrations chart still failed.
after check it, the api produce a cache from the first visit for the certain days, and generate a cache file in the aliyun oss.
I ask the SRE to remove the daily folder in Aliyun oss, but it still not work, But while I force recreate the cache and put it 
in the oss bucket, it works. It seems the oss use something like DNS or CDN, the update will work right now, but the delete need time to work.
But I cannot just wait for the customer's complains, So I write a script to recreate all the aggs cache.
the works finish.

# things learned

1) kafka group-name not store always in kafka, in kafka 0.11 it only store one day, in more recently version it default it 7days by default.
you can always modify it at hand.

2) the worker process should always config some monitor and notification or logging, make the error be discovery as soon as possible.

3) kafka consume and producer should have some ways to warning each other about the schema changes.

4) how to validate cache or recreated cache is should import things we should consider.

5) combile oss and CDN as api which may not change seems a realy good idea. But you should have method to control the permissions.

6) the CDN/DNS has such properties, that update will work soon, but delete takes times, while work on strange problem, consider this.
