"""
________________________________________________________________________

:PROJECT: labPy

*labPyWorkbench: A graphical environment for control and evaluation of microfluidic experiments*

:details: : 

:file:    labPyWorkbench.py

:author:  mark doerr <mark.doerr@uni.greifswald.de> : contrib.
          
:date: (creation)          20180907
:date: (last modification) 20181104
.. note:: some remarks
.. todo:: - data logger
          - det. logger
          - pump logger
          - 3D display
          - pump simulator
          - temperature logger
          - 3D display of real data
          - python Editor 
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

import sys, os
import logging
from enum import Enum
from datetime import datetime

from PySide2 import QtCore, QtWidgets, QtGui

import labpy.labpy_rc
import labpy.widgets.config_widget as lpwc
    
class WidgetPosition(Enum):
    """ Standard widget positions """
    CENTER  = 1      
    TOOLBAR = 2
    TOP     = 3
    LEFT    = 4
    RIGHT   = 5
    BOTTOM  = 6
    BOTTOMTAB  = 7
    DIALOG  = 8

class LP_TabWidget(QtWidgets.QTabWidget):
    """ Tab Widget Container for all process and process info widgets,
        with reduced tab height and drag event handling
        .. todo::  - add every created widget to view menu
                     by overwriting addTab method
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parent = parent
        self.setTabsClosable(True)
        self.setAcceptDrops(True)
        
        #~ self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        #~ self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
                
        self.setStyleSheet( """
            QTabBar::tab { font: 8pt; height: 3.3ex; } /* tab font and height */
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: lightGrey;
            }
            QTabBar::tab:selected {
               /* border-color: #9B9B9B;
                border-bottom-color: #C2C7CB; / same as pane color */
            }
            QTabBar::tab:!selected {
               /* margin-top: 2px;  make non-selected tabs look smaller */
            }"""
        )

    def addTab(self, *args, **kwargs):
        """ overwriting original method to add tabs to view
           :param [param_name]: [description]"""
        # add toggle action to view menu
        index =  super().addTab(*args, **kwargs)
        return index 
        
    # this is required for the LP_TabWidget to accept drags and drops
    def dragEnterEvent(self, event): 
        if event.mimeData().hasFormat('application/dp-dnditemdata'):
            if event.source() == self:  # dragging inside the CentralTabWidget
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()
        super().dragEnterEvent(event)

    def dropEvent(self, event): 
        if event.mimeData().hasFormat('application/dp-dnditemdata'):
            # triggering new_action to generate a new tab if no tabs present...
            if self.count() == 0:
                self.parent.new_act.trigger()
                event.acceptProposedAction() # changed from event.accept()
            else:
                logging.info("central tab widget: new data existis ")
        else : 
            event.ignore()
            
    def readSettings(self):
        """ :param [param_name]: [description]"""
        pass
        

class LP_MainWindow(QtWidgets.QMainWindow):
    """labPy Workbench main application window
    .. todo:: - dpi aware fonts/sizes
              - add every created widget to view menu
    """
    
    editCutSig = QtCore.Signal()
    
    unselectAllSig = QtCore.Signal()
    
    startAll_Sig = QtCore.Signal()
    stopAll_Sig = QtCore.Signal()
    autoSaveTimer_Sig = QtCore.Signal()
    
    monitorDataStart_Sig = QtCore.Signal()
    monitorDataStop_Sig = QtCore.Signal()
    
    def __init__(self, parent=None, settings=None, 
                       appname="", description="",
                       toolbar=True, bottomtab=True):
        super().__init__(parent)
        
        self.appname = appname
        self.description = description
        
        self.LP_QApplication = parent
        self.settings = settings
        
        self.view_toggle_dic = {}
        
        self.readSettings()
        
        self.setWindowTitle(self.appname + " (" + __version__ + ")" )
        self.setWindowIcon(QtGui.QIcon(':/linux/actions/scalable/' + 'run'))
        
        # testing screen resolution - this can be used to scale icons, 
        # s. http://doc.qt.io/qt-5/scalability.html
        self.dpi = QtGui.QGuiApplication.primaryScreen().logicalDotsPerInch()
        #~ logging.debug("screen resolution dpi: {}".format(self.dpi) )
        
        self.createActions()
        self.createMenus()
        
        if toolbar : self.createToolbars()
        self.createStatusbar()
        
        # configuration dialog
        self.config_dialog = lpwc.ConfigDialogWidget(self, settings=self.settings)
        self.main_conf_tab = MainConfigTab(self.config_dialog)
        self.config_dialog.addConfigTab(self.main_conf_tab, tab_name="Main Config" )
        
        # central tab widget
        self.central_TWDG =  LP_TabWidget(self)  
        self.setCentralWidget(self.central_TWDG)
        self.central_TWDG.tabCloseRequested.connect(self.closeCentralTab)
        self.central_TWDG.currentChanged.connect(self.centralTabIndexChanged)
        
        # bottom tab doc widget
        if bottomtab: self.createBottomTab()
    
        self.showMaximized()
        
        # auto save timer
        autosave_timer = QtCore.QTimer(self)
        autosave_timer.timeout.connect(lambda : self.autoSaveTimer_Sig.emit() )
        autosave_timer.start(self.autosave_timer_intervall)
        
    def createActions(self):
        resource_prefix = ':/linux/actions/24/'
        resource_scale_prefix = ':/linux/actions/scalable/'
        
        self.new_proj_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix + 'new'),"New &Project", self, 
                        shortcut=QtGui.QKeySequence.New,
                        statusTip="Create new Project", 
                        triggered=lambda new_project_name="": self.newProject(new_project_name="" ) )
        self.open_proj_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'open'),"&Open Project ...", self, 
                         shortcut=QtGui.QKeySequence.Open,
                         statusTip="Open previous project ....", 
                         triggered=self.openProject)
        
        self.new_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix + 'new'),"New &Experiment", self, 
                        shortcut=QtGui.QKeySequence.New,
                        statusTip="Create new experiment, with related csv data", 
                        triggered=lambda new_csv_filename="": self.newDataFile(new_csv_filename="" ) )
        self.open_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'open'),"Open Exper&iment ...", self, 
                         shortcut=QtGui.QKeySequence.Open,
                         statusTip="Open previous experiment ....", 
                         triggered=self.openData)
        self.save_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'save'), "&Save", self, 
                         shortcut=QtGui.QKeySequence.Save,
                         statusTip="Save experiment data to disk", 
                         triggered=self.save)
        self.saveAs_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'save_as'), "Save &As...", self,
                            shortcut=QtGui.QKeySequence.SaveAs,
                            statusTip="Save the document under a new name",
                            triggered=self.saveAs)
                            
        self.undo_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'undo'),"&Undo", self, 
                         shortcut=QtGui.QKeySequence.Undo,
                         statusTip="Undo last change", 
                         triggered=self.undo)
        self.redo_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'redo'),"&Undo", self, 
                         shortcut=QtGui.QKeySequence.Redo,
                         statusTip="Redo last change", 
                         triggered=self.redo)
                                                
        start_stop_icon = QtGui.QIcon()
        start_stop_icon.addPixmap(resource_scale_prefix + 'run', QtGui.QIcon.Normal,  QtGui.QIcon.Off)
        start_stop_icon.addPixmap(resource_scale_prefix + 'stop', QtGui.QIcon.Normal, QtGui.QIcon.On)        
        self.start_stop_all_Act = QtWidgets.QAction(start_stop_icon,"&Run", self, 
                                shortcut="Ctrl+r",
                                statusTip="start all measurements", 
                                checkable=True,
                                triggered=self.startStopAll)
        pause_icon = QtGui.QIcon()
        pause_icon.addPixmap(resource_scale_prefix + 'pause', QtGui.QIcon.Normal,  QtGui.QIcon.Off)
        pause_icon.addPixmap(resource_scale_prefix + 'run', QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pause_all_Act = QtWidgets.QAction(pause_icon,"&Pause", self, 
                        shortcut="Ctrl+p",
                        statusTip="start all measurements", 
                        checkable=True,
                        triggered=self.startStopAll)
        self.pause_all_Act.setEnabled(False)
                        
        self.zoom_in_Act = QtWidgets.QAction(QtGui.QIcon(resource_scale_prefix + 'zoom-in'),"zoom &in", self, 
                            shortcut="Ctrl++",
                            statusTip="Zoom in", 
                            triggered=self.zoomIn)
        self.zoom_default_Act = QtWidgets.QAction(QtGui.QIcon(resource_scale_prefix + 'zoom-default'),"zoom &default", self, 
                            shortcut="Shift+Ctrl++",
                            statusTip="Zoom default", 
                            triggered=self.zoomDefault)
        self.zoom_out_Act = QtWidgets.QAction(QtGui.QIcon(resource_scale_prefix +'zoom-out'),"zoom &out", self, 
                             shortcut="Ctrl+-",
                             statusTip="Zoom in", 
                             triggered=self.zoomOut)
                             
        self.monitor_Act = QtWidgets.QAction(QtGui.QIcon(resource_scale_prefix +'find'),"&Monitor", self, 
                                shortcut="Ctrl+m",
                                statusTip="Monitor data stream", 
                                checkable=True,
                                triggered=self.monitorDataStream)
                                
        self.annotate_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'annotate'),"&Annotate", self, 
                                shortcut="Ctrl+a",
                                statusTip="Annotate Data",
                                triggered=self.annotateData)

        self.config_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'config'),"&Config", self, shortcut="ctrl+F1",
                                       triggered=self.configAction)
                                       
        self.about_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'about'),"A&bout", self, shortcut="F1",
                                       triggered=self.aboutAction)

        self.exit_Act = QtWidgets.QAction(QtGui.QIcon(resource_prefix +'exit'),"E&xit", self, 
                         shortcut="Ctrl+Q",
                         statusTip="Exit/Quit labPy workbench", 
                         triggered=self.close)

    def newProject(self, new_csv_filename="" ):  
        if new_csv_filename == "" :
            url1 = QtCore.QUrl("file://")       # def. location 1
            url2 = QtCore.QUrl("file:///home")  # def. location 2
            urls = [url1,url2]
            new_project_dia = QtWidgets.QFileDialog()
            #~ new_project_dia.setSidebarUrls(urls);
            
            new_project_dir = new_project_dia.getExistingDirectory(self, 'Select a new Project directory for saving data...',
                            dir=self.LP_QApplication.default_working_dir, options=QtWidgets.QFileDialogShowDirsOnly)
        
        # now generating a new data
        if new_project_dir != "" :
            
            self.LA_QApplication.default_working_dir =  new_project_dir
           # self.dp_default_working_dir = curr_FI.absolutePath()
                
    def openProject(self):
        url1 = QtCore.QUrl("file://")
        url2 = QtCore.QUrl("file:///home")
        urls = [url1,url2]
        open_project_dia = QtWidgets.QFileDialog()
        #~ new_project_dia.setSidebarUrls(urls)
        
        open_project_dir = open_project_dia.getExistingDirectory(self, 'Open a Project directory for saving data...',
                        dir=self.LP_QApplication.default_working_dir, options=QtWidgets.QFileDialogShowDirsOnly)
        
        # now generating a new data
        if open_project_dir != "" :
            
            self.LA_QApplication.default_working_dir =  open_project_dir
           # self.dp_default_working_dir = curr_FI.absolutePath()
        
    def openData(self):
        """ should be moved to widget"""
        url1 = QtCore.QUrl("file://")
        url2 = QtCore.QUrl("file:///home")
        urls = [url1,url2]
        new_filname_dia = QtWidgets.QFileDialog()
        #~ new_filname_dia.setSidebarUrls(urls);
    
        new_filename_default = self.LP_application.default_working_dir
        
        csv_filename,csv_extension  = new_filname_dia.getOpenFileName(self, 'Select a csv file to be opened...',new_filename_default,'CSV files (*.csv)')
        
        logging.debug(csv_filename)
        
        # now generating a new data
        if csv_filename == "" :
            logging.debug("creating new file %s" % csv_filename)
            
        else :
            logging.debug("opening %s" % csv_filename)
            curr_FI =  QtCore.QFileInfo(csv_filename)
            self.dp_default_working_dir = curr_FI.absolutePath()
            
            #self.loadCSVFile(csv_filename)
            
    def loadCSVFile(self, csv_filename):
        """ should be moved to widget"""
        curr_FI =  QtCore.QFileInfo(csv_filename)
        csv_basename = curr_FI.fileName()
        
        with open(csv_filename, 'rb' ) as csv_file:
            x_dat, y_dat = np.loadtxt(csv_file, delimiter=",", skiprows=1, unpack=True)
        
        # now generating new plot and adding tab
        plot_canv = PlotCanvas(self)
        plot_canv.plotXY(x_dat,y_dat, plot_title=csv_basename)
        
        self.central_tw.addTab(plot_canv , csv_basename)
    
    def newDataFile(self, new_csv_filename="" ):  
        if new_csv_filename == "" :
            url1 = QtCore.QUrl("file://")       # def. location 1
            url2 = QtCore.QUrl("file:///home")  # def. location 2
            urls = [url1,url2]
            new_filname_dia = QtWidgets.QFileDialog()
            #~ new_filname_dia.setSidebarUrls(urls);
        
            new_filename_default = self.dp_default_working_dir + "/%s_%s.csv" %( QtCore.QDateTime.currentDateTime().toString("yyMMdd_hhmmss"),"process")
            new_csv_filename = new_filname_dia.getSaveFileName(self, 'Select New empty data file to be used for saving data...',new_filename_default,'CSV files (*.csv)')
        
        # now generating a new data
        if new_csv_filename != "" :
            curr_FI = QtCore.QFileInfo(new_csv_filename)
            logging.info("try to replace by weak list if performance is too slow or memory intensive")
            
            logging.debug("creating new file %s" % new_csv_filename)
            self.dp_default_working_dir = curr_FI.absolutePath()
                                           
    def startStopAll(self):
        """ :param [param_name]: [description]"""
        logging.debug("running measurements ..." )
        
        self.pause_all_Act.setEnabled(True)
        
        if self.start_stop_all_Act.isChecked():
            self.startAll_Sig.emit()
            self.start_stop_all_Act.setToolTip("Stop")
        else:
            self.stopAll_Sig.emit()
            self.start_stop_all_Act.setToolTip("Start")
            self.pause_all_Act.setEnabled(False)
        
        #~ self.global_timer_TE.start()
        
        #self.global_timer_TE = MeasTimerWidget()
        
    def monitorDataStream(self):
        """ :param [param_name]: [description]"""
        logging.debug("monitoring measurements ..." )
        
        if self.monitor_Act.isChecked():
            self.monitorDataStart_Sig.emit()
            #~ self.start_stop_all_Act.setToolTip("Stop")
        else:
            self.monitorDataStop_Sig.emit()
            #~ self.start_stop_all_Act.setToolTip("Start")
            #~ self.pause_all_Act.setEnabled(False)
        
    def annotateData(self):
        """ generic edit-undo method"""
        #~ self.redo_Sig.emit()
        logging.debug("annotate data {}".format(1) )
        
    def save(self):
        """ generic save method"""
        #~ self.saveAll_Sig.emit()
        logging.debug("save{}".format(1) )
        
    def saveAs(self):
        """ generic save as ... method"""
        #~ self.saveAs_Sig.emit()
        logging.debug("save as{}".format(1) )
        
    def undo(self):
        """ generic edit-undo method"""
        #~ self.undo_Sig.emit()
        logging.debug("undo {}".format(1) )
    
    def redo(self):
        """ generic edit-undo method"""
        #~ self.redo_Sig.emit()
        logging.debug("undo {}".format(1) )
        
    def zoomIn(self):
        """ generic zoom in method"""
        #~ curr_view = self.central_tw.currentWidget()        
        #~ if(curr_view) :
            #~ curr_view.zoomIn()
            #~ self.zoomIn_Sig.emit()
        logging.debug("zooming in{}".format(1) )
        
    def zoomDefault(self):
        """ generic zoom default method"""
         #~ self.zoomDefault_Sig.emit()
        #~ curr_view = self.central_tw.currentWidget()        
        #~ if(curr_view) :
            #~ curr_view.zoomIn()
        logging.debug("zooming default{}".format(1) )
        
    def zoomOut(self):
        """ generic zoom out method"""
         #~ self.zoomOut_Sig.emit()
        logging.debug("zooming out{}".format(1) )
        #~ curr_view = self.central_tw.currentWidget()
        #~ if(curr_view) :
            #~ curr_view.zoomOut()
            
    def centralTabIndexChanged(self,index):
        """ :param [param_name]: [description]"""
        tab_name = self.central_TWDG.tabText(index)
        #~ logging.debug("centr tab curr index name{}".format(tab_name) )
        
    def bottomTabIndexChanged(self,index):
        """ :param [param_name]: [description]"""
        tab_name = self.bottom_TWDG.tabText(index)
        #~ logging.debug("bott curr tab name{}".format(tab_name) )
        
        for curr_index in range(self.bottom_TWDG.count()):
            #~ logging.debug("curr index{}".format(curr_index) )
            if curr_index == index:
                pass
                #~ logging.debug("enable{}".format(curr_index) )
                try:
                    pass #self.bottom_TWDG.widget(curr_index).enableAllActions(enabled=True)
                except Exception as err:
                    logging.error("err {}".format(err) )
                    continue
            else :
                logging.debug("disable{}".format(curr_index) )
                try:
                    pass #self.bottom_TWDG.widget(curr_index).enableAllActions(enabled=False)
                except Exception as err:
                    logging.error("err {}".format(err) )
                    continue
            
    def closeCentralTab(self,index):
        """ :param [param_name]: [description]"""
        tab_name = self.central_TWDG.tabText(index)
        #~ logging.debug("centr tab name{}".format(tab_name) )
        self.view_toggle_dic[self.central_TWDG.widget(index)].setChecked(False)
        self.central_TWDG.removeTab(index)

    def closeBottomTab(self,index):
        """ :param [param_name]: [description]"""
        tab_name = self.bottom_TWDG.tabText(index)
        #~ logging.debug("bott tab name{}".format(tab_name) )
        self.view_toggle_dic[self.bottom_TWDG.widget(index)].setChecked(False)
        self.bottom_TWDG.removeTab(index)

    def configAction(self):
        """ add settings """
        self.config_dialog.show()
        
    def aboutAction(self):
        """ to-do: add
        """
        QtWidgets.QMessageBox.about(self, "About {appname}".format(appname=self.appname +  __version__), 
                           self.description.format(appname= self.appname +  __version__))
        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.new_proj_Act)
        self.fileMenu.addAction(self.open_proj_Act)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.new_Act)
        self.fileMenu.addAction(self.open_Act)
        self.fileMenu.addAction(self.exit_Act)
        self.fileMenu.addSeparator()
        
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undo_Act)
        self.editMenu.addAction(self.redo_Act)
        self.editMenu.addSeparator()

        self.runMenu = self.menuBar().addMenu("&Run")
        self.runMenu.addAction(self.start_stop_all_Act)
        self.runMenu.addAction(self.pause_all_Act)
        
        self.viewMenu = self.menuBar().addMenu("&View")
        self.viewMenu.addAction(self.zoom_in_Act)
        self.viewMenu.addAction(self.zoom_out_Act)
        self.viewMenu.addAction(self.zoom_default_Act)
        self.viewMenu.addSeparator()
        
        # tools, e.g. calculators
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        
        # configuration and help
        self.aboutMenu = self.menuBar().addMenu("&Config/Help")
        self.aboutMenu.addAction(self.config_Act)
        self.aboutMenu.addAction(self.about_Act)
    
    def createToolbars(self):
        self.file_TB = self.addToolBar("File")
        self.file_TB.setObjectName("File_TB")
        self.file_TB.addAction(self.new_Act)
        
        # The Edit position is reseved for external Widgets to place their Edit buttons here
        self.edit_TB = self.addToolBar("Edit")
        self.edit_TB.setObjectName("Edit_TB")
        self.edit_TB.addAction(self.annotate_Act)
 
        self.run_TB = self.addToolBar("Run")
        self.run_TB.setObjectName("Run_TB")
        
        self.run_TB.addAction(self.monitor_Act)
        self.run_TB.addAction(self.start_stop_all_Act)
        self.run_TB.addAction(self.pause_all_Act)

        self.zoom_TB = self.addToolBar("Zoom")
        self.zoom_TB.setObjectName("Zoom_TB")
        #~ zoom_slider = QSlider(QtCore.Qt.Horizontal)
        #~ zoom_slider.setRange(5, 200)
        #~ zoom_slider.setValue(100)
        #~ self.zoom_TB.addWidget(zoom_slider)
        self.zoom_TB.addAction(self.zoom_in_Act)
        self.zoom_TB.addAction(self.zoom_default_Act)
        self.zoom_TB.addAction(self.zoom_out_Act)
        
        # tools, e.g. calculators
        self.tools_TB = self.addToolBar("Tools")
        self.tools_TB.setObjectName("Tools_TB")
        
        # configuration and help
        self.config_TB = self.addToolBar("Config")
        self.config_TB.setObjectName("Config_TB")
        self.config_TB.addAction(self.config_Act)

    def createStatusbar(self):
        """ adds status bar to main window"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("labPy Workbench Ready")
        
    def createBottomTab(self):
        """ adds a bottom tab widget area to main window
            :param [param_name]: [description]"""
        self.bottom_dock = QtWidgets.QDockWidget("Views")
        self.bottom_dock.setObjectName("Views")
        
        self.bottom_dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea 
                                         | QtCore.Qt.LeftDockWidgetArea 
                                         | QtCore.Qt.RightDockWidgetArea)
        
        self.bottom_TWDG = LP_TabWidget(self)
        self.bottom_dock.setWidget(self.bottom_TWDG)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.bottom_dock)
        self.viewMenu.addAction(self.bottom_dock.toggleViewAction())
        
        self.bottom_TWDG.tabCloseRequested.connect(self.closeBottomTab)
        self.bottom_TWDG.currentChanged.connect(self.bottomTabIndexChanged)
        
        
    def writeSettings(self):
        """ :param [param_name]: [description]"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
    def readSettings(self):
        """ :param [param_name]: [description]"""
        try:
            self.autosave_timer_intervall = int(self.settings.value("autosave-interval"))
        except Exception as err:
            logging.error("Settings error:{}".format(err) )
            self.autosave_timer_intervall = 30000 # unit: ms
            
    def restoreWindowSettings(self):
        """ :param [param_name]: [description]"""
        self.restoreGeometry(self.settings.value("geometry"))
        self.restoreState(self.settings.value("windowState"))
        
    def closeEvent(self, event):
        """ :param [param_name]: [description]"""
        self.writeSettings()
        shutdown_message =  'Shutting down workbench now - but first saving everything ... \n'
        #~ sys.stderr.write(shutdown_message)
        #~ self.saveCSVAction()
       
        super().closeEvent(event)
        event.accept()
        
    def addConfigTab(self, widget=None, tab_name="Main Config" ):
        """ :param [param_name]: [description]"""
        self.config_dialog.addConfigTab(widget=widget, tab_name=tab_name )

class LP_Application(QtWidgets.QApplication):
    """Main labPy Qt5-Application"""
    def __init__(self, args, appname="labPyWorkbench", description="This is the labPyWorkbench",
                 toolbar=True, bottomtab=True):
        super().__init__(args)
        
        self.appname = appname
        self.description = description
        
        self.recentFileActs = []
        
        self.readAppSettings()
        
        self.mainWin = LP_MainWindow(settings=self.settings, 
                                     appname=self.appname, description=self.description,
                                     toolbar=toolbar, bottomtab=bottomtab)
                                     
        self.lastWindowClosed.connect(self.writeAppSettings)
        
    def readAppSettings(self):
        """read application settings"""
        self.settings = QtCore.QSettings("labPy", self.appname)
        
        try:
            self.default_working_dir = self.settings.value("application/working_dir")
        except Exception as err:
            logging.error("Settings error:{}".format(err) )
            self.default_working_dir = os.getcwd()

        logging.debug("curr def workdir : {}".format(self.default_working_dir) )
            
        #~ old recent_files_list = QtCore.QStringList()
        #~ old recent_files_list = self.settings.value("files/recent_files").toStringList()
        # s. qt5 recent file example
        #~ recent_files_list = settings.value('files/recentFileList', [])
        
        #~ for recent_file_name in recent_files_list: 
            #~ self.new_experiment_action(recent_file_name)
           
    def writeAppSettings(self):
        self.settings.setValue("application/working_dir", self.default_working_dir )
        
        #~ recent_files_list = QtCore.QStringList() # this is freshly generated to contain the latest state
        #~ for experiment in self.experiments.itervalues() :
            #~ recent_files_list << experiment.xmlFileInfo().absoluteFilePath()
        #~ print(recent_files_list)
        #~ self.settings.setValue("files/recent_files", recent_files_list)
    
    def toggleWigetView(self, widget=None, name="", pos=None):
        """ :param [param_name]: [description]"""
        widget_pos_dict = { WidgetPosition.CENTER : None,
                    WidgetPosition.TOOLBAR : None,
                    WidgetPosition.LEFT : QtCore.Qt.LeftDockWidgetArea,
                    WidgetPosition.RIGHT : QtCore.Qt.RightDockWidgetArea,
                    WidgetPosition.TOP : QtCore.Qt.TopDockWidgetArea,
                    WidgetPosition.BOTTOM : QtCore.Qt.BottomDockWidgetArea,
                    WidgetPosition.BOTTOMTAB : QtCore.Qt.BottomDockWidgetArea }
        
        #~ logging.debug("widg name: {}".format(name) )
        #~ logging.debug("pos: {}  ".format(pos) )
        
        if pos == WidgetPosition.CENTER :
            if widget.isVisible():
                logging.debug("widget is already open {} - closing now".format(name) )
                curr_index = self.mainWin.central_TWDG.indexOf(widget)
                self.mainWin.central_TWDG.removeTab(curr_index) 
            else:
                new_tab_idx = self.mainWin.central_TWDG.addTab(widget, name)
                self.mainWin.central_TWDG.setCurrentIndex(new_tab_idx)
                
        elif pos == WidgetPosition.TOOLBAR :
            if not widget.isVisible():
                toolbar = self.mainWin.addToolBar(name)
                toolbar.setObjectName(name)
                toolbar.addWidget(widget)
        
        elif pos == WidgetPosition.TOP :
            if not widget.isVisible():
                dock = QtWidgets.QDockWidget(name)
                dock.setObjectName(name)
                dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea 
                                             | QtCore.Qt.TopDockWidgetArea 
                                             | QtCore.Qt.LeftDockWidgetArea 
                                             | QtCore.Qt.RightDockWidgetArea)
                dock.setWidget(widget)
                self.mainWin.addDockWidget(widget_pos_dict[pos],dock)
                self.mainWin.viewMenu.addAction(dock.toggleViewAction())
                
        elif pos == WidgetPosition.BOTTOM :
            if not widget.isVisible():
                dock = QtWidgets.QDockWidget(name)
                dock.setObjectName(name)
                dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea 
                                             | QtCore.Qt.LeftDockWidgetArea 
                                             | QtCore.Qt.RightDockWidgetArea)
                dock.setWidget(widget)
                self.mainWin.addDockWidget(widget_pos_dict[pos],dock)
                self.mainWin.viewMenu.addAction(dock.toggleViewAction())
                
        elif pos == WidgetPosition.BOTTOMTAB :
            if widget.isVisible():
                #~ logging.debug("widget is already open {} - closing now".format(name) )
                curr_index = self.mainWin.bottom_TWDG.indexOf(widget)
                #~ curr_index = self.mainWin.bottom_TWDG.setCurrentIndex(curr_index)
                self.mainWin.bottom_TWDG.removeTab(curr_index)
            else:
                new_tab_idx = self.mainWin.bottom_TWDG.addTab(widget, name)
                #~ logging.debug("tabnum:  {} - name {} ".format(new_tab_idx, name) )
                self.mainWin.bottom_TWDG.setCurrentIndex(new_tab_idx)
        else :
            if not widget.isVisible():
                dock = QtWidgets.QDockWidget(name)
                dock.setObjectName(name)
                dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea 
                                             | QtCore.Qt.LeftDockWidgetArea 
                                             | QtCore.Qt.RightDockWidgetArea)
                dock.setWidget(widget)
                self.mainWin.addDockWidget(widget_pos_dict[pos],dock)
                
                self.mainWin.viewMenu.addAction(dock.toggleViewAction())
            else:
                logging.debug("bring tab to front {}".format(name) )
        
    def addLPWidget(self, widget=None, name="", description="default widget description", 
                    pos=WidgetPosition.LEFT, shortcut="", visible=None, tool=False ):
        """ :param widget: LP widget to be added
            :param name: LP widget to be added 
            :param pos: position ()"""
            
        # only if not new doc widget ?
        self.mainWin.menu_toogle_view_Act = QtWidgets.QAction(text=name, parent=self.mainWin, 
                            shortcut=shortcut,
                            statusTip=description, 
                            checkable=True,
                            triggered=lambda widget=widget, name=name, pos=pos: self.toggleWigetView(widget=widget, name=name, pos=pos ) )
                            
        self.mainWin.view_toggle_dic[widget] = self.mainWin.menu_toogle_view_Act
        
        if tool == True :
            self.mainWin.toolsMenu.addAction(self.mainWin.menu_toogle_view_Act)
            if visible is None: visible = False # tools are not visible by default
        else :
            self.mainWin.viewMenu.addAction(self.mainWin.menu_toogle_view_Act)
            if visible is None: visible = True # everything else is visible by default
        if visible is not None :
            if visible : self.mainWin.menu_toogle_view_Act.trigger()
            
    def run(self):
        """ starts the main execution loop of the QtApplication, 
            but restoring the window settings first """
        
        self.mainWin.restoreWindowSettings()
        self.exec_()
                
class MainConfigTab(QtWidgets.QWidget):
    """Config tab of main window application for config dialog """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.createControlElements()
        
        parent.accepted.connect(self.saveSettings)
        
    def createControlElements(self):
        """ :param [param_name]: [description]"""
        
        self.generalGroup = QtWidgets.QGroupBox("General")
        
        self.auto_save_LAB = QtWidgets.QLabel("Autosave interval")
        self.auto_save_LAB.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.auto_save_SB = QtWidgets.QSpinBox()
        self.auto_save_SB.setRange(60000, 1800000)
        self.auto_save_SB.setSingleStep(60000)
        self.auto_save_units_LAB = QtWidgets.QLabel("ms")
        
        self.auto_save_HL = QtWidgets.QHBoxLayout()
        self.auto_save_HL.addWidget(self.auto_save_LAB)
        self.auto_save_HL.addWidget(self.auto_save_SB)
        self.auto_save_HL.addWidget(self.auto_save_units_LAB)
        
        self.generalGroup.setLayout(self.auto_save_HL)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.generalGroup)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)
        
    def setSettings(self, settings):
        """ :param [param_name]: [description]"""
        self.settings = settings
        
        try:
            self.auto_save_SB.setValue(int(self.settings.value("autosave-interval")))
        except Exception as err:
            logging.error("Settings error:{}".format(err) )
            
    def saveSettings(self):
        """ :param [param_name]: [description]"""
        logging.debug("saving main settings {}".format(1) )
        self.settings.setValue("autosave-interval", self.auto_save_SB.value())
