+++
title = "16 无畏并发 fearless concurrency"
author = ["hackrole"]
date = 2020-11-04
lastmod = 2020-11-05T00:20:43+08:00
tags = ["Rust"]
draft = false
weight = 2003
+++

concurrent-programming: programs can run in independent with each other.
parallel programming: program can run at same time.

as a low-level language, rust need less abstraction and more control.


## use thread {#use-thread}

process vs thread

programs:

1.  Race conditions: data-race. resource-race.
2.  DeakLock
3.  difficult concurrent bug.

os-thread vs green-thread: 1:1 vs M:N

```rust
/// thread examples

/// when the main-thread exit, the fork-thread will exit too.
/// just like python thread.deamon flag.

use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from the spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {} from the main thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
}
```

````rust
/// use join to wait sub-thread finish
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from the spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        };
    });

    for i in 1..5 {
        println!("hi number {} from the main thread!", i);
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap();
}
```

thread vs move-closure

```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    /// this would raise, cause the `v` was a borrow-ref.
    /// it may be dropped before sub-thread. rust avoid you to do this.
    // let handle = thread::spawn(|| {
    //     println!("Here's a vector: {:?}", v);
    // });

    /// add `move` to move owner to sub-thread.
    let handle = thread::spawn(move || {
        println!("Here's a vector: {:?}", v);
    });

    /// the would made `v` not exists in sub-thread.
    /// if variables has been moved into sub-thread, this would raise too.
    // drop(v)


    handle.join().unwrap();
}
````


## pass msg between threads {#pass-msg-between-threads}

````rust
use std::thread;
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("HI");
        tx.send(val).unwrap();
    });

    let received = rx.recv().unwrap();
    println!("Got: {}", received);
}
````

````rust
use std::thread;
use std::sync::mpsc;
use std::time::Duratin;

fn single_send() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("Hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duratin::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {}", received);
    }
}

fn multi_send() {
    let (tx, rx) = mpsc::channel();

    // use clone to got multi sender
    let tx1 = mpsc::Sender::clone(&tx);
    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        let vals = vec![
            String::from("move"),
            String::from("messages"),
            String::from("for"),
            String::from("you"),
        ];
        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {}", received);
    }
}
````


## share-memory concurrent {#share-memory-concurrent}

channel is like single-owner ref.
share-memory is like multi-owner ref.
rust type-system and owner-rule can help correctly manage those.

mutex(互斥器) mutual-exclusion abbs.
mutex usually stay with data, use the lock to guarding its data.

correctly use mutex, you need

1.  request lock before use data.
2.  after use data, you must release the lock.

<!--listend-->

````rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(5);

    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }

    println!("m = {:?}", m);
}
````

````rust
/// multi-thread mutex example
// use std::rc:Rc;
use std::sync::{Mutex, Arc};
use std::thread;

fn main() {
    /// this would compile, cause counter with move cannot have multi-owner
    // let counter = Mutex::new(0);
    /// this would compile failed, cause Rc is not thread-safe.
    // let counter = Rc::new(Mutex::new(0));
    /// Arc is thread-safe Ac-Ref
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handlet = thread::spawn(move || {
            let mut num = counter.lock.unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
````

Mutex提供了类似Cell<T>的内部可变性，可以修改非mut类型的值.
Rust不能避免Mutex的所有逻辑错误.

````rust
/// TODO: add a dead-lock rust Mutex programming.
````

Mutex<T> vs MutexGuard<T>


## 使用Sync and Send trait的可扩展并发 {#使用sync-and-send-trait的可扩展并发}

Rust提供于golang相反的设计，语言本身不提供并发相关内容, 并发功能由库来提供和扩展。
然后有两个概念内嵌语言中: \`std::marker\`的 \`Sync\` 和 \`Send\` trait.

marker-trait: 标记类型, 不需要实现trait-method
implement this need write unsafe-rust-code.

1.  Send-Trait mark Type can move owner-right between thread.
2.  Almost all rust Type implement Send-Trait.
3.  Some speical example like Rc<T> is design for single-thread, Arc<T> is its thread-safe version.
4.  Any Type which contains only Send-Type auto become Send-Type.
5.  Sync-Trait mark Type can be used safely in multiple-thread env.
6.  for Type T, if &T is Send-Trait, T is Sync-Trait.
7.  Type make of Sync-Type auto become Sync-Type.
