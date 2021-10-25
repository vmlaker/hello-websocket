"""
Continuously capture images from a webcam and write to a Redis store.
Usage:
   python recorder.py [width] [height]
"""

import itertools
import os
import sys
import time

import cv2
import numpy as np
import redis


# Retrieve command line arguments.
WIDTH = None if len(sys.argv) <= 1 else int(sys.argv[1])
HEIGHT = None if len(sys.argv) <= 2 else int(sys.argv[2])

# Create video capture object, retrying until successful.
MAX_SLEEP = 5.0
CUR_SLEEP = 0.1
while True:
    cap = cv2.VideoCapture(-1)
    if cap.isOpened():
        break
    print(f'not opened, sleeping {CUR_SLEEP}s')
    time.sleep(CUR_SLEEP)
    if CUR_SLEEP < MAX_SLEEP:
        CUR_SLEEP *= 2
        CUR_SLEEP = min(CUR_SLEEP, MAX_SLEEP)
        continue
    CUR_SLEEP = 0.1

# Create client to the Redis store.
store = redis.Redis()

# Set video dimensions, if given.
if WIDTH:
    cap.set(3, WIDTH)
if HEIGHT:
    cap.set(4, HEIGHT)

# Repeatedly capture current image, encode it, convert it to bytes and push
# it to Redis database. Then create unique ID, and push it to database as well.
for count in itertools.count(1):
    _, image = cap.read()
    if image is None:
        time.sleep(0.5)
        continue
    _, image = cv2.imencode('.jpg', image)
    store.set('image', np.array(image).tobytes())
    store.set('image_id', os.urandom(4))
    print(count)
