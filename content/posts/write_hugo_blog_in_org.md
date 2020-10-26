+++
title = "writing Hugo blogin Org writing hugo blog in org"
author = ["hackrole"]
date = 2020-10-27
lastmod = 2020-10-27T00:53:13+08:00
tags = ["hugo", "org"]
categories = ["emacs"]
draft = true
weight = 2001
[menu.main]
  identifier = "writing-hugo-blogin-org-writing-hugo-blog-in-org"
  weight = 2001
+++

## first heading within the post {#first-heading-within-the-post}

-   this post will be exported as
    `content/posts/writing-hugo-blog-in-org-file-export.md`
-   its title will be "writing Hugo blog in org
-   it will have _hugo_ and _org_ tags and _emacs_ as category
-   the _lastmod_ property in the front-matter is set automatically to the time of export.
-   the menuitem _identifier_ is auto-set
-   the menu item _weight_ and post _weight_ if needed have to be manully specified as show abve.


### a sub-heading under the heading {#a-sub-heading-under-the-heading}

-   it's draft state will be marked as `true` because of `#+HUGO_DRAFT: true`.

with the point\_anywhere\_, do `C-c C-e H h` to export the whole file titled /Writing Hugo blog in org/to a hugo post.

the exported Markdown has a litter comment footer as set in the _local variables_ section below

it autosave now.
the title still not correct


## footnotes {#footnotes}
