"""
Serve webcam images (via socket server) using Tornado.
"""

# Import standard modules.
import sys
import base64

# Import 3rd-party modules.
from tornado import websocket, web, ioloop
import numpy
import StringIO
from coils import MapSockClient, MapSockRequest

map_client = MapSockClient('localhost', int(sys.argv[1]), encode=False)

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

class SocketHandler(websocket.WebSocketHandler):

    def on_message(self, message):
        response = map_client.send(MapSockRequest('get', 'image'))
        sio = StringIO.StringIO(response)
        image = numpy.load(sio)
        image = base64.b64encode(image)
        self.write_message(image)
        
app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

if __name__ == '__main__':
    app.listen(9000)
    ioloop.IOLoop.instance().start()
