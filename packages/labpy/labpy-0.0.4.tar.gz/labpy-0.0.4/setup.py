"""_____________________________________________________________________

:PROJECT: labPy

*labpy setup *

:details: labpy setup file for installation.
         - For installation, run:
           run pip3 install .
           or  python3 setup.py install

:file:    setup.py
:authors: mark doerr (mark.doerr@uni-greifswald.de)

:date: 20180918         
:date: 20181103

.. note:: -
.. todo:: - 
________________________________________________________________________
"""
__version__ = "0.0.4"

import os
import sys

from setuptools import setup, find_packages
#~ from distutils.sysconfig import get_python_lib

pkg_name = 'labpy'

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file :
        return file.read()

install_requires = [] 
data_files = []
    
setup(name=pkg_name,
    version=__version__,
    description='labpy - a python laboratory (automation) environment ',
    long_description=read('README.rst'),
    author='mark doerr',
    author_email='mark.doerr@uni-greifswald.de',
    keywords=('lab automation, Qt5, PySide2, laboratory, instruments,' 
              'experiments, evaluation, visualisation, serial interface, SiLA2, robots, database'),
    url='https://gitlab.com/LARAsuite/pylab',
    license='GPLv2+',
    packages=find_packages(), #['pylab'],
    #~ package_dir={'pylab':'pylab'},
    install_requires = install_requires,
    test_suite='',
    classifiers=[  'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Utilities',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                   'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                   'Topic :: Scientific/Engineering :: Visualization',
                   'Topic :: Scientific/Engineering :: Information Analysis'],
    include_package_data=True,
    data_files=data_files,
)
