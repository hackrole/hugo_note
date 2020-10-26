+++
author = ["hackrole"]
lastmod = 2020-10-27T01:23:15+08:00
draft = false
+++

## emacs {#emacs}

all posts in here will have category set to _emacs_


### <span class="org-todo todo TODO">TODO</span> writing hugo blog in org {#writing-hugo-blog-in-org}

:PROPERTIES:
:EXPORT\_FILE\_NAME: writing-hugo-blog-in-org-subtree-export
:EXPORT_DATE: 2020-10-29
:EXPORT\_HUGO\_MENU: :menu "main"
:EXPORT\_HUGO\_CUSTOM\_FRONT\_MATTER: :foo bar :baz zoo :alpha 1 :beta "two words" :gamma 10


#### first heading within the post {#first-heading-within-the-post}

-   this post will be exported as
    `content/posts/writing-hugo-blog-in-org-file-export.md`
-   its title will be "writing Hugo blog in org
-   it will have _hugo_ and _org_ tags and _emacs_ as category
-   the _lastmod_ property in the front-matter is set automatically to the time of export.
-   the menuitem _identifier_ is auto-set
-   the menu item _weight_ and post _weight_ if needed have to be manully specified as show abve.

<!--list-separator-->

-  a sub-heading under the heading

    -   it's draft state will be marked as `true` because of `#+HUGO_DRAFT: true`.

    with the point\_anywhere\_, do `C-c C-e H h` to export the whole file titled /Writing Hugo blog in org/to a hugo post.

    the exported Markdown has a litter comment footer as set in the _local variables_ section below

    it autosave now.
    the title still not correct


## footnotes {#footnotes}
