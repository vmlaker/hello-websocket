hello-websocket
===============

Webcam over websocket in Python, using OpenCV and 
`Tornado <http://www.tornadoweb.org>`_.

Details
-------

The code runs a *recorder* process that continuously reads images
from the webcam. Upon every capture it writes the image to a Redis
key-value store.

Separately, a *server* process (running Tornado) handles websocket messages. 
Upon receiving a request message (sent from *client* web browser)
it retrieves the latest image from the Redis database and sends it 
to the *client* over websocket connection.

.. image:: https://raw.github.com/vmlaker/hello-websocket/master/diagram.png

The *client* web page is dead simple: 
It sends an initial request on a WebSocket.
When image data comes in, it assigns it to ``src`` attribute of the
``<img>`` tag, then simply sends the next request. That's it!

Installation
------------

The code uses Python and third-party modules installed in a 
``virtualenv`` with ``pip``. But since OpenCV is not part 
of the Python Package Index, you're gonna need to install 
it system-wide. (Later below, *make* will manually pull the library
into the virtual environment):
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

systemd services
----------------

If your O/S has 
`systemd <http://freedesktop.org/wiki/Software/systemd>`_
you have the option of installing 
*recorder* and *server* as systemd services.
Begin by customizing settings in file ``systemd/hello.conf``.
Then, from the project root directory, generate your service files:
::

   python systemd/create.py
   
Install your newly-created services into your systemd location:
::

   sudo cp `pwd`/systemd/*.service /usr/lib/systemd/system/

You can now start the two services by starting the *server*
(*recorder* is a dependency, and will start automatically):
::

   sudo systemctl start hws-server

To shut down all three services, just stop the *mapper*
(*recorder* and *server* depend on *mapper*, and will stop automatically):
::

   sudo systemctl stop hws-mapper
