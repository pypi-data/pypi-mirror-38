"""
________________________________________________________________________

:PROJECT: labPy

*timer_widget: labPy timer widget*

:details: timer_widget: various timer widgets
          - timer tool bar widget for the labpyworkbench
          - timer edit
          - lab timer
          - stop watch

:file:    timer_widget.py

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

from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia

import labpy.labpyworkbench as lpwb

class TimerWidget(QtWidgets.QLabel):
    """ Measurement timer """
    def __init__ (self, LP_application=None, name="Timer", 
                  pos=lpwb.WidgetPosition.TOOLBAR, time_zero=None):
        
        if time_zero is None : time_zero = QtCore.QTime(0,0,0,0)
        super().__init__(parent=None)
        """ Class initialiser """
        
        self.LP_application = LP_application
        
        self.curr_time = QtCore.QTime(00,00,00)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.incTimer)
        
        self.setText(self.curr_time.toString("HH:mm:ss.z"))
        
        self.setStyleSheet("font-weight: bold;"
                           "font-size: 16pt;"
                           "color: orange")
                           
        self.setObjectName(name)
        
        # optional adding parts to main application
        if LP_application is not None:
            self.LP_mainWin = LP_application.mainWin
            LP_application.addLPWidget(self,name=name, pos=pos)
            
            self.LP_mainWin.startAll_Sig.connect(self.start)
            self.LP_mainWin.stopAll_Sig.connect(self.stop)
           
    def start(self, timeout=100):
        """ :param [param_name]: [description]"""
        self.timer.start(timeout)
        
    def stop(self):
        """ :param [param_name]: [description]"""
        self.timer.stop()
        self.curr_time = QtCore.QTime(00,00,00)
        self.setText(self.curr_time.toString("HH:mm:ss.z"))
        
    def incTimer(self):
        """ :param [param_name]: [description]"""
        self.curr_time = self.curr_time.addMSecs(100)
        self.setText(self.curr_time.toString("HH:mm:ss.z"))
        

class TimerEditWidget(QtWidgets.QTimeEdit):
    """ Measurement timer """
    def __init__ (self, LP_application=None, 
                  name="TimerEdit", pos=lpwb.WidgetPosition.TOOLBAR, time_zero=None):
        
        if time_zero is None : time_zero = QtCore.QTime(0,0,0,0)
        super().__init__(parent=None)
        """ Class initialiser """
        
        self.LP_application = LP_application
        
        self.curr_time = QtCore.QTime(00,00,00)
        
        self.timer = QtCore.QTimer(self)
        #~ self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.timeout.connect(self.incTimer)
        
        self.setDisplayFormat("HH:mm:ss.z")
        
        #self.setTime(time_zero)
        
        # optional adding parts to main application
        if LP_application is not None:
            self.LP_mainWin = LP_application.mainWin
            LP_application.addLPWidget(self,name=name, pos=pos)
            
            self.LP_mainWin.startAll_Sig.connect(self.start)
            self.LP_mainWin.stopAll_Sig.connect(self.stop)
           
        
    def start(self, timeout=100):
        """ :param [param_name]: [description]"""
        self.timer.start(timeout)
        
    def stop(self):
        """ :param [param_name]: [description]"""
        self.timer.stop()
        self.clear()
        
    def incTimer(self):
        """ :param [param_name]: [description]"""
        self.curr_time = self.curr_time.addMSecs(100)
        self.setTime(self.curr_time)
        
class LabTimer(QtWidgets.QGroupBox):
    """ Lab Timer Widget """
    def __init__ (self, parent=None, LP_application=None, name="LabTimer", 
                        pos=lpwb.WidgetPosition.BOTTOMTAB, time_zero=None):
        """ Class initialiser """
        super().__init__(parent=None)
        
        self.name = name 
        
        self.time_zero = QtCore.QTime(0,0,0,0)
        
        self.curr_time = self.time_zero
        self.setTime   = self.time_zero
        
        self.createControlElements()
        self.player = QtMultimedia.QMediaPlayer(self)
        
        self.timer = QtCore.QTimer(self);
        self.timer.timeout.connect(self.countDown)
        
        if LP_application is not None:
            self.LP_mainWin = LP_application.mainWin
            LP_application.addLPWidget(self,name=name, pos=pos)
                    
    def createControlElements(self):
        """ :param [param_name]: [description]"""
        
        self.timeDisplay_TimEd = QtWidgets.QTimeEdit(self)
        self.timeDisplay_TimEd.setDisplayFormat("HH:mm:ss")
        self.timeDisplay_TimEd.setStyleSheet("QTimeEdit {  font-weight: bold; font-size: 80px;} ");
        self.timeDisplay_TimEd.setCurrentSection(QtWidgets.QDateTimeEdit.MinuteSection)
        
        self.hour_PB = QtWidgets.QPushButton("hour", self)
        self.min_PB = QtWidgets.QPushButton("min ", self)
        self.sec_PB = QtWidgets.QPushButton("sec ", self)
        
        self.clear_PB = QtWidgets.QPushButton("clear", self)
        self.clear_PB.setStyleSheet("QPushButton { background-color: \"yellow\"; font-weight: bold; font-size: 20px;} ");
        
        self.reset_PB = QtWidgets.QPushButton("reset", self)
        self.reset_PB.setStyleSheet("QPushButton { background-color: \"blue\"; font-weight: bold; font-size: 20px;} ");
        
        self.startStop_PB = QtWidgets.QPushButton("Start", self)
        self.startStop_PB.setCheckable(True)
        self.startStop_PB.setStyleSheet("""  
                    QPushButton { background-color: "green";  font-weight: bold; font-size: 40px;}
                    QPushButton:checked { background-color: "red"; } """);
        
        self.controlsLayout = QtWidgets.QGridLayout()
        
        self.controlsLayout.addWidget(self.timeDisplay_TimEd, 0,0,1,3)
        self.controlsLayout.addWidget(self.hour_PB, 1,0 )
        self.controlsLayout.addWidget(self.min_PB, 1,1)
        self.controlsLayout.addWidget(self.sec_PB, 1,2)
        
        self.controlsLayout.addWidget(self.clear_PB, 2,0)
        self.controlsLayout.addWidget(self.reset_PB, 2,1)
        self.controlsLayout.addWidget(self.startStop_PB, 2,2)
        
        self.setLayout(self.controlsLayout)
        
        self.setTitle("{}".format(self.name))
        self.setStyleSheet("QGroupBox { font-weight: bold;} ");
        
        self.startStop_PB.clicked.connect(self.startStopTimer)
        
        self.hour_PB.clicked.connect(lambda: self.increaseTime(0))
        self.min_PB.clicked.connect(lambda: self.increaseTime(1))
        self.sec_PB.clicked.connect(lambda: self.increaseTime(2))

        self.clear_PB.clicked.connect(self.clearTimeEdit)
        self.reset_PB.clicked.connect(self.resetTimeEdit)
        
    def startStopTimer(self):
        """ :param [param_name]: [description]"""
        if self.startStop_PB.isChecked() :   
            self.timer.start(1000)
            self.startStop_PB.setText("Stop")
        else: 
            self.stop()
            
    def stop(self):
        """ :param [param_name]: [description]"""
        self.timer.stop()
        self.startStop_PB.setChecked(False)
        self.startStop_PB.setText("Start")
        
    def resetTimeEdit(self):
        """ :param [param_name]: [description]"""
        self.stop()
        self.timeDisplay_TimEd.setTime(self.setTime)
        self.curr_time = self.setTime
        
    def clearTimeEdit(self):
        """ :param [param_name]: [description]"""
        #~ self.timeDisplay_TimEd.clear()
        self.stop()
        self.timeDisplay_TimEd.setTime( self.time_zero )
        self.curr_time =  self.time_zero
        
    def increaseTime(self,section=0):
        """ :param [param_name]: [description]"""
        self.timeDisplay_TimEd.setCurrentSectionIndex(section)
        self.timeDisplay_TimEd.stepUp()
        self.updateSetTime()
            
    def updateSetTime(self):
        """ :param [param_name]: [description]"""
        self.setTime = self.timeDisplay_TimEd.time() # storing set time for reset
        self.curr_time = self.setTime
        
    def countDown(self, time_interval=1):
        """ :param [param_name]: [description]"""
        self.curr_time = self.curr_time.addSecs(-time_interval) # counting down time_interval 
        
        self.timeDisplay_TimEd.setTime(self.curr_time)
        
        if self.curr_time < QtCore.QTime(0,0,1,0) :
            self.timer.stop()
            self.startStop_PB.setDown(False)
            self.playSound()
            self.startStop_PB.setChecked(False);
            
            self.playSound()

    def playSound(self, soundname="beep.mp3", volume=100):
        """ playSound 
            !! might need to be added as resource
            :param [param_name]: [description]"""
        
        logging.debug("playing sound:{}".format(soundname) )
        
        QtMultimedia.QSound.play(soundname)
        
        #~ content= QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(soundname))
        #~ self.player.setMedia(content)
        #~ self.player.setVolume(volume)
        #~ self.player.play()

class StopWatch(QtWidgets.QGroupBox):
    """ Class doc """
    def __init__ (self, parent=None, LP_application=None, name="StopWatch", 
                        pos=lpwb.WidgetPosition.BOTTOMTAB, time_zero=None):
        """ Class initialiser """
        super().__init__(parent=None)
        
        self.name = name 
        
        self.time_zero = QtCore.QTime(0,0,0,0)
        
        self.curr_time = self.time_zero
        self.setTime   = self.time_zero
        
        self.createControlElements()
        self.player = QtMultimedia.QMediaPlayer(self)
        
        self.timer = QtCore.QTimer(self);
        self.timer.timeout.connect(self.countUp)
        
        if LP_application is not None:
            self.LP_mainWin = LP_application.mainWin
            LP_application.addLPWidget(self,name=name, pos=pos)
                    
    def createControlElements(self):
        """ :param [param_name]: [description]"""
        
        self.timeDisplay_TimEd = QtWidgets.QTimeEdit(self)
        self.timeDisplay_TimEd.setDisplayFormat("HH:mm:ss:z")
        self.timeDisplay_TimEd.setStyleSheet("QTimeEdit {  font-weight: bold; font-size: 80px;} ");
        self.timeDisplay_TimEd.setCurrentSection(QtWidgets.QDateTimeEdit.MinuteSection)
        
        self.hour_PB = QtWidgets.QPushButton("hour", self)
        self.min_PB = QtWidgets.QPushButton("min ", self)
        self.sec_PB = QtWidgets.QPushButton("sec ", self)
        
        self.clear_PB = QtWidgets.QPushButton("clear", self)
        self.clear_PB.setStyleSheet("QPushButton { background-color: \"yellow\"; font-weight: bold; font-size: 20px;} ");
        
        #~ self.reset_PB = QtWidgets.QPushButton("reset", self)
        #~ self.reset_PB.setStyleSheet("QPushButton { background-color: \"blue\"; font-weight: bold; font-size: 20px;} ");
        
        self.startStop_PB = QtWidgets.QPushButton("Start", self)
        self.startStop_PB.setCheckable(True)
        self.startStop_PB.setStyleSheet("""  
                    QPushButton { background-color: "green";  font-weight: bold; font-size: 40px;}
                    QPushButton:checked { background-color: "red"; } """);
        
        self.controlsLayout = QtWidgets.QGridLayout()
        
        self.controlsLayout.addWidget(self.timeDisplay_TimEd, 0,0,1,3)
        self.controlsLayout.addWidget(self.hour_PB, 1,0 )
        self.controlsLayout.addWidget(self.min_PB, 1,1)
        self.controlsLayout.addWidget(self.sec_PB, 1,2)
        
        self.controlsLayout.addWidget(self.clear_PB, 2,0)
        #~ self.controlsLayout.addWidget(self.reset_PB, 2,1)
        self.controlsLayout.addWidget(self.startStop_PB, 2,2)
        
        self.setLayout(self.controlsLayout)
        
        self.setTitle("{}".format(self.name))
        self.setStyleSheet("QGroupBox { font-weight: bold;} ");
        
        self.startStop_PB.clicked.connect(self.startStopTimer)
        
        self.hour_PB.clicked.connect(lambda: self.increaseTime(0))
        self.min_PB.clicked.connect(lambda: self.increaseTime(1))
        self.sec_PB.clicked.connect(lambda: self.increaseTime(2))

        self.clear_PB.clicked.connect(self.clearTimeEdit)
        #~ self.reset_PB.clicked.connect(self.resetTimeEdit)
        
    def startStopTimer(self):
        """ :param [param_name]: [description]"""
        if self.startStop_PB.isChecked() :   
            self.timer.start(100)
            self.startStop_PB.setText("Stop")
        else: 
            self.stop()
            
    def stop(self):
        """ :param [param_name]: [description]"""
        self.timer.stop()
        self.startStop_PB.setChecked(False)
        self.startStop_PB.setText("Start")
        
    def resetTimeEdit(self):
        """ :param [param_name]: [description]"""
        self.stop()
        self.timeDisplay_TimEd.setTime(self.setTime)
        self.curr_time = self.setTime
        
    def clearTimeEdit(self):
        """ :param [param_name]: [description]"""
        #~ self.timeDisplay_TimEd.clear()
        self.stop()
        self.timeDisplay_TimEd.setTime( self.time_zero )
        self.curr_time =  self.time_zero
        
    def increaseTime(self,section=0):
        """ :param [param_name]: [description]"""
        self.timeDisplay_TimEd.setCurrentSectionIndex(section)
        self.timeDisplay_TimEd.stepUp()
        self.updateSetTime()
            
    def updateSetTime(self):
        """ :param [param_name]: [description]"""
        self.setTime = self.timeDisplay_TimEd.time() # storing set time for reset
        self.curr_time = self.setTime
        
    def countUp(self, time_interval=100):
        """ :param [param_name]: [description]"""
        self.curr_time = self.curr_time.addMSecs(time_interval) # counting down time_interval 
        
        self.timeDisplay_TimEd.setTime(self.curr_time)
        
        if self.curr_time < QtCore.QTime(0,0,0,1) :
            self.timer.stop()
            self.startStop_PB.setDown(False)
            self.playSound()
            self.startStop_PB.setChecked(False);

    def playSound(self, soundname="beep.wav", volume=100):
        """ :param [param_name]: [description]"""
        
        logging.debug("playing sound:{}".format(soundname) )
        
        content= QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(soundname))
        
        self.player.setMedia(content)
        self.player.setVolume(volume)
        self.player.play()
        
            
