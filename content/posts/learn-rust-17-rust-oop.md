+++
title = "17 rust OOP"
author = ["hackrole"]
date = 2020-11-04
lastmod = 2020-11-05T00:19:48+08:00
tags = ["Rust"]
draft = false
weight = 2004
+++

1.  rust can bind data with methods
2.  rust can use pub/private to abstract inner implement.
3.  rust not support exntends. you should consider use combination more.

extend has two more usage-point.

1.  reuse pub method from parent-class or ability to rewrite it on willing. Rust use Trait to do this.
2.  polymorphism. Parent-Ref can ref any-SubType-instances, and method-call is eval at runtime.in Rust, you may use Generics-Type and Trait-Bounds todo this. \\\`bounded parametric polymorphism\\\`.


## <span class="org-todo todo TODO">TODO</span> Trait-object used for instances with different types {#trait-object-used-for-instances-with-different-types}
