"""
Serve webcam images from a Redis store using Tornado.
Usage:
   python server.py
"""

import base64
import time

import redis
from tornado import websocket, web, ioloop

MAX_FPS = 100

class IndexHandler(web.RequestHandler):
    """ Handler for the root static page. """
    def get(self):
        """ Retrieve the page content. """
        self.render('index.html')

class SocketHandler(websocket.WebSocketHandler):
    """ Handler for the websocket URL. """

    def __init__(self, *args, **kwargs):
        """ Initialize the Redis store and framerate monitor. """

        super().__init__(*args, **kwargs)
        self._store = redis.Redis()
        self._prev_image_id = None

    def on_message(self, message):
        """ Retrieve image ID from database until different from last ID,
        then retrieve image, de-serialize, encode and send to client. """

        while True:
            time.sleep(1./MAX_FPS)
            image_id = self._store.get('image_id')
            if image_id != self._prev_image_id:
                break
        self._prev_image_id = image_id
        image = self._store.get('image')
        image = base64.b64encode(image)
        self.write_message(image)
        print(image_id)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(9000)
    ioloop.IOLoop.instance().start()
