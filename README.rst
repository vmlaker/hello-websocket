hello-websocket
===============

Webcam over websocket in Python, using OpenCV and 
`Tornado <http://www.tornadoweb.org>`_.

Details
-------

A *recorder* process continuously reads images from a webcam.
Upon every capture, it writes the image to a Redis key-value store.

A separate *server* process (running Tornado) handles websocket requests
sent by the *client*, i.e. web browser. Upon receiving the request, it retrieves
the latest image from the Redis database and sends it to the client over the
established websocket connection.

.. image:: https://github.com/vmlaker/hello-websocket/blob/master/diagram.png?raw=true

The *client* web page is dead simple: 
It sends an initial request on a websocket.
When image data arrives, it assigns it to ``src`` attribute of the
``<img>`` tag, then simply sends the next request. That's it!

Installation
------------

The code uses Python and third-party modules installed in a 
``virtualenv``. But since OpenCV is not part of the Python Package Index,
you're gonna need to install it system-wide. (Later below, *make* will
manually pull the library into the virtual environment):
::

   apt-get install python-opencv

Also install Redis server:
::

   apt-get install redis-server

Now go ahead and grab the source code repo:
::

   git clone https://github.com/vmlaker/hello-websocket
   cd hello-websocket

Build the virtual environment with all needed modules:
::

   make

Usage
-----

There are two separate programs that need to be running:

#. *recorder* - webcam capture process that writes to Redis database.
#. *server* - the Tornado server which reads current image from 
   the Redis database and serves to requesting WebSocket clients.

First run the *recorder*:
::

   make recorder

Now (in a different shell) run the *server*:
::

   make server
   
Go to http://localhost:9000 to view the webcam.
