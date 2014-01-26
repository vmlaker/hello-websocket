"""
Serve webcam images (from a remote socket dictionary server)
using Tornado (to a WebSocket browser client.)

Usage:

   python server.py <host> <port>

"""

# Import standard modules.
import sys
import base64
import StringIO

# Import 3rd-party modules.
from tornado import websocket, web, ioloop
import numpy
import coils

# Retrieve command line arguments.
host = sys.argv[1]
port = int(sys.argv[2])

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

class SocketHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(SocketHandler, self).__init__(*args, **kwargs)

        # Client to the socket server.
        self._map_client = coils.MapSockClient(host, port, encode=False)

        # Monitor the framerate at 1s, 5s, 10s intervals.
        self._fps = coils.RateTicker((1,5,10))

    def on_message(self, message):
        response = self._map_client.send(coils.MapSockRequest('get', 'image'))
        sio = StringIO.StringIO(response)
        image = numpy.load(sio)
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
