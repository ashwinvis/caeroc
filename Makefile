# Caeroc Installer
# ----------------

install:
	python setup.py install

dev:
	python setup.py develop

clean:
	find caeroc -name "*.so" -delete
	find caeroc -name "*.pyc" -delete

tests:
	python -m unittest discover

help:
	cat ./Makefile
