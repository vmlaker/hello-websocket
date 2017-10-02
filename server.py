"""
Serve webcam images from a Redis store using Tornado.
Usage:
   python server.py
"""

import base64
import StringIO
import sys

import coils
import numpy as np
import redis
from tornado import websocket, web, ioloop


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

class SocketHandler(websocket.WebSocketHandler):
    """ Handler for websocket queries. """
    
    def __init__(self, *args, **kwargs):
        """ Initialize the Redis store and framerate monitor. """
        super(SocketHandler, self).__init__(*args, **kwargs)
        self._store = redis.Redis()
        self._fps = coils.RateTicker((1, 5, 10))

    def on_message(self, message):
        """ Retrieve image from database, de-serialize,
        encode and send to client. """
        image = self._store.get('image')
        image = StringIO.StringIO(image)
        image = np.load(image)
        image = base64.b64encode(image)
        self.write_message(image)

        # Print object ID and the framerate.
        text = '{} {:.2f}, {:.2f}, {:.2f} fps'.format(id(self), *self._fps.tick())
        print(text)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(9000)
    ioloop.IOLoop.instance().start()
