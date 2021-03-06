+++
title = "prepare"
author = ["hackrole"]
date = 2021-06-26
lastmod = 2021-06-28T22:59:55+08:00
tags = ["SICP"]
draft = true
weight = 2001
+++

## env prepare {#env-prepare}


### install racket {#install-racket}

```bash
# on ubuntu
sudo apt install racket
```


### install sicp package {#install-sicp-package}

```bash
# on ubuntu
raco install sicp
# or on drracket package-manager search for sicp and install
# GUI handle
```


### racket get-starting {#racket-get-starting}

the \`#lang sicp\` at the beginning


#### using drracket, GUI handle {#using-drracket-gui-handle}


#### using racket shell {#using-racket-shell}

the \`#lang sicp\` not work in racket shell.
define it in the file, and load the file by
\`(enter! "filename.rkt")

or using
\`(load "filename.rkt")
which seems not work with \`#lang define\`


#### racket shell script {#racket-shell-script}

```bash
chmod +x filename.rktl
./filename.rktl
```

```racket
## filename: example.rktl
#! /usr/bin/env racket
(define (exract str)
  (substring str 4 7))
(extract "the dog out")
```


#### racket script {#racket-script}

```racket
;; filename: example rktl
#lang sicp

(define (add x y)
  (+ x y))
(add 1 2)
```


#### package racket programming into executable {#package-racket-programming-into-executable}

1.  drracket Racket|create executable
2.  raco exe <filename.rkt>
3.  shell-script mode


#### <span class="org-todo todo TODO">TODO</span> go-through the racket guide {#go-through-the-racket-guide}

[racket get-started](https://docs.racket-lang.org/getting-started/index.html#%28part.%5Ftop%29)

[racket guide](https://download.racket-lang.org/releases/8.1/doc/guide/intro.html)

<!--list-separator-->

- <span class="org-todo todo TODO">TODO</span>  how-to debug programming


### the SICP site {#the-sicp-site}


#### the offical site {#the-offical-site}

<https://link.zhihu.com/?target=https%3A//mitpress.mit.edu/sicp/>


#### the execise answers {#the-execise-answers}

[sicp offical solution](http://community.schemewiki.org/?sicp-solutions)

[the sicp execise answers chinese](https://sicp.readthedocs.io/en/latest/)


#### ref site {#ref-site}

[blog about get-started](https://zhuanlan.zhihu.com/p/34313034)


## <span class="org-todo todo TODO">TODO</span> the first captial of sicp: 构造过程抽象 {#the-first-captial-of-sicp-构造过程抽象}


### 程序设计的基本元素 {#程序设计的基本元素}


#### 基本元素: {#基本元素}

1.  基本的表达式
2.  组合的方法
3.  抽象的方法,为组合对象命名


#### 过程与数据 {#过程与数据}


#### 求值过程 {#求值过程}

求值过程由过别特殊形式和一般性求值规则组成.

特殊形式如: define, if, cond, and, or

一般求值规则: 求值子表达式，将子表达式应用最左的表达式，直到结果为基本表达式,如数，字符串等求值为自身的对象(可理解为特殊规则?）

环境为程序求值提供上下文.


#### 求值的代换模型 {#求值的代换模型}

不是实际解释器使用的模型，为方便理解而建立，后续会介绍更精

计算机程序必须是有效可行的


#### 过程作为黑箱抽象 {#过程作为黑箱抽象}

作用域和可见性. 自由变量和约束变量
内部定义和块结构

<!--list-separator-->

- <span class="org-todo todo TODO">TODO</span>  词法作用域???


### 过程与他们产生的计算 {#过程与他们产生的计算}

能看清所考虑动作的后果的能力，对成为程序专家至关重要

算法的空间复杂度和时间复杂度


#### 线性递归和迭代 {#线性递归和迭代}

递归很多时候很符合程序的运行方式，所以为一个过程书写递归过程会更自然简单。
lisp中在未介绍循环结构时，一般用尾递归程序来实现迭代计算。

尾递归在部分语言中会被优化，不会导致程序栈的增长

尾递归一般的条件是函数的返回为基本表达式或一个函数调用, 如果返回的是一个组合表达式，则一般无法做尾递归优化.
所以实现尾递归优化的策略一般是将状态作为一个参数传给递归函数。

```racket
;; 非尾递归
(define (factorial n)
  (if (= n 1)
      1
      (* n (factorial (- n 1)))))

;; 尾递归
(define (factorial n)
  ;; 中间状态作为参数传递给递归函数
  (define (fact-iter product counter max-count)
    (if (> counter max-count)
        product
        (fact-iter (* counter product)
                   (+ counter 1)
                   max-count)))
  (fact-iter 1 1 n))
```

```racket
(define (dec a)
  (- a 1))

(define (inc a)
  (+ a 1))

;; 非尾递归
(define (+ a b)
  (if (= a 0)
       b
       (inc (+ (dec a) b))))

;; 尾递归
(define (+ a b)
  (if (= a 0)
      b
      (+ (dec a) (inc b))))
```

```racket
#lang sicp

;; Ackermann函数
;; 作用????
(define (A x y)
  (cond ((= y 0) 0)
        ((= x 0) (* 2 y))
        ((= y 1) 2)
        (else (A (- x 1)
                 (A x (- y 1))))))

;; 2n
(define (f n) (A 0 n))
;; 2^n
(define (g n) (A 1 n))
;; 2^(2n)
(define (h n) (A 2 n))
```


#### 树形递归 {#树形递归}

树形递归虽然效率不高，但是一般易于实现，优化的迭代版本一般难以实现。

一般递归函数都可以通过在程序中包含一个队列或栈的方式来通过迭代版本实现，原理基本就是用一个特定数据结构模拟的递归中栈的效果.

另一种方式称为: 表格技术或记忆技术，原理为通过缓存中间计算结果来减少需要做的计算，但是需注意。程序最终仍然会触发2^n次调用，
只是重复调用不再需要重复计算，而是从缓存中直接获取，所以这种方法对计算相对耗时时效果才比较好.

<!--list-separator-->

-  fib

    1.  fibonacci数的递归版本，算法复杂度为2^n. 树形递归
    2.  迭代版本算法复杂度为n.
    3.  一次性计算版本为求值: ((1 + sqrt(5)) / 2) ^ n) / (sqrt 5)的底

    <!--listend-->

    ```racket
    ;; 递归版本
    (define (fib n)
      (cond ((= n 0) 0)
            ((= n 1) 1)
            (else (+ (fib (- n 1))
                     (fib (- n 2))))))

    ;; 迭代版本
    (define (fib2 n)
      (define (fib-iter a b count)
        (if (= count 0)
            b
            (fib-iter (+ a b) a (- count 1))))
      (fib-iter 1 0 n))
    ```

    ```racket
    #lang sicp

    ;; 换零钱的方式
    ;; 等价的非递归版本将难实现
    ;; 算法思想: 总数 = (现金换成除第一种硬币的数目) + (现金-第一种货币面值后换成所有货币的数目). 递归
    (define (count-change amount)
      (cc amount 5))

    (define (cc amount kinds-of-coins)
      (cond ((= amount 0) 1)
            ((or (< amount 0) (= kinds-of-coins 0)) 0)
            (else (+ (cc amount (- kinds-of-coins 1))
                     (cc (- amount
                            (first-denomination kinds-of-coins))
                         kinds-of-coins)))))

    (define (first-denomination kinds-of-coins)
      (cond ((= kinds-of-coins 1) 1)
            ((= kinds-of-coins 2) 5)
            ((= kinds-of-coins 3) 10)
            ((= kinds-of-coins 4) 25)
            ((= kinds-of-coins 5) 50)))
    ```

<!--list-separator-->

-  求幂运算

    求幂运算可以通过 二分法 得出一个 logN时间复杂度的算法

    ```racket
    ;; 递归版本
    (define (expt b n)
      (if (= n 0)
          1
          (* b (expt b (- n 1)))))

    ;; 迭代版本
    （define (expti b n)
      (define (expt-iter b counter product)
        (if (= counter 0)
            product
            (expt-iter b
                       (- counter 1)
                       (* b product))))

      (expt-iter b n 1))

    ;; 二分法,递归

    (define (even? n)
      (= (remainder n 2) 0))

    (define (fast-expt b n)
      (cond ((= n 0) 1)
            ((even? n) (square (fast-expt b (/ n 2))))
            ((else (* b (fast-expt b (- n 1)))))))

    ;; TODO 二分法, 迭代??
    (define (fast-expti b n)
      (define (fast-expt-iter b n product)
        (cond ((= n 0) product)
              ((even? n) (fast-expt-iter (* b b) (/ n 2) product))))
      (fast-expt-iter 0 1 1))
    ```

<!--list-separator-->

- <span class="org-todo todo TODO">TODO</span>  最大公约数

    欧几里德算法
    GCD(a, b) = GCD(b, r) ;; r = a mod b

    ```racket
    #lang siip

    ;; TODO exec 1.19, 1.20
    (define (gcd a b)
      (if (= b 0)
          a
          (gcd b (remainder a b))))
    ```

<!--list-separator-->

-  素数检测

    1.  寻找因子: 2 -> sqrt(n)
    2.  费马定理, 概率方法.

        ```racket
        ;; 寻找因子
        (define (smallest-divisor n)
          (find-divisor n 2))
        (define (find-divisorn test-divisor)
          (cond ((> (square test-divisor) n) n)
                ((divides? test-divisor n) test-divisor)
                (else (find-divisor n (+ test-divisor 1)))))

        (define (divides? a b)
          (= (remainder b a) 0))
        (define (prime? n)
          (= n (smallest-divisor n)))

        ;; 费马定理
        (define (expmod base exp n)
          (cond ((= exp 0) 1)
                ((even? exp)
                 (remainder (square (expmod base (/ exp 2) m))
                            m))
                (else
                 (remainder (* base (expmod base (- exp 1) m))
                            m))))

        (define (fermat-test n)
          (define (try-it a)
            (= (expmod a n n) a))
          (try-it (+1 (random (- n 1)))))

        (define (fermat-prime? n times)
          (cond ((= times 0) true)
                ((fermat-test n) (fast-prime? n (- times 1)))
                (else false)))
        ```


### <span class="org-todo todo TODO">TODO</span> 用高阶函数做抽象 {#用高阶函数做抽象}

高阶过程: 已过程为参数或返回过程的函数.

高阶过程可以增强语言的表达能力, 为公共模式命名

一般的OFP编程思想，如map/filter/reduce, 比较常用与集合数据或数学和式等.

也可用于抽象多个函数的共用部分，将非共用部分作为lambda传入，但是需要注意不应已破坏函数的可读性为代价,
比较好的思路就是看拆分后仍否可以方便为为函数命名

同时要关注如何将递归风格的高阶过程转化为迭代风格

高阶过程可理解为过程抽象的技术，通过抽取相似过程，来提供抽象程度和提高代码复用性。
但是要注意最终目的是为了程序的可读性，过度抽象不可取

这里通过对几个过程观察，可以提取出通用的sum过程，并进一步提取出更通用的累积过程accumerate.

```racket
#lang sicp

(define (sum-itergers a b)
  (if (> a b)
      0
      (+ a (sum-itergers (+ a 1) b))))

(define (sum-cubes a b)
  (if (> a b)
      0
      (+ (cube a) (sum-cubes (+ a 1) b))))

(define (pi-sum a b)
  (if (> a b)
      0
      (+ (/ 1.0 (* a (+ a 2))) (pi-sum (+ a 4) b))))


;; 和式sum, next用于算出下一项
(define (sum term a next b)
   (if (> a b)
       0
       (+ (term a)
          (sum term (next a) next b))))

(define (inc n) (+ n 1))
(define (sum-cubers-2 a b)
  (sum cube a inc b))

(define (identity x) x)
(define (sum-intergers-2 a b)
  (sum identity a inc b))

(define (pi-sum-2 a b)
  (define (pi-term x)
    (/ 1.0 (* x (+ x 2))))
  (define (pi-next x)
    (+ x 4))
  (sum pi-term a pi-next b))
```


#### 抽象选择的多样性 {#抽象选择的多样性}

这里可以看出抽象选择的多样性，
如果文中提供的抽象都是对区间 [a, b]和next函数来逐次迭代来获取所有值。

另一种方法，如实现一个数据生产器或迭代器（更主流的设计思路),组合map/reduce/filter过程
代码可读性可能更好些


### <span class="org-todo todo TODO">TODO</span> 函数零点和不动点 {#函数零点和不动点}

基于渐进的思路来寻找函数的解，需要注意过程是可收敛的，已经收敛的速度

渐进的思路一般为二分法，是二分查找的基础

可以使用辅助方法来帮助函数收敛，如平均阻尼等.

进一步函数零点和不动点的操作可以对很多可表示为函数的过程的通用操作，如


## <span class="org-todo todo TODO">TODO</span> the second captial of sicp: 构造数据抽象 {#the-second-captial-of-sicp-构造数据抽象}


### 数据抽象导论 {#数据抽象导论}


### 层次性数据和闭包的性质 {#层次性数据和闭包的性质}
