+++
title = "17 rust OOP"
author = ["hackrole"]
date = 2020-11-04
lastmod = 2020-11-06T00:02:24+08:00
categories = ["Rust"]
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

Generic and Trait-Bound can only replace one type.会在编译时做单态化，所以无法在Vec中存放多种类型.即静态分发(static dispatch)
在Vec中存放Tracit配置dyn可以(dynamic dispatch)

`~object-safe-trait~`:

1.  返回类型不为self
2.  方法没有任何泛型类型参数

<!--listend-->

```rust
pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    /// dyn keyword
    pub components: Vec<Box<dyn Draw>>,
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}

/// Generic with trait-bound can only static-dispatch
// pub struct Screen<T: Draw> {
//     pub components: Vec<T>,
// }

// impl<T> Screen<T>
// where T: Draw{
//     pub fn run(&self) {
//         for component in self.components.iter() {
//             component.draw();
//         }
//     }
// }


/// add Draw-Trait Type
pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self){
        println!("draw button");
    }
}


struct SelectBox {
    width: u32,
    height: u32,
    options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        println!("draw selectbox");
    }
}
```


## 面向对象设计模式的实现 {#面向对象设计模式的实现}

`~TODO 状态模式~`

```rust
use blog::Post;

fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");
    assert_eq!("", post.content());

    post.request_review();
    assert_eq!("", post.content());

    post.approve();
    assert_eq!("I ate a salad for lunch today", post.content());
}


pub struct Post {
    state: Option<Box<dyn State>>,
    content: String,
}

impl Post {
    pub fn new() -> Post {
        Post {
            state: Some(Box::new(Draft {})),
            content: String::new(),
        }
    }

    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }

    pub fn content(&self) -> &str {
        self.state.as_ref().unwrap().content(self)
    }

    pub fn request_review(&mut self){
        if let Some(s) == self.state.take() {
            self.state = Some(s.request_review())
        }
    }

    pub fn approve(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.approve())
        }
    }
}


trait State {
    fn requet_review(self: Box<Self>) -> Box<dyn State>;
    fn approve(self: Box<Self>) -> Box<dyn State>;
    fn content<'a>(&self, post: &'a Post) -> &'a str {
        ""
    }
}

struct Draft {}

impl State for Draft {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        Box::new(PendingReview {})
    }

    fn approve(self: Box<Self>) -> Box<dyn State> {
        self
    }
}

struct PendingReview {}


impl State for PendingReview {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        self
    }

    fn approve(self: Box<Self>) -> Box<dyn State>{
        Box::new(Published {})
    }
}

struct Published {}

impl State for Published {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        self
    }

    fn approve(self: Box<Self>) -> Box<dyn State> {
        self
    }

    fn content<'a>(&self, post: &'a Post) -> &'a str {
        &post.content
    }
}
```
