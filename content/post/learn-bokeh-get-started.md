+++
title = "quick-start"
author = ["hackrole"]
date = 2020-11-17
lastmod = 2020-11-18T00:45:51+08:00
series = ["bokeh"]
categories = ["bokeh"]
draft = false
weight = 2001
series: = ""
+++

bokeh can provide **interactive visualization** for **modern web browsers**.
**elegant**, **concise**, **vesatile graphics**,
\*afford high-performacne interactiivity onver lagerge or streaming datasets.

bokeh provide two interface levels:

1.  bokeh.models: low-level interface provide most flexibility
2.  bokeh.plotting: higher-level interface centered around composing visual glyphs.

this focus on `bokeh.plotting`.


## installation {#installation}

```shell
# recommend way
# conda install deps, and exmaples in *examples/* subdirectory
conda install bokeh

# using pip, you need install ~numpy~ and so on.
pip install bokeh
```


## get-starting {#get-starting}

-   [] TODO output bokeh plot to or-babel result
-

you can download sample-date and example from bokeh

`bokeh sampledata`

the general steps of bokeh.ploting:

1.  prepare data
2.  tell bokeh where to generate output(file or notebook)
3.  call figure() to create a plot figure
4.  add renderers, to add renderers to figure, such as ==
5.  call `show()` or `save()` to output results

<!--listend-->

<a id="code-snippet--first exmaple to get-started"></a>
```ipython
from bokeh.plotting import figure, output_file, show, output_notebook

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# output to static html file
# ??? how to use in web-server like flask.
# output_file("lines.html")
# output_notebook()

# create a new plot with a litter and axis labels
p = figure(title="simple line example", x_axis_label="x", y_axis_label="y")

# add a line renderer with legend and line thickness
p.line(x, y, legend_label="Temp.", line_width=2)

# show the results
show(p)
```

bokeh work well with **jupyter-notebook**.
**jupyter-notebook** is the common tool for exploratory data analysis, widely used across the pyData community.
you can view online [Bokeh NBViewer Gallery](http://nbviewer.ipython.org/github/bokeh/bokeh-notebooks/blob/master/index.ipynb), or **examples/howto** in the [Bokeh Repo.](https://github.com/bokeh/bokeh)

TODO notebook:

1.  [bokeh interact with jupyter's dropdown and sliders](https://github.com/bokeh/bokeh/tree/2.2.3/examples/howto/notebook%5Fcomms/Jupyter%20Interactors.ipynb)
2.  [use Numba to efficiently perform image processing](https://github.com/bokeh/bokeh/tree/2.2.3/examples/howto/notebook%5Fcomms/Numba%20Image%20Example.ipynb)

bokeh notebook cannot display in **Github** preveiw, cause bokeh using javascript for display which was scrub by Github.


## concept {#concept}


### Plot {#plot}

central concept in Bokeh, containers that hold all the various objects (renderers, guides, data, and tools)

??? the `figure()` return object


### Glyph {#glyph}

basic visual marks that bokeh can display.
??? the `line()` `plot()` returns

1.  at low-level, there are **glyph objects**, such as `Line` on the `bokeh.models` interface
2.  at higher-level, there are **glyph methods** such as `line()` provided by `bokeh.plotting` interface.


### Guides and Annotations {#guides-and-annotations}

tools component that aid presentation or help user make comparisions.


#### Guide {#guide}

visual aids help user judge distances, angles etc.
such as grid-lines(珊格线) or bands(???布林线), axes(轴线, linear, log, datetime)


#### annotations {#annotations}

visual aids that label or name parts of the plot.
such as titles, legends(图例) etc.


### Ranges {#ranges}

the data-space bounds of a plot.

by default of `bokeh.plotting` interface,
it give `DataRange1d` that try to automatically set the plot bounds to encompass all the available data.

<a id="code-snippet--explicit set fixed-range-bound"></a>
```ipython
p = figure(x_range=[0, 10], y_range=(10, 20))
```


### Resources {#resources}

the generate **bokeh output**, such as html-file or notebook.

bokeh default load **bokehjs** from cdn.bokeh.org, you can embedeed it static by ==


## <span class="org-todo todo TODO">TODO</span> more-exampels {#more-exampels}


### Vectorized colors and sizes {#vectorized-colors-and-sizes}


### Linked Panning and Brushing {#linked-panning-and-brushing}


### DateTiem axes {#datetiem-axes}


## <span class="org-todo todo TODO">TODO</span> Bokeh applications {#bokeh-applications}

check-over this [run bokeh server](https://docs.bokeh.org/en/latest/docs/user%5Fguide/server.html)

bokeh comes with an optional server-component, the **Bokeh Serevr**.

it affords many novel and powerful capabilities:

1.  UI widgets and plot selections driving computations and plot updates.
2.  Intelligent server-side downsampling of large datasets.
3.  Streaming data automatically updating plots.
4.  Sophisticated glyph re-writing and transformations for “Big Data”.
5.  Plot and dashboard publishing for wider audiences.
