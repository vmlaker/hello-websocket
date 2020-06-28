hello-websocket
===============
Webcam over websocket in Python using OpenCV and
`Tornado <http://www.tornadoweb.org>`_.

How it works
------------
A *recorder* process continuously reads images from a webcam.
Upon every capture, it writes the image to a Redis key-value store.

A separate *server* process (running Tornado) handles websocket requests
sent by a *client* (web browser). Upon receiving a request, it retrieves
the latest image from the Redis database and sends it to the client over the
established websocket connection.

.. image:: https://github.com/vmlaker/hello-websocket/blob/master/diagram.png?raw=true

The *client* web page is dead simple: 
It sends an initial request on a websocket.
When image data arrives, it assigns it to ``src`` attribute of the
``<img>`` tag, then simply sends the next request. That's it!

Installation
------------
The code uses Python in a virtualenv. Since OpenCV is not officially in the
`Python Package Index <http://pypi.org>`_, we manually copy the system OpenCV
library into the virtualenv.

First, install OpenCV for Python system-wide:
::

   apt-get install python-opencv

Also install Redis server:
::

   apt-get install redis-server

Build the virtual environment with all needed modules:
::

   make

Usage
-----
Two separate programs need to be running: 1) the *recorder* which captures
and writes to Redis database, and 2) the *server* which reads the current
image from the database and serves to requesting WebSocket clients.

Run the *recorder*:
::

   make recorder

Now (in a different shell) run the *server*:
::

   make server
   
Go to http://localhost:9000 to view the webcam.
