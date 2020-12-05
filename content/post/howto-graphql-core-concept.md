+++
title = "core-concept"
author = ["hackrole"]
date = 2020-12-05
series = ["howtographql"]
categories = ["howtographql"]
draft = false
weight = 2001
+++

## rest vs graphql {#rest-vs-graphql}


### good things from rest {#good-things-from-rest}

1.  stateless API, which make web-scalable and easy-manage
2.  resource-oriented programming and structured accessto resources, which make many goods, such as cacheable, retriable.


### the bad things with rest {#the-bad-things-with-rest}

\`1+N\` problem: fetch list api, fetch every detail api to get more message.

1.  overfetching(fetch too much data which was not requried)
2.  underfetching(not-enough data from api, which make it need multi request to get the data).
3.  too flexible, may things this like dynamic(rest) vs static(graphql).

the answer from rest-api design.

1.  overfetching: add special-api?
2.  underfetching(1+N): compound-resource
3.  too flexible: swagger?


### graphql core-concepts {#graphql-core-concepts}


#### the schema-definition-language(SDL) {#the-schema-definition-language--sdl}

the spec to define you API and data-model.

```graphql
# a data-model named Person
type Person {
  name: String! # ! mark this field required.
  age: Int!
  posts: [Post]!
}

type Post {
  title: String!
  author: Person!
}
```


#### Query {#query}

graph-like query, which solve the overfetch and underfetch problem.

```graphql
# query example
{
  allPersons {
    name
    age
    # query nested structed
    posts {
      title
    }
  }
}
# query with arguments
{
  allPersons(last: 2){
    name
  }
}
```


#### write with Mutations {#write-with-mutations}

three type mutation: create/update/delete

```graphql
# Mutation need `mutation` prefix
mutation {
  # the argument was data to create
  createPersion(name: "Bob", age: 36) {
    # this was data to return, allow single-roudtrip to mutationi and query data.
    name
    age
  }
}
```


#### realtime update with Subscriptions {#realtime-update-with-subscriptions}

like websocket notify in web.
not request-response type, represent a stream of data sent over to the client.

-   TODO how to implement this in real-server-env.

<!--listend-->

```graphql
subscription {
  newPersion {
    name
    age
  }
}
```

```graphql
# put it all together
type Query {
  allPersons(last: Int): [Persion]!
}

type Mutation {
  createPerson(name: String!, age: Int!): Person!
}

type Subscription {
  newPerson: Person!
}

type Person {
  name: String!
  age: Int!
  # ??
  posts: [Post!]!
}

type Post {
  title: String!
  author:  Person!
}
```


### bit picture {#bit-picture}

graphql was release as a specification,
which describe in detail the behaviour of a graphql server.

the usual architecture of graphql-server.

1.  graphql-server with a connected database.
2.  thin layer in front of a number of third party api
3.  a hybrid of above


### the graphql problem {#the-graphql-problem}


#### <span class="org-todo todo TODO">TODO</span> the graph-design make data-relationship complex. {#the-graph-design-make-data-relationship-complex-dot}

how to do cache for the API??

data-relation would cause stateful-api, which has scalable-problem??


#### <span class="org-todo todo TODO">TODO</span> no idempotent/unsafe method distinguish. {#no-idempotent-unsafe-method-distinguish-dot}

how to design retry failed idempotent-method??
how to apply multi mutation at-once??


#### <span class="org-todo todo TODO">TODO</span> the perfermance problem {#the-perfermance-problem}

graphql reslove was knows as CPU-unfriendly, which may case perfermance-problem.

the data-loader desgin detail??


#### <span class="org-todo todo TODO">TODO</span> 错误处理和debugger {#错误处理和debugger}


#### <span class="org-todo todo TODO">TODO</span> authentication and authzation {#authentication-and-authzation}
