"""
________________________________________________________________________

:PROJECT: labPy

*temperature_widget: labPy temperature widget*

:details: temperature_widget: a tool bar widget for the labpyworkbench. 

:file:    temperature_widget.py

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

__version__ = "v0.0.4"

import logging

from PySide2 import QtWidgets

import labpy.labpyworkbench as lpwb

class TemperatureWidget(QtWidgets.QWidget):
    """ Measurement temperature """
    def __init__ (self, LP_application=None, parent=None, name="Temperature",
                  temperature=0.42, unit=" C", pos=lpwb.WidgetPosition.TOOLBAR):
        super().__init__(parent=parent)
        
        self.curr_temp = temperature
        self.temp_unit = unit
        self.font_size = 16
        
        self.temp_widget_HL = QtWidgets.QHBoxLayout()
        self.temp_label = QtWidgets.QLabel(str(self.curr_temp) + self.temp_unit )
        self.temp_widget_HL.addWidget(self.temp_label)
        self.setLayout(self.temp_widget_HL)
        
        self.temp_label.setStyleSheet("""font-weight: bold;
                                         font-size: {font_size}pt;
                                         color: {color};""".format(color="lightblue", 
                                                                    font_size=self.font_size))
                                                                    
        if LP_application is not None:
            LP_application.addLPWidget(self,name=name, pos=pos)
        
        
    def setTemperature(self, temperature=42.1):
        """ :param [param_name]: [description]"""
        
        self.curr_temp = temperature
        
        self.temp_label.setText(str(self.curr_temp)+self.temp_unit)
        
        if self.curr_temp < 20.0: color ="blue"
        elif self.curr_temp < 30.0: color = "green"
        elif self.curr_temp < 37.0: color = "orange"
        else :  color = "red"
                           
        logging.debug("font size:{}".format(self.font_size) )
        
        self.temp_label.setStyleSheet("""font-weight: bold;
                                         font-size: {font_size}pt;
                                         color: {color};""".format(font_size=self.font_size, color=color ))
                                         
    def setFontSize(self, font_size=16):
        """ :param [param_name]: [description]"""
        self.font_size = font_size
        #~ self.temp_label.setStyleSheet("font-size: {font_size}pt;".format(font_size=self.font_size))
        
    def setStyleSheet(self, style=""):
        """ :param [param_name]: [description]"""
        self.temp_label.setStyleSheet(style)
    
    def setUnit(self, unit=" C"):
        """ :param [param_name]: [description]"""
        
        self.temp_unit = unit
            

        
