---
title: graphql note
date: 2019-04-03
weight: 5
author: hackrole
email: hack.role@gmail.com
tags: ['graphql', 'graphene', 'graphene-django']
category: ['programming']
draft: true
---

# concept

## underfetching

the rest api may design not so good to fit the client requests.
which may need the client to send multi request to get want it want.

## overfetching

the rest api may return too much than the client ask,
it will take more time for network to download and renderer to parse data.

## N+1 request problem

usually in rest web services. you may
request a user with follows, and get all follows article name by another N requests.

Rest solve this by use compose-resource, which may conflicted with the princile of REST.

GraphQL can got the data as you want, so it can perform better at this problem.

## graphql

### query

used to fetch data for graphql server 
```graphql
query {
    human {
        id
        name
    }
}
```

### mutation

used to cause data write

can contains multiple fields like query.

multiple fields in query will execute in parallel.
multiple fields in mutation will run in series.

```graphql
mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!){
    createReview(episode: $ep, review: $review){
        stars
        commentary
    }
}
```

### subscribe

use for realtime data-change subscribe.

### resovler

the way to get data for `Field`.
can get data for database or web or anywhere else.

### schema

the root object in graphql.
it concrete the root query and root mutation.
and will response to the client request.

can use to execute to get result which will be
useful to test the api and unit-test.

### field

define sub query/mutation in root or nonroot query/mutation.

fields may be scalar, like string/int/float.
Or objects/List/, remember the graphql is strong type.
the null/nonnull is important.

### Schema Definition Language(SDL)
use for write GraphQL schemas

### DataLoader

use for effecitve reason to reduce the times to required database or other resolver.

### arguments
pass agruments to fields, to do query-filter or mutation-data

```graphql
human(id: "1000"){
    name
    height(unit: FOOT)
}
```

### alias

useful for same object with different arguments.
```graphql
query {
    empireHero: hero(episode: EMPIRE) {
        name
    }
    jediHero: hero(episode: JEDI){
        name
    }
}
```

### Fragments

reusable units to construct sets of fields.
avoid for repeat the fields in complicated DSL.

```graphql
query {
    leftcomparsion: hero(episode: EMPIRE){
        ...comparisonFields
    }
    rightcomparsion: hero(episode: JEDE){
        ...comparisonFields
    }

    fragment comparisonFields on Character{
        name
        appearsIn
        friends {
            name
        }
    }
}
```

### Variable

used in fragments for different units.
can make the frontend developer more happier.

variable can have defult value.


```graphql
query HeroComparison($first: Int=3){
    leftComparison: hero(episode: EMPIRE){
        ...comparisonFields
    }
    rightComparison: hero(episode: JEDI){
        ...comparisonFields
    }
    fragments comparisonFields on Character {
        name
        friendsConnection(first: $first){
            totalCount
            edges {
                node {
                    name
                }
            }
        }
    }
}
```

### directives

use with variables to dynamtically change the structure and shape of our query.

@include(if: Boolean)
@skip(if: Boolean)

can define your own directives.

```graphl
query hello($episode: Episode, $withFriends: Boolean!){
    hello(episode: $Episode){
        name
        friends @include(if: $withFriends){
            name
        }
    }
}
```

### operation name

to name to query/mutation/subscription operator
used to make our code less ambiguous.

```
query HeroNameAndFriends {
    hero {
        name
        friends {
            name
        }
    }
}
```

### inline fragments

graphql schema include the ability to define interface and union types.

if your query return an interface or union type, you will need
to use inline fragment to access data on the underlying concrete type.

```graphql
query HeroForEpisode($ep: Episode!){
    hero(episode; $ep){
        name
        ... on Droid {
            primaryFunction
        }
        ... on Human {
            height
        }
    }
}
```

### meta fields

get meta data for graphql server

query {
    search(text: "a"){
        __typename
        ... on Human{
            name
        }
        ... on Droid{
            name
        }
        ... on Starship{
            name
        }
    }
}

### interface

an abstract type that inlcude a certain set of fields that a type must include
to implement the interface.
```graphql
interface Character{
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
}
type Human implements Character {
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
    starships: [Starship]
    totalCredits: Int
}
type Droid implements Character{
    id: ID!
    name: String!
    friends: [Character]
    appearsIn: [Episode]!
    primaryFunction: String
}
```

### union types

similar to interface, but they donot specify any common fields between types.

```graphql
union SearchResult = Human | Droid | Starship

query {
    search(text: "an"){
        __typename
        ... on Human {
            name
            height
        }
        ... on Droid {
            name
            primaryFunction
        }
        ... on Starship{
            name
            length
        }
    }
}
```

### input type

use to pass complex objects in arguments.
particularly useful in case of mutations.

```graphl
input ReviewInput{
    stars: Int!
    commentary: String
}

mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!){
    createReivew(episode: $ep, review: $review){
        stars
        commentary
    }
}
```

### schema stitching

combine and connect multiple GraphQL API into a single one.

## graphql bindings

# problems

## network

## authorization

## filters
generate filters with django-filter and relay.

## pagination

## version

## batch load and cache

throught DataLoader

## error handlers

# tools

## graphql faker

## prisma

## graphql playground

## graphql config

## graphql-tools

## graphql fragments


# refs

[https://www.prisma.io/blog/top-5-reasons-to-use-graphql-b60cfa683511](five reason to use graphql)

[graphql spec 201807](https://graphql.github.io/graphql-spec/June2018/)

[howtographql](https://www.howtographql.com/)

[facebook graphql relay doc](https://facebook.github.io/relay/docs/en/graphql-server-specification.html)

[how prisma and graphql fit together](https://www.prisma.io/blog/prisma-and-graphql-mfl5y2r7t49c/)
