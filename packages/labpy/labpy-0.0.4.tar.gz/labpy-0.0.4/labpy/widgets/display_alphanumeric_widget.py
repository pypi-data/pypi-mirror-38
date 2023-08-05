"""
________________________________________________________________________

:PROJECT: labPy

*display_alphanumeric_widget: labPy alphanumeric display widget*

:details: display_alphanumeric_widget: a tool bar. 

:file:    display_alphanumeric_widget.py

:author:  mark doerr <mark.doerr@uni.greifswald.de> : contrib.
          
:date: (creation)          20180907
:date: (last modification) 20181104
.. note:: some remarks
.. todo:: - data logger

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

__version__ = "v0.0.2"

import logging

from PySide2 import QtCore, QtGui, QtWidgets

import labpy.labpyworkbench as lpwb

class NumericDisplayWidget(QtWidgets.QDockWidget):
    """ Numeric Display
    """
    def __init__(self, parent, max_width=0):
        super().__init__(parent=None)
        
        self.update_plot = True
        
        main_display_widget = QtGui.QWidget(parent)
        if max_width > 0:
            main_display_widget.setMaximumWidth(max_width)
        
        v_layout = QtGui.QVBoxLayout(main_display_widget)
        
        h_layout = QtGui.QHBoxLayout()
                 
        self.annotate_PB = QtGui.QPushButton(main_display_widget)
        #self.annotate_PB.setGeometry(QtCore.QRect(380, 250, 251, 61))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.annotate_PB.sizePolicy().hasHeightForWidth())
        self.annotate_PB.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.annotate_PB.setFont(font)
        self.annotate_PB.setStyleSheet(_fromUtf8("QPushButton{\n"
                                        "  border-radius : 10px;\n"
                                        "    background-color: rgb(0, 85, 255);\n"
                                        "    selection-color: rgb(170, 255, 0);\n"
                                        "        min-width: 80px;\n"
                                        "}\n"
                                        "\n"
                                        " QPushButton:pressed {\n"
                                        "    background-color: rgb(85, 255, 0);\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:checked {\n"
                                        "    \n"
                                        "    background-color: rgb(255, 0, 0);\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:flat {\n"
                                        "     border: none; /* no border for a flat push button */\n"
                                        " }\n"
                                        ""))
        #self.annotate_PB.setCheckable(True)
        self.annotate_PB.setObjectName(_fromUtf8("annotate_PB"))
        
        self.pause_plot_PB = QtGui.QPushButton(main_display_widget)
        #self.pause_plot_PB.setGeometry(QtCore.QRect(120, 270, 91, 41))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pause_plot_PB.sizePolicy().hasHeightForWidth())
        self.pause_plot_PB.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pause_plot_PB.setFont(font)
        self.pause_plot_PB.setStyleSheet(_fromUtf8("QPushButton{\n"
                                        " border-radius : 10px;\n"
                                        " background-color: rgb(255, 255, 0);\n"
                                        "    selection-color: rgb(170, 255, 0);\n"
                                        "    gridline-color: rgb(89, 152, 52);\n"
                                        "        min-width: 60px;\n"
                                        "}\n"
                                        "\n"
                                        " QPushButton:pressed {\n"
                                        "    background-color: rgb(85, 255, 0);\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:checked {\n"
                                        "    \n"
                                        "    background-color: rgb(255, 0, 0);\n"
                                        " }\n"
                                        "\n"
                                        " QPushButton:flat {\n"
                                        "     border: none; /* no border for a flat push button */\n"
                                        " }\n"
                                        ""))
        self.pause_plot_PB.setCheckable(True)
        self.pause_plot_PB.setObjectName(_fromUtf8("pause_plot_PB"))
        
        self.pause_plot_PB.clicked.connect(self.togglePlotStatus)
        
        #~ self.pause_plot_PB.setText(_translate("labTimer", "clear", None))
        #~ self.startStop_PB.setText(_translate("labTimer", "start/stop", None))
        
        #~ h_layout.addWidget(self.startStop_PB)
        h_layout.addWidget(self.annotate_PB)
        h_layout.addWidget(self.pause_plot_PB)
        v_layout.addLayout(h_layout)
        
        self.value_display = QtGui.QLabel("0.000", parent=main_display_widget)
        self.value_display.setGeometry(QtCore.QRect(30, 10, 641, 131))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.value_display.setFont(font)
        self.value_display.setStyleSheet(_fromUtf8("\n"""))
        self.value_display.setObjectName(_fromUtf8("timeDisplay_TimEd"))
        
        v_layout.addWidget( self.value_display)
        
        self.valueList_te = QtGui.QTextEdit(parent=main_display_widget)
        
        v_layout.addWidget( self.valueList_te)
        
        self.setWidget(main_display_widget)
    
    def appendText(self, text):
        self.valueList_te.append(text)
        
    def prependText(self, text):
        self.valueList_te.moveCursor(QtGui.QTextCursor.Start)
        self.valueList_te.insertPlainText(text)
        
    def displayText(self, text):
        self.value_display.setText(text)
        
    def togglePlotStatus(self):
        if self.update_plot:
           self.update_plot = False
        else :
           self.update_plot = True
  
class TextDisplayWidget(QtWidgets.QPlainTextEdit):
    """ Text Display widget
    """
    def __init__ (self, LP_application=None, name="Text Display", 
                  description="A Simple Plain Text Display",
                  pos=lpwb.WidgetPosition.CENTER, max_width=0, visible=None, tool=False, parent=None):
        """ Class initialiser """
        super().__init__(parent=None)
    
        self.update_print = True
        
        self.LP_application = LP_application

        #~ main_display_widget = QtGui.QWidget(parent)
        #~ if max_width > 0:
            #~ main_display_widget.setMaximumWidth(max_width)
        
        #~ v_layout = QtGui.QVBoxLayout(main_display_widget)
        #~ self.info_te = QtGui.QTextEdit(parent=main_display_widget)
        #~ v_layout.addWidget( self.info_te)
        #~ self.setWidget(main_display_widget)
        
        if LP_application is not None:
            self.LP_mainWin = LP_application.mainWin
            LP_application.addLPWidget(self,name=name, description=description, 
                                       pos=pos, visible=visible, tool=tool)
                
    def setText(self, text):
        """ append Text to current"""
        self.setPlainText(text)
                                           
    def appendText(self, text):
        """ append Text to current"""
        self.appendPlainText(text)
        
    def prependText(self, text):
        self.moveCursor(QtGui.QTextCursor.Start)
        self.insertPlainText(text)
                
    def togglePrintStatus(self):
        if self.update_print:
           self.update_print = False
        else :
           self.update_print = True
