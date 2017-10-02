"""
Continuously capture images from a webcam and write to a Redis store.
Usage:
   python recorder.py [width] [height]
"""

import StringIO
import sys
import time

import coils
import cv2
import numpy as np
import redis


# Retrieve command line arguments.
width = None if len(sys.argv) <= 1 else int(sys.argv[1])
height = None if len(sys.argv) <= 2 else int(sys.argv[2])

# Create video capture object and client to the Redis store.
cap = cv2.VideoCapture(-1)
store = redis.Redis()

# Set video dimensions, if given.
if width: cap.set(3, width)
if height: cap.set(4, height)

# Monitor the framerate at 1s, 5s, 10s intervals.
fps = coils.RateTicker((1, 5, 10))

# Repeatedly capture current image, 
# encode, serialize and push to Redis database.
while True:
    hello, image = cap.read()
    if image is None:
        time.sleep(0.5)
        continue
    
    hello, image = cv2.imencode('.jpg', image)
    sio = StringIO.StringIO()
    np.save(sio, image)
    value = sio.getvalue()
    store.set('image', value)

    # Print the framerate.
    text = '{:.2f}, {:.2f}, {:.2f} fps'.format(*fps.tick())
    print(text)
