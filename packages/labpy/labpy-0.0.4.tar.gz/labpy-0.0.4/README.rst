labPy
======

labPy is a collection of a laboratory instrument connectors/drivers and Qt5 (PySide2) based GUIs  / instrument widget sets
for fast data plotting, logging and instrument control. Its modular design is aiming at replacing LabView (R), but keeping it tiny and lean.

source: https://gitlab.com/LARAsuite/pylab

labPy main features
____________________


  * unified GUI environment for easily creating lab device interfaces (python3/QT5/pyside2 based)
  * complete application with advanced menus, toolbars, statusbar, settings dialogues
  * dock-able windows, flexible window movement, saving of window states
  * settings will be preserved over closing the app
  * command-line parsing
  * signals for communication, threading for multi-threading applications
  * many standard widgets (Temperature display, timer, alphanumeric displays, data plotting)
  * pluggable widget system
  * hardware device interface (serial communication)
  * SiLA2 (https://sila-standard.org) support
  * Arduino and Raspberry Pi support
  * extremely small footprint, fast
  * examples / demo library
  
labpy packages
_______________

  * core   - labpyworkbench
  * widgets - collection of reusable widgets
  * dev_com - device communication library
  * math_models - mathematical models for data evaluation and simulation
 

labpy fast installation
_________________________

the fastest way to install labpy is through PyPi and pip:

    # --user indicatates to do a local installation into home directory
    pip3 install --user labpy
    
    
labpy full installation
_________________________

    git clone https://gitlab.com/LARAsuite/labpy.git
    
    cd labpy 
    
    # this installs everything in a virtual environment for testing:
    
    python3 labpyinstall.py 
    
    (Note: please also install dependencies !!)

  
quick start demos
__________________

see examples/demos for feature demos

more examles can be find in the examples section


documentation
______________


see docs/quickstart.rst guide for a quick start

and docs for complete documentation

generating the documentation
-----------------------------

current widgets
________________

  * alpha numeric
  * timer
  * oszillograph
  * wave generator
  * pump control
  * simple text edit
  * python edit
  * matplot 
  * pyqtgraph
