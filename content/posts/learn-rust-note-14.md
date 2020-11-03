+++
title = "14章命名空间"
author = ["hackrole"]
date = 2020-11-01
lastmod = 2020-11-02T23:28:09+08:00
tags = ["Rust"]
draft = true
weight = 2001
+++

workspace(工作空间)讲多个crates合并到一个项目中,

是否有只能有多个bin-crate和一个lib-crate限制?

```toml
// add/Cargo.toml
// workspace need a special Cargo.toml which only contains workspace
[workspace]
members = [
    "adder"
]

// every project in current workspace need own Cargo.toml
// projects will share root directory Cargo.lock to make
// every project have same lib versioin.
[depencencies]
add-one = { path: "../add-one"}
```

```rust
// add-one/lib.rs
pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(3, add_one(2))
    }
}
```

```rust
// adder main.rust
use add_one;

fn main(){
    let num = 10;
    println!("Hello, world! {} plus one is {}!", num, add_one::add_one(num));
}
```

使用cargo build -p <project>来build特定项目

发布需要进入每个单独的项目做发布，没有-p/--all参数


## cargo install {#cargo-install}

\`cargo install\` 默认安装到~/.carog/bin目录，只能安装bin-crates.


## cargo submodule {#cargo-submodule}

定义命令名为cargo-<command>的命令可以作为cargo子命令运行
