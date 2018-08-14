caeroc
======

Compressible Aerodynamics Calculator for Python
-----------------------------------------------

|version| |LICENSE| |travis|

A python package for compressible flows. A dynamic toolkit which enables
you to make use of the formulae governing compressible flows.

.. figure:: https://raw.githubusercontent.com/ashwinvis/caeroc/gh-pages/screenshot.png
   :alt: Screenshot

.. figure:: https://raw.githubusercontent.com/ashwinvis/caeroc/gh-pages/caeroc-video.png
   :alt: Demo. Click to see the full video
   :align: right
   :target: https://peertube.social/videos/watch/2663f4b3-7c0a-4283-ac8b-9f864187d775

Requirements
------------
- Python 2.7, >=3.4
- pylab (numpy, scipy and matplotlib)
- ashwinvis/scikit-aero >= 0.2
- PyQt5 / PySide (optional, but recommended for GUI)
- pandas (optional: for making tables)
- colorlog (optional: for coloured log)

Installation
------------
To install from PyPI:

.. code:: bash

    pip install -e git+https://github.com/AeroPython/scikit-aero.git#egg=scikit-aero

    # Any of the following
    pip install caeroc
    pip install caeroc[pyqt]
    pip install caeroc[pyside]

To install development versions of ``caeroc`` and ``scikit-aero``

.. code:: bash

    pip install pipenv
    pipenv install -e git+https://github.com/ashwinvis/caeroc.git#egg=caeroc

If the current configuration of the GUI does not work for you,
regenerate it by running:

.. code:: bash

    cd caeroc/gui
    ./configure

Launch
------
Simply run in your terminal

.. code:: bash

    caeroc-app

Features
--------

-  [x] Command-line tool which opens a Qt based GUI calculator

   In development

-  [ ] Save data as a database
-  [ ] Plotting graphs
-  [ ] Generate gas tables
-  [ ] Calculate flow characteristics: Coefficient of pressure, lift and
   drag for basic profiles.

Courtesy
--------

-  The idea for a compressible aerodynamics calculator in the form an
   online JS tool had been implemented by `William
   Devenport <http://www.aoe.vt.edu/people/faculty.php?fac_id=wdevenpo>`__
   `here <http://www.dept.aoe.vt.edu/~devenpor/aoe3114/calc.html>`__.
   This project is pushing more functionalities as an offline tool and
   allowing users to dynamically use the formulae for specific cases.
-  Thanks to the scikit-aero team for being the backend

.. |version| image:: https://img.shields.io/pypi/v/caeroc.svg
   :target: https://pypi.python.org/pypi/caeroc/
   :alt: Latest version
.. |LICENSE| image:: https://img.shields.io/badge/license-GPL-blue.svg
   :target: /LICENSE
.. |travis| image:: https://travis-ci.org/ashwinvis/caeroc.svg?branch=master
   :target: https://travis-ci.org/ashwinvis/caeroc
