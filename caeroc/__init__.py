"""
caeroc
========

Provides 

  1. An object-oriented calculator utility and plotting.
  2. GUI interface.

The docstring examples assume that `fluiddyn` has been imported as below::

  >>> import caeroc

Use the built-in ``help`` function to view a function's docstring::

  >>> help(caeroc.gui)
  ... # doctest: +SKIP

Available subpackages
---------------------
formulae
    Governing integral equations for compressible flows organised as various
    classes.
gui
    A PyQt/PySide based interface to have an user-friendly view.
profiles
    Toolkit for making specific calculations for a body.

"""
__version__ = '0.0.2b0'


def launch():
    from . import gui
    gui.CalcApp().run()
