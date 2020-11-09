+++
title = "rust advance feature"
author = ["hackrole"]
date = 2020-11-08
lastmod = 2020-11-09T23:51:21+08:00
categories = ["Rust"]
draft = false
weight = 2006
+++

1.  unsafe-rust
2.  advance-trait
    -   trait-ref-type 与trait相关的关联类型
    -   default type param 默认参数类型
    -   fully qualified syntax 完全限定语法
    -   supertraits 超父类
    -   newtype模式
3.  advance-type
    -   more about new-type pattern
    -   type alias 类型别名
    -   never type
    -   dymatic-size type 动态大小类型
4.  advance function and closure
    -   function point 函数指针
    -   return closure 返回闭包
5.  macro 宏


## unsafe-rust {#unsafe-rust}

the-addional-super power of unsafe

1.  解引用裸指针
2.  调用不安全的函数或方法
3.  访问或修改可变静态变量
4.  实现不安全的trait
5.  访问union字段

**the _owner-check_ is still on**


### unref-raw-point {#unref-raw-point}

1.  ignore owner-rule, allow mut and immute ref.
2.  not ensure the point valid
3.  allow empty
4.  not implement auto-clean.

<!--listend-->

```rust
/// create immute and mut raw-point
/// you can create raw-point in safe-code, but can only deref it in unsafe code.
let mut num = 5;

let r1 = &num as *const i32;
let r2 = &mut num as *mut i32;

unsafe {
    println!("r1 is: {}", *r1);
    println!("r2 is: {}", *r2);
}

/// unsure validate raw-point
let address = 0x123456usize;
let r = address as &const i32;
```


### call unsafe function or method {#call-unsafe-function-or-method}

```rust
unsafe fn dangerous() {}

unsafe {
    dangerous();
}

/// can create safe-abstaction on unsafe-code
/// rust cannot understand ref twice
use std::slice;

fn split_at_mut(slice: &mut [i32], mid: usize) -> (&mut [i32], &mut[i32]) {
    let len = slice.len();
    let ptr = slice.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (slice::from_raw_parts_mut(ptr, mid),
         slice::from_raw_parts_mut(ptr.add(mid), len - mid))
    }
}
```


### use `extern` to call extern-code {#use-extern-to-call-extern-code}

**foreign function interface, FFI**
**applicaton binary interface, ABI**

```rust
extern "C" {
    fn abs(input: i32) -> i32;
}

/// export extern-function must add ~no_mangle~
#[no_mangle]
pub extern "C" fn call_from_c() {
    println!("Just called a rust function from c!", );
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```


### visit or modify mutable-static variable {#visit-or-modify-mutable-static-variable}

```rust
static mut COUNTER: u32 = 0;

fn add_to_count(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    add_to_count(3);

    unsafe {
        println!("COUNTER: {}", COUNTER);
    }
}
```


### implement unsaf-trait {#implement-unsaf-trait}

```rust
unsafe trait Foo {

}


unsafe impl Foo for i32 {

}
```


## advance-trait {#advance-trait}

`associated types`

```rust
pub trait Iterator {
    /// 占位类型
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}


impl Interator for Counter {
    /// unlike generic, this can only choose once.
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        // -snip-
    }
}

/// generic can implement multi-times,
/// and need add generic-param
pub trait Iterator<T> {
    fn next(&mut self) -> Option<T>;
}

impl Iterator<String> for Counter {
    fn next<String>(&mut self) -> Option<String> {
        // -snip-
    }
}

impl Iterator<u32> for Counter {
    fn next<u32>(&mut self) -> Option<u32> {
        // -snip-
    }
}
```

add default-type for Generic, A good example is Operator-overloading(运算符重载)
rust not allow create-op or overload-op, but can implement op list in  `std::ops`.

```rust
use std::ops::Add;

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

/// Add Trait
// RHS is default-type-paramters, 默认类型参数
trait Add<RHS=Self> {
    type Output;

    fn add(self, rhs: RHS) -> Self::Output;
}


/// default-type-paramters can
/// 1) extends type and not broke existing-code
/// 2) customer in most-people not-need situation
struct Millimeters(u32);
struct Meters(u32);

impl Add(Meters> for Millimeters {
    type Output = Millimeters;

    fn add(self, other: Meters) -> Millimeters {
        Millimeters(self.0 + (other.0 * 1000))
    }
}
```

完全限定语法与消除歧义: 调用相同名称的方法
rust neither can avoid traits has same method-name, nor can avoid implement the two traits for same type.

```rust
trait Pilot {
    fn fly(&self);
}

trait Wizard {
    fn fly(&self);
}

struct Human;

impl Pilot for Human {
    fn fly(&self){
        println!("This is your captain speaking.");
    }
}

impl Wizard for Human {
    fn fly(&self) {
        println!("Up!");
    }
}

impl Human {
    fn fly(&self) {
        println!("*waving arms furiously*");
    }
}


fn main() {
    let person = Human;
    /// this call method implement for type.
    person.fly();
    /// call method from certain trait
    Pilot::fly(&person);
    Wizard::fly(&person);
}
```

```rust
/// static-method or assoicate-method have no self-paramters.
/// so cannot use above method to call Trait-method.
/// you need to use *完全限定语法*
trait Animal {
    fn baby_name() -> String;
}

struct Dog;


impl Dog {
    fn baby_name() -> String {
        String::from("Spot")
    }
}

impl Animal for Dog {
    fn baby_name() -> String {
        String::from("puppy")
    }
}

fn main() {
    println!("A baby dog is called a {}", Dog::baby_name());
    // *完全限定语法* syntax <Type as Trait>::function(receiver_if_method, next_arg, ...);
    println!("A baby dog is called a {}", <Dog as Animal>::baby_name());
}
```

use other-trait functions in current trait. the depends-on trait also need tobe implemented.
the depends-on trait is supertrait of current-trait.

```rust
use std::fmt;

trait OutlinePrint: fmt::Display {
    fn outline_print(&self) {
        let output = self.to_string();
        let len = output.len();
        println!("{}", "*".repeat(len + 4));
        println!("*{}*", " ".repeat(len + 2));
        println!("* {} *", output);
        println!("*{}*", " ".repeat(len + 2));
        println!("{}", "*".repeat(len + 4));
    }
}


struct Point {
    x: i32,
    y: i32,
}

impl fnt::Display for Point {
    fn fmt(&self, &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

/// this world raise if not implement Debug-Trait
impl OutlinePrint for Point {}
```

newtype 模式用以在外部类型上实现外部trait, newtype was concept come from haskell. no speed punish in runtime.
you may need implement every-method in inner-type or implement-Deref trait.

```rust
use std::fmt;

struct Wrapper(Vec<String>);

impl fmt::Display for Wrapper {
    fn fmt(&selff, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

fn main() {
    let w = Wrapper(vec![String::from("hello"), String::from("world")]);
    println!("w = {}", w);
}
```
