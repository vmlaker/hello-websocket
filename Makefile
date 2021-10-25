#####################################################################
#
#  Makefile for hello-websocket.
#
#####################################################################
THE_PYTHON = python3.8

.venv: requirements.txt
	virtualenv .venv -p $(THE_PYTHON)
	.venv/bin/pip install -r requirements.txt

test: .venv
	.venv/bin/python -c 'import cv2; print(cv2)'

recorder: .venv
	.venv/bin/python recorder.py

server: .venv
	.venv/bin/python server.py

clean:
	rm -rf .venv
