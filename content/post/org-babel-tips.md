+++
title = "tips while using org-babel"
author = ["hackrole"]
date = 2020-10-27
lastmod = 2021-07-26T15:54:06+08:00
tags = ["org", "org-babel"]
categories = ["emacs"]
draft = false
+++

## multiple block tangle to single file {#multiple-block-tangle-to-single-file}


### first format {#first-format}

use \`:noweb yes\` and variable as placeholder.
write code block with header \`:noweb-ref <placeholder variable>\`

```elisp
<<config>>

<<next-config>>
```

```elisp
(println "hello")
```

```elisp
(println "this following")
```

```elisp
(println "this is another ways")
```


### use name and collect {#use-name-and-collect}

<a id="code-snippet--init"></a>
```emacs-lisp
(setq msg "Never a foot too far, even.")
```

<a id="code-snippet--msg"></a>
```emacs-lisp
(message msg)
```

<a id="code-snippet--goodbye"></a>
```emacs-lisp
(message "good bye")
```

```text
good bye
```

```emacs-lisp
<<init>>

<<msg>>

<<goodbye>>
```

```text
good bye
```
