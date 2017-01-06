##############################################
#
#  Makefile to install Python in virtualenv
#  with all dependencies for hello-websocket.
#
##############################################

VENV_LIB = venv/lib/python2.7
VENV_CV2 = $(VENV_LIB)/cv2.so

# Find cv2 library for the global Python installation.
GLOBAL_CV2 := $(shell python -c 'import cv2; print(cv2)' | awk '{print $$4}' | sed s:"['>]":"":g)

# Copy global cv2 library file into the virtual environment.
$(VENV_CV2): $(GLOBAL_CV2) venv
	cp $(GLOBAL_CV2) $@

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -r requirements.txt

test: $(VENV_CV2)
	. venv/bin/activate && python -c 'import cv2; print(cv2)'

MAP_HOST = 127.0.0.1
MAP_PORT = 50003

mapper: venv
	test -d venv || virtualenv venv
	. venv/bin/activate && python mapper.py $(MAP_HOST) $(MAP_PORT)

recorder: venv
	test -d venv || virtualenv venv
	. venv/bin/activate && python recorder.py $(MAP_HOST) $(MAP_PORT)

server: venv
	test -d venv || virtualenv venv
	. venv/bin/activate && python server.py $(MAP_HOST) $(MAP_PORT)

clean:
	rm -rf venv
