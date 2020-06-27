##############################################
#
#  Makefile for hello-websocket.
#
##############################################

PYTHON_EXE = python3.8
VENV_LIB = .venv/lib/$(PYTHON_EXE)/site-packages
VENV_CV2 = $(VENV_LIB)/cv2.so

# Find cv2 library for the global Python installation.
GLOBAL_CV2 := $(shell $(PYTHON_EXE) -c 'import cv2; print(cv2)' | awk '{print $$4}' | sed s:"['>]":"":g)

# Copy global cv2 library file into the virtual environment.
$(VENV_CV2): $(GLOBAL_CV2) .venv
	cp $(GLOBAL_CV2) $@

.venv: requirements.txt
	virtualenv .venv -p $(PYTHON_EXE)
	.venv/bin/pip install -r requirements.txt

test: $(VENV_CV2)
	.venv/bin/python -c 'import cv2; print(cv2)'

recorder: .venv
	.venv/bin/python recorder.py

server: .venv
	.venv/bin/python server.py

clean:
	rm -rf .venv
