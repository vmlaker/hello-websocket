#####################################################################
#
#  Makefile for hello-websocket.
#
#####################################################################
.venv: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

test: .venv
	.venv/bin/python -c 'import cv2; print(cv2)'

recorder: .venv
	.venv/bin/python recorder.py

server: .venv
	.venv/bin/python server.py

clean:
	rm -rf .venv
