+++
title = "using ob-ipython as alternative of jupyter"
author = ["hackrole"]
date = 2020-12-06
lastmod = 2020-12-05T20:04:39+08:00
tags = ["ob-ipython", "jupyter", "bokeh", "org-mode"]
categories = ["emacs"]
draft = false
+++

## ob-ipython introduce {#ob-ipython-introduce}

[ob-ipython repo](https://github.com/gregsexton/ob-ipython)

ob-ipython是基于org-babel,提供了一个在org-mode下做类似jupyter-notebook体验的开发模式.
用来快速做代码尝试或一个pandas数据分析很长合适.

为什么不使用原声的jupyter呢?

1.  基于browser的jupyter使用体验并不好.

按键配置和补全,snippets等等都是致命伤，这让jupyter notebook用起来更像个toy-project.

1.  org-mode天生强大的功能配合ob-babel, ob-ipython.
    org-mode强大的文件编辑功能自不必说, 这种方式也比原生的代码里套markdown的方式更舒服.
    配合上可以使用emacs所有的增强功能.

2.  literal-programming的正确使用方式.


## 支持的特性 {#支持的特性}

1.  内嵌pandas, matplotlib图片和表格数据
2.  org-mode variable
3.  导出功能export
4.  multi-language??
5.  jupyter-kernel support??
6.  working with a remote session??
7.  在代码中打开REPL to play with.
8.  org literal-programming with :tang supported.


## install in spacemacs {#install-in-spacemacs}


### first add **ob-ipython** to spacemacs **dotspacemacs-additional-packages** {#first-add-ob-ipython-to-spacemacs-dotspacemacs-additional-packages}


### install jupyter {#install-jupyter}

```shell
pip install jupyter
```


### config ob-ipython in spacemacs \`user-config\` {#config-ob-ipython-in-spacemacs-user-config}

```elisp
(with-eval-after-load 'org
  (add-to-list 'org-babel-load-languages '(ipython . t))
  (add-to-list 'org-babel-load-languages '(rust . t))
  ;; 不再询问是否允许执行代码块
  (setq org-confirm-babel-evaluate nil)
  ;; displace/update images in the buffer after I evaluate
  (add-hook 'org-babel-after-execute-hook 'org-display-inline-images 'append))
```


### add snipet for conversation {#add-snipet-for-conversation}

```snippet
# -*- mode: snippet -*-
# name: ipython block
# key: srcip
# --
#+BEGIN_SRC ipython :session ${1::ipyfile ${2:$$(let ((temporary-file-directory "./")) (make-temp-file (concat (file-name-sans-extension (file-name-nondirectory buffer-file-name)) "-py") nil ".png"))} }:exports ${3:both} :results raw drawer
$0
#+END_SRC
```


## use example and tips {#use-example-and-tips}


### 使用maptlotlib inline来保证图片输出 {#使用maptlotlib-inline来保证图片输出}

```ipython
%matplotlib inline
import matplotlib.pylot as plt
import numpy

plt.hist(np.random.randn(20000), bins=200)
```


### 使用ipyfile来控制生成的图片 {#使用ipyfile来控制生成的图片}
