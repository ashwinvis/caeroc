# Caeroc Installer
# ----------------

ver := $(shell python2 -c 'from caeroc import __version__; print __version__')

install:
	python setup.py install
	cd scikit-aero && python setup.py install

develop:
	python setup.py develop
	cd scikit-aero && python setup.py develop

gui:
	cd caeroc/gui/ && ./configure

clean:
	find caeroc -name "*.so" -delete
	find caeroc -name "*.pyc" -delete

tests:
	python -m unittest discover

help:
	cat ./Makefile

tag_version:
	git tag -a $(ver)
