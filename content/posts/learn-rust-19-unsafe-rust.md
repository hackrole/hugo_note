+++
title = "rust advance feature"
author = ["hackrole"]
date = 2020-11-08
lastmod = 2020-11-08T22:41:00+08:00
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
