
from setuptools import setup, find_packages
"""
try:
    from Cython.Distutils.extension import Extension
    from Cython.Distutils import build_ext
except ImportError:
    from setuptools import Extension, build_ext
    from distutils.command import build_ext
"""
import os
here = os.path.abspath(os.path.dirname(__file__))

import sys
if sys.version_info[:2] < (2, 6) or (3, 0) <= sys.version_info[0:2] < (3, 2):
    raise RuntimeError("Python version 2.6, 2.7 or >= 3.2 required.")

# Get the long description from the relevant file
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()
lines = long_description.splitlines(True)
long_description = ''.join(lines[8:])

# Get the version from the relevant file
execfile('caeroc/_version.py')
# Get the development status from the version string
from pkg_resources import parse_version
parsed_version = parse_version(__version__)
try:
    if parsed_version.is_prerelease:
        if 'a' in __version__:
            devstatus = 'Development Status :: 3 - Alpha'
        else:
            devstatus = 'Development Status :: 4 - Beta'
    else:
        devstatus = 'Development Status :: 5 - Production/Stable'
except AttributeError:
    if 'a' in __version__:
        devstatus = 'Development Status :: 3 - Alpha'
    elif 'b' in __version__:
        devstatus = 'Development Status :: 4 - Beta'
    else:
        devstatus = 'Development Status :: 5 - Production/Stable'

setup(name='caeroc',
      version=__version__,
      description=('Compressible aerodynamics calculator in Python'
                   'A tool for experiments and simulations.'),
      long_description=long_description,
      keywords='compressible aerodynamics, calculator, gas dynamics',
      author='Ashwin Vishnu Mohanan',
      author_email='avmo@kth.se',
      url='https://github.org/jadelord/caeroc',
      license='GPL',
      classifiers=[
          # How mature is this project? Common values are
          # 3 - Alpha
          # 4 - Beta
          # 5 - Production/Stable
          devstatus,
          'Intended Audience :: Science/Research',
          'Intended Audience :: Education',
          'Topic :: Scientific/Engineering',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          # Specify the Python versions you support here. In particular,
          # ensure that you indicate whether you support Python 2,
          # Python 3 or both.
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          # 'Programming Language :: Python :: 3',
          # 'Programming Language :: Python :: 3.3',
          # 'Programming Language :: Python :: 3.4',
      ],
      packages=find_packages(exclude=['doc', 'examples']),
      # package_data={
      #     'sample': ['package_data.dat'],
      # },
      install_requires=['numpy', 'matplotlib'],
      extras_require=dict(plot=['pylab','pandas'], ui=['PySide']),
      scripts=[]
      )
"""
      cmdclass={"build_ext": build_ext}
      ext_modules=None)
"""
