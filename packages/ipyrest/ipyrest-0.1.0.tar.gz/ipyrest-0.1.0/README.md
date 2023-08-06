# Ipyrest

[![Binder](https://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/deeplook/ipyrest/master) 
[![Nbviewer](https://github.com/jupyter/design/blob/master/logos/Badges/nbviewer_badge.svg)](http://nbviewer.jupyter.org/github/deeplook/ipyrest/tree/master/)
[![Travis-CI](http://img.shields.io/travis/deeplook/ipyrest.svg)](https://travis-ci.org/deeplook/ipyrest)
  
Ipyrest is an emerging Jupyter notebook widget for exploring RESTful APIs. It has two main goals: provide a more convenient interface in the spirit of Postman, and allow for plug-in components, starting with output renderers for various MIME types, e.g. GeoJSON:

![banner](images/banner.png "")

Features
--------

Ipyrest deals with the following concepts, implementated to varying degrees: Server, Service, Request, Response, Data, MIME-Type, Compression, Logging, Caching, Time-Out, Errors, Viewing, Plugins, Testing, and UI.

At the moment the following plugins are available for rendering output from HTTP responses in common formats: Plain Text, CSV, HTML, Bitmaps, SVG, JSON, GeoJSON, GPX, Protobuf, (and some experimental 3D stuff).

The main direct dependencies are: Python >= 3.6, jupyter (incl. lab), ipywidgets, ipyleaflet, ipyvolume, geojson, qgrid, protobuf, timeout_decorator, requests, vcr, mypy, pytest, 

Installation
------------

Released versions of Ipyrest can be installed from PyPI with (as soon as available):

```
pip install ipyrest
```

Development versions of Ipyrest can be installed either directly from GitHub or after downloading/cloning and unpacking like this in its top-level directory:

```
pip install git+https://github.com/deeplook/ipyrest

pip install -e .
```

Testing
-------

Just make sure you have `pytest` installed and run `PYTHONPATH=. pytest -s -v tests` in the root directory. Some tests will automatically start a local webserver in `tests/api_server.py` which implements a set of sample API endpoints for local testing.

Some tests need keys/tokens defined as environment variables for the respective APIs being tested. If not present these tests will be skipped.

Documentation
-------------

The `docs` folder is only a stub for now. At the moment it is recommended to look at [`examples/meetup.ipynb`](examples/meetup.ipynb), mostly a tutorial-like collection of examples given as a presentation at a meetup. Some of these need appropriate API keys.

How to Contribute
-----------------

More to come...
