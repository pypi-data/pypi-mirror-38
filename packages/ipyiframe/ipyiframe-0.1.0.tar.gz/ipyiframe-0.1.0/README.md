# Jupyter custom ipywidget: **ipyiframe**

[![Latest Version](https://img.shields.io/pypi/v/ipyiframe.svg)](https://pypi.python.org/pypi/ipyiframe/)
[![Downloads](https://img.shields.io/pypi/dm/ipyiframe.svg)](https://pypi.python.org/pypi/ipyiframe/)

## 1 - Overview

This repo contains the source code and the building scripts for **ipyiframe** a custom [ipywidget](https://ipywidgets.readthedocs.io/en/stable/).

It enables to iframe any content passed as srcdoc from a Jupyter notebook - classic or JupyterLab - which can then be exported as standalone html with the ipywidget export machinery.

Under the hood, it uses the [iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe) HTML element.  
Note that the `sandbox` property is set to `allow-scripts` which forces isolation therefore guarantees security.  
Additionally scaling of the iframed content is possible.

<div style="display:block; margin: 0 auto; text-align:center">
<img src="img/demo-ipyiframe.gif" width="700">
</div>

## 2 - Install

## 2.1 - User Install

From terminal:

```bash
# for notebook >= 5.3
$ pip install ipyiframe

# for notebook < 5.3
$ pip install ipyiframe
$ jupyter nbextension install ipyiframe --py --sys-prefix
```

## 2.2 - Developer Install

From terminal:

```bash
$ git clone https://gitlab.com/oscar6echo/ipyiframe.git
$ cd ipyiframe/js
$ npm install
$ npm run watch # in another terminal
$ cd ..
$ pip install -e .
$ jupyter nbextension install --py --symlink --sys-prefix ipyiframe
$ jupyter nbextension enable --py --sys-prefix ipyiframe
```

# 3 - Use

```python
from IPython import display
from ipyiframe import Iframe

# let url be a valid url
# let content be a str

f = Iframe(
    # url - default to None
    src=url
    # content - default to None
    # exactly one of src and srcdoc can be passed
    srcdoc=content,
    # width in CSS px - from the content page
    width=700,
    # height in CSS px - from the content page
    height=750,
    # CSS for iframe border attr
    border='1px gray solid',
    # CSS for iframe margin attr
    margin='',
    # CSS for iframe padding attr
    padding='1px',
    # iframe scrolling attr
    scrolling='no'
    # scaling factor - default to 1.0
    scale=0.6,
    # transform-origin param - default to 'top left'
    transform_origin='top center'
)
display(f)
```

See the [demo notebook](https://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/ipyiframe/raw/master/notebooks/demo-ipyiframe.ipynb) on [nbviewer](https://nbviewer.jupyter.org/).
