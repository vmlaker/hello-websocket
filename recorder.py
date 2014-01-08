"""
Run webcam capture and maintain current image on socket server.
"""

# Import standard modules.
import sys
import StringIO

# Import third-party modules.
import coils
import cv2
import numpy
from coils import MapSockClient, MapSockRequest

cap = cv2.VideoCapture(-1)
map_client = MapSockClient('localhost', int(sys.argv[1]), encode=False)

while True:
    hello, image = cap.read()
    hello, image = cv2.imencode('.jpg', image)
    sio = StringIO.StringIO()
    numpy.save(sio, image)
    value = sio.getvalue()
    request = MapSockRequest(
        'set',
        'image',
        value,
        )
    response = map_client.send(request)
