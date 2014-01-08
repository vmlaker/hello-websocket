hello-websocket
===============

Webcam over WebSocket in Python, using OpenCV and 
`Tornado <http://www.tornadoweb.org>`_.

Details
-------

The code runs a *recorder* process that continuously reads images
from the webcam. Upon every capture it updates the *mapper*, a tiny
local storage server which keeps the latest captured image
in memory. The *mapper* is accessible via low-level (local) socket interface.

Separately, a *server* process (running Tornado) handles WebSocket messages. 
Upon receiving a request message (sent from *client* web browser)
it connects to the local *mapper*, retrieves latest image and sends it 
to the *client* over WebSocket connection.

The *client* web page is dead simple: 
It sends an initial request on a WebSocket.
When image data comes in, it assigns it to ``src`` attribute of the
``<img>`` tag, then simply sends the next request. Voilà!

Installation
------------

The code uses Python and third-party modules installed in a 
``virtualenv`` with ``pip``. But since OpenCV is not part 
of the Python Package Index, you're gonna need to install 
it system-wide. (Later below, *make* will manually pull the library
into the virtual environment):
::

   yum install opencv-python

Now go ahead and grab the source code repo,
and the additional auxiliary
`Coils <http://vmlaker.github.io/coils>`_ repo:
::

   git clone https://github.com/vmlaker/hello-websocket
   cd hello-websocket
   git clone https://github.com/vmlaker/coils

Build the virtual environment with all needed modules:
::

   make

Usage
-----

There are three separate programs that need to be running:

#. *mapper* - a lightweight server that keeps the current captured 
   image in memory and serves it to multiple local clients.
#. *recorder* - webcam capture process that feeds the *mapper*.
#. *server* - the Tornado server which reads current image from 
   the *mapper* and serves to requesting WebSocket clients.

First run the *mapper*:
::

   make mapper

Now (in a different shell) run the *recorder*:
::

   make recorder

Finally (in a third shell) run the *server*:
::

   make server
   
Go to http://localhost:9000 to view the webcam.
