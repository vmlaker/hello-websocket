"""
Use WebSocket to send captured images to client.
"""

import base64
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        cap = cv2.VideoCapture(-1)
        while True:
            hello, image = cap.read()
            hello, image = cv2.imencode('.jpg', image)
            ws.send(base64.b64encode(image))

if __name__ == '__main__':
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
