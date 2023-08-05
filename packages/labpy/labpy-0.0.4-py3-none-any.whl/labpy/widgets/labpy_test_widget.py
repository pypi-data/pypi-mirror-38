"""
________________________________________________________________________

:PROJECT: labPy

*labPy test widget*

:details: testwidget: very simple labpy test widget for adding elements to main window

          - 

:file:    labpy_testwidget.py

:author:  mark doerr <mark@MicT660p> : contrib.

:version: 0.0.1

:date: (creation)          20181104
:date: (last modification) 20181104
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

__version__ = "v0.0.1"


import sys
import logging

from PySide2 import QtCore, QtWidgets, QtGui

import labpy_rc

import labpyworkbench as lpwb


class LabPyTest(QtWidgets.QWidget): 
    """ very simple Test Widget.
    """
    MaxRecentFiles = 5
    
    def __init__ (self, LP_application=None, name="SimpleTextEditor", 
                  description="A Simple Plain Text Editor",
                  pos=lpwb.WidgetPosition.BOTTOMTAB, visible=None, tool=False, parent=None):
        """ Class initialiser """
        super().__init__(parent=None)
        
        self.LP_application = LP_application
        self.LP_mainWin = None
        
        if LP_application is not None:
            self.LP_mainWin = LP_application.mainWin
            LP_application.addLPWidget(self,name=name, description=description, 
                                       pos=pos, visible=visible, tool=tool)
            self.createActions()
            self.addAct2Toolbar(self.LP_mainWin.edit_TB)
            self.addAct2Menu(self.LP_mainWin.fileMenu)
            
    def cutAction(self):
        """ generic edit-cut method"""
        #~ self.editCut_Sig.emit()
        logging.debug("cut {}".format(1) )
        
    def copyAction(self):
        """ generic edit-copy method"""
        #~ self.editCopy_Sig.emit()
        logging.debug("copy {}".format(1) )
        
    def pasteAction(self):
        """ generic edit-paste method"""
        #~ self.editPaste_Sig.emit()
        logging.debug("paste{}".format(1) )
        
            
    def createActions(self):
        """ python editor QT actions"""
        resource_prefix = ':/linux/actions/24/'
        resource_scale_prefix = ':/linux/actions/scalable/'
        
        self.copy_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'copy'),"&Copy", self, 
                         shortcut=QtGui.QKeySequence.Copy,
                         statusTip="Copy the current selection's contents to the clipboard", 
                         triggered=self.copyAction)
        self.cut_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'cut'),"Cu&t", self, 
                        shortcut=QtGui.QKeySequence.Cut,
                        statusTip="Cut the current selection's contents to the clipboard", 
                        triggered=self.cutAction)
        self.paste_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'paste'),"&Paste", self, 
                          shortcut=QtGui.QKeySequence.Paste,
                          statusTip="Paste the clipboard's contents into the current selection", 
                          triggered=self.pasteAction)
        
    def addAct2Toolbar(self, toolbar):
        """ :param [param_name]: [description]"""
        
        toolbar.addAction(self.copy_Act)
        toolbar.addAction(self.cut_Act)
        toolbar.addAction(self.paste_Act)
        
    def addAct2Menu(self, menu):
        """ :param [param_name]: [description]"""
        
        menu.addAction(self.new_Act)
        menu.addAction(self.open_Act)
        menu.addAction(self.save_Act)
        menu.addAction(self.saveAs_Act)
