+++
title = "prepare"
author = ["代鹏"]
date = 2021-06-26
lastmod = 2021-07-01T13:20:29+08:00
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
