"""
Run webcam capture and maintain current image on socket server.

Usage:

   python recorder.py port [width] [height]
"""

# Import standard modules.
import sys
import StringIO

# Import third-party modules.
import coils
import cv2
import numpy
from coils import MapSockClient, MapSockRequest

# Create video capture object and socket client.
cap = cv2.VideoCapture(-1)
map_client = MapSockClient('localhost', int(sys.argv[1]), encode=False)

# Set video dimensions, if given.
if len(sys.argv) > 2: cap.set(3, int(sys.argv[2]))
if len(sys.argv) > 3: cap.set(4, int(sys.argv[3]))

# Repeatedly capture current image, 
# encode and push on socket connection.
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
