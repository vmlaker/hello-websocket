"""
Continuously capture images from a webcam
and update a socket dictionary server with the current snapshot.

Usage:

   python recorder.py <host> <port> [<width>] [<height>]

"""

# Import standard modules.
import sys
import StringIO

# Import third-party modules.
import numpy
import cv2
import coils

# Retrieve command line arguments.
host = sys.argv[1]
port = int(sys.argv[2])
width = None if len(sys.argv) <= 3 else int(sys.argv[3])
height = None if len(sys.argv) <= 4 else int(sys.argv[4])

# Create video capture object and socket client.
cap = cv2.VideoCapture(-1)
map_client = coils.MapSockClient(host, port, encode=False)

# Set video dimensions, if given.
if width: cap.set(3, width)
if height: cap.set(4, height)

# Monitor the framerate at 1s, 5s, 10s intervals.
fps = coils.RateTicker((1,5,10))

# Repeatedly capture current image, 
# encode and push on socket connection.
while True:
    hello, image = cap.read()
    if image is None:
        import time
        time.sleep(0.5)
        continue
    hello, image = cv2.imencode('.jpg', image)
    sio = StringIO.StringIO()
    numpy.save(sio, image)
    value = sio.getvalue()
    request = coils.MapSockRequest(
        'set',
        'image',
        value,
        )
    response = map_client.send(request)

    # Print the framerate.
    text = '{:.2f}, {:.2f}, {:.2f} fps'.format(*fps.tick())
    print(text)
