hello-websocket
===============

Webcam over WebSocket using OpenCV and 
`Tornado <http://www.tornadoweb.org>`_.

Installation
------------

First install OpenCV Python bindings system-wide.
::

   yum install opencv-python

Build Python virtual environment with all needed modules:
::

   make

Usage
-----

Run the server:
::

   make server

Go to http://localhost:9000.
