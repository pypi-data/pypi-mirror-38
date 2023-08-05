[![Build Status](https://travis-ci.org/yiwensong/illuminati_and_stuff.svg?branch=master)](https://travis-ci.org/yiwensong/illuminati_and_stuff)
[![Coverage Status](https://coveralls.io/repos/github/yiwensong/illuminati_and_stuff/badge.svg?branch=master)](https://coveralls.io/github/yiwensong/illuminati_and_stuff?branch=master)
[![PyPI version](https://badge.fury.io/py/illuminati-and-stuff.svg)](https://pypi.org/project/illuminati-and-stuff/)

# Illuminati and stuff

A pyramid tween that throws the traceback in the body of 500 responses.


## setup

Install this package (i.e. `pip install illuminati-and-stuff`) and run the
following where you have your pyramid configs:

```python
import illuminati_and_stuff
import pyramid

config = pyramid.config.Configurator()

...

config.add(illuminati_and_stuff)
```
