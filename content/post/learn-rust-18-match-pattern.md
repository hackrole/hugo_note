+++
title = "18 rust pattern"
author = ["hackrole"]
date = 2020-11-08
lastmod = 2020-11-10T15:55:41+08:00
categories = ["Rust"]
draft = false
+++

包括的内容:

1.  字面量 literal
2.  解构数组，枚举，结构提，元组等
3.  变量
4.  通配符
5.  占位符


## rust match {#rust-match}

rust `match` is exhaustive, all situation must be consided

\_ match all, and not bind to variable, use to ignore

`if let` use can only care abouot one situation

```rust
fn main() {
    let favorite_color: Option<&str> = None;
    let is_tuesday = false;
    let age: Result<u8, _> = "34".parse();

    if let Some(color) = favorite_color {
        println!("Using your favorite color, {}, as the backgourd", favorite_color);
    }else if is_tuesday {
        println!("Tuesday is green day!");
    }else if let Ok(age) = age {
        if age > 30 {
            println!("Using purple as the background color");
        }else{
            println!("using orange as the background color");
        }
    }else{
        println!("Using blue as the background color");
    }
}
```

`while let`

```rust
fn main() {
    let mut stack = Vec::new();
    stack.push(1);
    stack.push(2);
    stack.push(3);

    while let Some(top) = stack.pop() {
        println!("{}", top);
    }
}
```

`for`

```rust
let v = vec!['a', 'b', 'c'];

for (index, value) in v.iter().enumerate() {
    println!("{} is at index", value, index);
}
```

`let`

```rust
let (x, y, z) = (1, 2, 3);
/// below will raises
let (x, y) = (1, 2, 3);
```

**function pattern**

```rust
fn print_coordinates(&(x, y): &(i32, i32)) {
    println!("Current location: ({}, {})", x, y);
}

fn main() {
    let point = (3, 5);
    print_coordinates(&point);
}
```


## irrefutable vs refutable {#irrefutable-vs-refutable}

1.  function, let, for only accept **irrefutable-pattern**
2.  if let, while let only accept **refutable-pattern**


## match example {#match-example}

```rust
/// match literal
let x = 1;

match x {
    1 => println!("one");
    2 => println!("two");
    _ => println!("anything");
}

/// variable, take case the ~variable scope~
let x = Some(5);
let y = 10;

match x {
    Some(50) => println!("Got 50");
    Some(y) => println!("Matched, y = {:?}", y);
    _ => println!("Default case, x = {:?}", x);
}
println!("x = {:?}, y = {:?}", x, y);

/// multi pattern
let x = 1;
match x {
    1 | 2 => println!("one or two");
    3 => println!("three");
    _ => println!("anything");
}

/// use ~..=~ to match range
/// *range-match* only accept number or char.
let x = 5;
match x {
    1..=5 => println!("one throught five");
    'a'..='j' => println!("a->j");
    _ => println!("something else");
}
```

\_ vs \_name vs ..

1.  \_ not bind, \_name bind (may transfer variable owner)
2.  .. use to match many

**match guard**

```rust
let num = Some(4);

match num {
    Some(x) if x < 5 => println!("less than five: {}", x),
    Some(x) => println!("{}", x),
    Noe => (),
}
```

**@ bind**

```rust
enum Message {
    Hello {id: i32},
}

let msg = Message::Hello {id: 5};

match msg {
    Message::Hello {id: id_variable @ 3..=7} => {
        println!("Found an id in range: {}", id_variable);
    },
    Message::Hello {id: 10..=12} => {
        println!("foun an id in another range");
    },
    Message::Hello {id} => {
        println!("Found some other id: [}", id);
    }
}
```
