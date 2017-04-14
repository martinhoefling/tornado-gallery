[![Build Status](https://travis-ci.org/martinhoefling/tornado-gallery.svg?branch=master)](https://travis-ci.org/martinhoefling/tornado-gallery)
[![Requirements Status](https://requires.io/github/martinhoefling/tornado-gallery/requirements.svg?branch=master)](https://requires.io/github/martinhoefling/tornado-gallery/requirements/?branch=master)

# tornado-gallery

*Image gallery and rating server.*

tornado-gallery serves a specified directory structure containing images / galleries to modern web browsers.

## Current Features:

 * Images are resized or served from cache on the fly to minimize bandwidth usage.
 * Image ratings are displayed and stored back in image xmp section.
 * Asynchronous request handling, resizing of images in multiple processes.
 * Preloading of next and previous image in browser.


## Technical Information

The backend is based on [tornado](http://tornadoweb.org) web framwork from facebook/friendfeed.
[Pillow](https://github.com/python-pillow/Pillow) is used for image editing while [python-xmp-toolkit](https://code.google.com/p/python-xmp-toolkit/) is employed to read/write metadata.
Polymer is used for the frontend.

## Basic Installation

* Make sure that exempi library used by python-xmp-toolkit is installed (e.g. via brew or apt). Further bower (and nodejs) is requiered to fetch the frontend.
* Create a python virtualenv and install (dev-)requirements.txt
* Create wrapper script via `python setup.py develop` or start app.py in tgallery package.
* `bower install` fetches frontend dependencies
* Navigate to http://localhost:1234/

... or use the Dockerfile to create a docker image.

## Running as docker container

Pull image via `docker pull martinhoefling/tornado-gallery`, then start container
```
docker run -ti -v /home/martin/Pictures:/gallery martinhoefling/tornado-gallery
```

## ToDo / missing features:

* Image Cache Cleanup
* Authentication
