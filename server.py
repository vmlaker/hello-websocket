from threading import Thread
import base64

from tornado import websocket, web, ioloop
import cv2

clients = set()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        if self not in clients:
            clients.add(self)

    def on_close(self):
        if self in clients:
            clients.remove(self)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
])

def capture():
    cap = cv2.VideoCapture(-1)
    while True:
        hello, image = cap.read()
        hello, image = cv2.imencode('.jpg', image)
        image = base64.b64encode(image)
        for client in clients:
            client.write_message(image)

if __name__ == '__main__':
    Thread(target=capture).start()
    app.listen(9000)
    ioloop.IOLoop.instance().start()
