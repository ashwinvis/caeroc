caeroc
======
Compressible Aerodynamics Calculator for Python
-----------------------------------------------
![alpha](https://img.shields.io/badge/caeroc-v0.0.2a-green.svg) 
[![LICENSE](https://img.shields.io/badge/license-GPL-blue.svg)](/LICENSE)

A python package for compressible flows. A dynamic toolkit which enables you to make use of the formulae governing compressible flows.

Installation
------------
```bash
make install
```

Features
--------
- [x] Command-line tool which opens a Qt based GUI calculator

```bash
caeroc-app
```
![In development](http://i.imgur.com/7Bb0ypN.png)

- [ ] Save data as a database
- [ ] Plotting graphs
- [ ] Generate gas tables
- [ ] Calculate flow characteristics: Coefficient of pressure, lift and drag for basic profiles.

Courtesy
--------
* The idea for a compressible aerodynamics calculator in the form an online JS tool had been implemented by [William Devenport](http://www.aoe.vt.edu/people/faculty.php?fac_id=wdevenpo) [here](http://www.dept.aoe.vt.edu/~devenpor/aoe3114/calc.html). 
This project is pushing more functionalities as an offline tool and allowing users to dynamically use the formulae for specific cases.
* Thanks to the scikit-aero team for being the backend
