"""
________________________________________________________________________

:PROJECT: labPy

*config_widget: labPy config widget*

:details: config_widget: a config/settings widget for the labPy.
          The widget is kept very general. The settings details shall 
          be set in each related widget / app (s.,e.g., labpyworkbench) 

:file:    config_widget.py

:author:  mark doerr <mark.doerr@uni.greifswald.de> : contrib.
          
:date: (creation)          20180909
:date: (last modification) 20180924
.. note:: some remarks
.. todo:: - 

________________________________________________________________________

**Copyright**:
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
  For further Information see COPYING file that comes with this distribution.
________________________________________________________________________

"""

__version__ = "v0.0.3"

import logging

from PySide2 import QtCore, QtWidgets, QtGui

class ConfigDialogWidget(QtWidgets.QDialog):
    """ Config/Settings dialog """
    def __init__ (self, parent=None, 
                  settings=None, title="Main Configuration"):
        super().__init__(parent)
        """ :param parent: parent widget
            :param name: config dialog title"""
        
        self.settings = settings
        
        self.config_TW = QtWidgets.QTabWidget(self)
        
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout_VL = QtWidgets.QVBoxLayout()
        mainLayout_VL.addWidget(self.config_TW)
        mainLayout_VL.addWidget(buttonBox)
        self.setLayout(mainLayout_VL)

        self.setWindowTitle(title)
        
        #~ self.config_TW.addTab(SampleConfigTab(self), "Special")
        
    def addConfigTab(self, widget=None, tab_name="ConfigTab"):
        """ :param [param_name]: [description]"""
        self.config_TW.addTab(widget, tab_name)
        self.adjustSize()
        widget.setSettings(self.settings)


class SampleConfigTab(QtWidgets.QWidget):
    """ this is just an example """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.createControlElements()
        
    def createControlElements(self):
        """ :param [param_name]: [description]"""
        
        self.generalGroup = QtWidgets.QGroupBox("Box1")

        self.readable = QtWidgets.QCheckBox("Readable")
        #~ if fileInfo.isReadable():
            #~ readable.setChecked(True)

        self.writable = QtWidgets.QCheckBox("Writable")
        #~ if fileInfo.isWritable():
            #~ writable.setChecked(True)

        self.executable = QtWidgets.QCheckBox("Executable")
        #~ if fileInfo.isExecutable():
            #~ executable.setChecked(True)

        self.ownerGroup = QtWidgets.QGroupBox("Box2")

        self.ownerLabel = QtWidgets.QLabel("Owner")
        self.ownerValueLabel = QtWidgets.QLabel("own1")
        self.ownerValueLabel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        self.groupLabel = QtWidgets.QLabel("Group")
        self.groupValueLabel = QtWidgets.QLabel("g1")
        self.groupValueLabel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)

        self.permissionsLayout = QtWidgets.QVBoxLayout()
        self.permissionsLayout.addWidget(self.readable)
        self.permissionsLayout.addWidget(self.writable)
        self.permissionsLayout.addWidget(self.executable)
        self.generalGroup.setLayout(self.permissionsLayout)

        self.ownerLayout = QtWidgets.QVBoxLayout()
        self.ownerLayout.addWidget(self.ownerLabel)
        self.ownerLayout.addWidget(self.ownerValueLabel)
        self.ownerLayout.addWidget(self.groupLabel)
        self.ownerLayout.addWidget(self.groupValueLabel)
        self.ownerGroup.setLayout(self.ownerLayout)

        self.mainLayout_VL = QtWidgets.QVBoxLayout()
        self.mainLayout_VL.addWidget(self.generalGroup)
        self.mainLayout_VL.addWidget(self.ownerGroup)
        self.mainLayout_VL.addStretch(1)
        self.setLayout(self.mainLayout_VL)
        
    def setSettings(self, settings):
        """ :param [param_name]: [description]"""
        self.settings = settings
        
    def accept(self):
        """ :param [param_name]: [description]"""
        logging.debug("saving settings {}".format(1) )
