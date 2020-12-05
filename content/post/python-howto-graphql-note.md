+++
title = "python-graphql-server note"
author = ["hackrole"]
date = 2020-12-05
series = ["howtographql"]
categories = ["howtographql"]
draft = false
weight = 2002
+++

## schema-driven development {#schema-driven-development}

1.  define your types and the appropriate queries and mutations for them.
2.  implemetns functions called resolvers to handle these types and their fields.
3.  as new requirements arrive, go back to step 1 update the schema.


## about relay {#about-relay}

1.  a mechanism for refetching an object
2.  a description of how to page through connections
3.  structure around mutation to make them prediatable
