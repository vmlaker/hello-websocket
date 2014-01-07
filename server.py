"""
Serve webcam using Tornado.
"""

# Import standard modules.
from threading import Thread, Lock
import base64

# Import 3rd-party modules.
from tornado import websocket, web, ioloop
import cv2

clients = set()  # Tornado clients.
lock = Lock()  # Mutex lock for clients list.

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

def synchronized(lock):
    """ Synchronization decorator. """
    def wrap(f):
        def newFunction(*args, **kw):
            with lock:
                return f(*args, **kw)
        return newFunction
    return wrap

class SocketHandler(websocket.WebSocketHandler):

    @synchronized(lock)
    def open(self):
        if self not in clients:
            clients.add(self)

    @synchronized(lock)
    def on_close(self):
        if self in clients:
            clients.remove(self)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

@synchronized(lock)
def write(datum):
    for client in clients:
        client.write_message(datum)
    
def capture():
    cap = cv2.VideoCapture(-1)
    while True:
        hello, image = cap.read()
        hello, image = cv2.imencode('.jpg', image)
        image = base64.b64encode(image)
        write(image)

if __name__ == '__main__':
    Thread(target=capture).start()
    app.listen(9000)
    ioloop.IOLoop.instance().start()
