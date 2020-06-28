#####################################################################
#
#  Makefile for hello-websocket.
#
#####################################################################
THE_PYTHON = python3.8
VENV_LIB = .venv/lib/$(THE_PYTHON)/site-packages
VENV_CV2 = $(VENV_LIB)/cv2.so

# Find cv2 library in the system Python installation.
GLOBAL_CV2 := $(shell $(THE_PYTHON) \
   -c 'import cv2; print(cv2)' | awk '{print $$4}' | sed s:"['>]":"":g)

# Copy system Python's cv2 library file into the virtualenv.
$(VENV_CV2): $(GLOBAL_CV2) .venv
	cp $(GLOBAL_CV2) $@

.venv: requirements.txt
	virtualenv .venv -p $(THE_PYTHON)
	.venv/bin/pip install -r requirements.txt

test: $(VENV_CV2)
	.venv/bin/python -c 'import cv2; print(cv2)'

recorder: $(VENV_CV2)
	.venv/bin/python recorder.py

server: $(VENV_CV2)
	.venv/bin/python server.py

clean:
	rm -rf .venv
