# PyMarkup
[![Build Status](https://travis-ci.org/bluepython508/PyMarkup.svg?branch=master)](https://travis-ci.org/bluepython508/PyMarkup)
[![Documentation Status](https://readthedocs.org/projects/pymarkup/badge/?version=latest)](https://pymarkup.readthedocs.io/en/latest/?badge=latest)

An internal DSL for generating XML-like markup in Python 3.7

### Installation
Installation is as simple as `pip install pymarkup`.
To develop, download the source, and run `pip install -e .[dev]`

### Usage
A basic example:
```python
from pymarkup import MarkupBuilder

t = MarkupBuilder()

with t:  # <html> tag
    with t.h1(id='HelloWorld'):  # Attribute access creates new element, and call adds attributes to tag
        t + 'Hello World!'  # Add child text to tag

    with t.a(href="github.com"):
        t + t.img(src="i_am_an_image.png")  # Self-closing tags are added with +
    with t.ul:
        for x in range(2):
            with t.li:
                t + x
```
`repr(t)` gives:
```html
<html>
<h1 id="HelloWorld">
Hello World!
</h1>
<a href="github.com"><img src="i_am_an_image.png"/>
</a>
<ul>
<li>
0
</li>
<li>
1
</li>
</html>
```

For more information, see the [docs](https://pymarkup.readthedocs.io/en/latest/)