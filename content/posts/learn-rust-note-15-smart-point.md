+++
title = "15 smart-point(智能指针)"
author = ["hackrole"]
date = 2020-11-01
lastmod = 2020-11-04T00:14:37+08:00
tags = ["Rust"]
draft = true
weight = 2002
+++

## introduce {#introduce}

智能指针也是一类指针，但是拥有额外的元数据和功能。
比如 reference-count(引用计数)只能指针, 允许数据有多个所有者，记录共多少个所有者，在没有所有者时清理数据
String和Vec<T>也是智能指针，有元数据(容量等)和额外的功能(方法)

智能指针通常使用struct实现,一般是要实现Deref和Drop trait
智能指针是Rust常用的通用设计模式，很多库会有自己的智能指针，也可以编写自己的智能指针.

这里主要讨论最常用的智能指针:

1.  Box<T> 用于在堆上分配值
2.  Rc<T> 一个引用计数类型,数据可以有多个所有者
3.  Ref<T>和RefMut<T>, 通过RefCell<T>访问. RefCell<T>是一个在运行时而不是编译时执行的借用规则的类型。

另外需要涉及 ****内部可变性**** (interior mutability)模式
已经 ****引用循环**** (reference cycles), 会泄漏内存，已经如何避免


## Box<T>使用堆上的数据 {#box-t-使用堆上的数据}

使用场景:

1.  编译时未知大小的类型，由想要在需要确切大小的上下文中使用这个类型值
2.  多有大量数据，需要确保在数据不被copy的情况下转移所有权
3.  当希望一个值只关心他的类型是否实现特定的trait，而不是具体类型

<!--listend-->

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {}", b);
}
```

```rust
// use rust to define a recursive Type.
// Recursive-Type can ref itself, so cannot get it size in build-time.
enum List {
    Cons(i32, Box<List>),
    Nil
}

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3), Box::new(Nil))));
}
```


## Deref Trait将智能指针当作常规引用处理 {#deref-trait将智能指针当作常规引用处理}

DerefMut用于重载可变引用

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}


impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T{
        &self.0
    }
}
```


## Drop Trait允许在值离开作用域时执行一些代码 {#drop-trait允许在值离开作用域时执行一些代码}

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self){
        printn!("Dropping customersmartpointr with data `{}`!", self.ata)
    }
}

fn main() {
    let c = CustomSmartPointer {data: String::from("my stuff")};
    let d = CustomSmartPointer {data: String::from("other stuff")};
    println!("CustomerSmartPointers created.")
}
```

rust不允许我们直接调用Drop Trait的drop, 应该使用标准库提供的std::mem::drop

```rust
fn main() {
    let c = CustomSmartPointer {data: String::from("some new")};
    println!("CustomSmartPointer created.");
    // this world raise, cause rust not allow to call DropTrait.drop
    // c.drop();
    // use std::mem:drop is ok, it's in prelude
    drop(c);
    println!("customer droped before the end of main");
}
```


## Rc<T>引用计数智能指针 {#rc-t-引用计数智能指针}

Rc<T>只能用于单线程场景

```rust
/// this world failed
// enum List {
//     Cons(i32, Box<List>),
//     Nil,
// }

// use crate::List::{Cons, Nil};

// fn main() {
//     let a = Cons(5, Box::new(Cons(10, Box::new(Nil))));
//     let b = Cons(3, Box::new(a));
//     let c= Cons(4, Box::new(a));
// }

enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::rc::Rc;

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    let b = Cons(3, Rc::clone(&a));
    let c = Cons(4, Rc::clone(&a));
}
```


## RefCell<T>和内部可变性模式 {#refcell-t-和内部可变性模式}

RefCell<T>不变性作用于运行时, 只能用于单线程场景

```rust
pub trait Messenger {
    fn send(&self, msg: &str);
}

pub struct LimitTracker<'a T: Messager> {
    message: &'a T,
    value: usize,
    max: usize,
}

impl<'a, T> LimitTracker<'a, T>
where T: Messenger {
    pub fn new(messenger: &T, max: usize) -> LimitTracker<T> {
        LimitTracker {
            messenger,
            value: 0,
            max,
        }
    }

    pub fn set_value(&mut self, value: usize) {
        self.value = value;

        let percentage_of_max = self.value as f64 / self.max as f64;

        if percentage_of_max >= 1.0 {
            self.messenger.send("Error: You are over you quota!");
        } else if percentage_of_max >= 0.9 {
            self.messenger.send("Urgent warning: You've used up 90% of your quota!");
        } else if percentage_of_max >= 0.75 {
            self.messenger.send("Warning: You've used up over 75% of your quota!");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    struct MockMessenger {
        sent_messages: RefCell<Vec<String>>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger{
            MockMessenger { sent_messages: RefCell::new(vec![]) }
        }
    }
    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.borrow_mut().push(String::from(message));
        }

        /// this world panic in runtime
        /// cause RefCell implement Deref Trait, would do ref-check in runtime
        /// every borrow_mut() return a mut ref, every borrow() return a immut ref.
        /// it obey the rust ref-rules in runtime(one mut or multi immut)
        // fn send(&self, message: &str) {
        //     let mut one_borrow = self.sent_messages.borrow_mut();
        //     let mut two_borrow = self.sent_messages.borrow_mut();

        //     one_borrow.push(String::from(message));
        //     two_borrow.push(String::from(message));
        // }
    }

    #[test]
    fn it_send_an_over_75_percente_warning_message() {
        let mock_messenger = MockMessenger::new();
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);

        limit_tracker.set_value(80);

        assert_eq!(mock_messenger.sent_messages.borrow().len(), 1);
    }
}
```

RefCell<T> 通常和Rc<T>一起使用，可以实现multi-mut-ref.

```rust
#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use Crate::List::{Cons, Nil};
use std::rc:Rc;
use std::cell:RefCell;

fn main() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

    let b = Cons(Rc::new(RefCell::new(6)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(10)), Rc::clone(&a));

    *value.borrow_mut() += 10;

    println!("a after = {:?}", a);
    println!("b after = {:?}", b);
    println!("c after = {:?}", c);
}
```


## 引用循环和内存泄漏 {#引用循环和内存泄漏}

```rust
/// make a ref-circle, it's possible in rust.
/// but rust make sure it safe.
use std::rc::Rc;
use std::cell::RefCell;
use crate::List::{Cons, Nil};

#[derive(Debug)]
enum List{
    Cons(i32, RefCell<Rc<List>>),
    Nil
}


impl List {
    fn tail(&self) -> Option<&RefCell<Rc<List>>> {
        match self {
            Cons(_, item) => Some(item),
            Nil => None,
        }
    }
}

fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));

    println!("a initial rc count = {}", Rc::strong_count(&a));
    println!("a next item = {:?}", a.tail());

    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));

    println!("a rc count after b creation = {}", Rc::strong_count(&a));
    println!("b initial rc count = {}", Rc::strong_count(&b));
    println!("b next item = {:?}", b.tail());

    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc::clone(&b);
    }

    println!("b rc count after changing a = {}", Rc::strong_count(&b));
    println!("a rc count after chaning a = {}", Rc::strong_count(&a));

    /// Uncomment the next line to see that we have a cycle;
    /// it will overflow the stack
    //println!("a next item = {:?}", a.tail());
}
```

一般可以通过Weak<T>来消除引用循环,
Weak Ref通过Rc::downgrade创建，之后会增加并记录week\_ref的count, 但是在strong\_count为0时会清理数据.
WeakRef通过 \`rust\`{Weak<T>::upgrade() -> Option<Rc<T>>}

```rust
use std::rc::{Rc, Weak};
use std::cell::RefCell;

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak:new()),
        children: RefCell::new(vec![]),
    });

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());

    let branch = Rc::new(Node {
        value: 5,
        parent: RefCell::new(Weak::new()),
        chidlren: RefCell::new(vec![Rc::clone(&self)]),
    });
    *leaf.parent.borrow_mut() = Rc::downgrade(&branch);

    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
}
```
