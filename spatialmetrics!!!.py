# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialMetrics
                                 A QGIS plugin
 This plugins calculates Spatial Metrics for Spatial Indicators
                              -------------------
        begin                : 2013-12-13
        copyright            : (C) 2013 by Leon
        email                : mugwizal@gmail.som
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4.QtCore import QSettings, QVariant, Qt, SIGNAL
from PyQt4.QtGui import QDialog, QDialogButtonBox, QMessageBox
# Initialize Qt resources from file resources.py
from qgis.gui import *
import qgis.utils
import resources_rc
# Import the code for the dialog
from spatialmetricsdialog import SpatialMetricsDialog
from visualizationdialog import VisualizationDialog
from TSSvisualizationdialog import TSSVisualizationDialog
from TSSdialog import TSSDialog
from Animationdialog import AnimationDialog
from SIAnimationdialog import SIAnimationDialog
import os.path
import os,  glob
import string
import numpy as np
from osgeo import gdal
import time
import sys


class SpatialMetrics:
        
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("/locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'spatialmetrics_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
        # Create the dialog (after translation) and keep reference
        self.dlg = SpatialMetricsDialog()
        self.dlg2 = VisualizationDialog()
        self.dlg3 = TSSDialog()
        self.dlg4 = AnimationDialog()
        self.dlg5 = SIAnimationDialog()
        self.dlg6 = TSSVisualizationDialog()
        self.canvas = self.iface.mapCanvas()

        
        #Initial  variables for opening files
##        QObject.connect( self.dlg.ui.pushButton_3, SIGNAL( "clicked()" ), self.Preprocessing) #link the button to the function preprocess input files
        QObject.connect( self.dlg3.ui.pushButton_7, SIGNAL( "clicked()" ), self.DisplayTSSnames)
        QObject.connect( self.dlg3.ui.pushButton_6, SIGNAL( "clicked()" ), self.TSSgraphs)
        
        #SI visualization
        self.loadSI()   #load on combo box list of  spatial indicators
        self.loadES() #load on combo box list of Ecosystem services 
        QObject.connect(self.dlg.ui.comboBox_2, SIGNAL("currentIndexChanged (const QString&)"),   self.changeCombo) #link the ES list to SI list
        QObject.connect(self.dlg.ui.comboBox_3, SIGNAL("currentIndexChanged (const QString&)"),   self.desableinactivebuttons) #link the ES list to SI list
        QObject.connect( self.dlg.ui.btnBaseDir_3, SIGNAL( "clicked()" ), self.selectDir1 ) #link the button to the function of selecting the directory
        self.dlg.ui.buttonBox.accepted.connect(self.SMcalc)
        self.dlg.ui.buttonBox.rejected.connect(self.dlg.reject)
        QObject.connect( self.dlg.ui.pushButton_6, SIGNAL( "clicked()" ), self.graphs) #link the button to the function of selecting the viewtss
        QObject.connect( self.dlg.ui.pushButton_5, SIGNAL( "clicked()" ), self.loadMaps) #link the button to the function animation
        QObject.connect( self.dlg5.ui.pushButton_2, SIGNAL( "clicked()" ), self.Anim)
        QObject.connect( self.dlg5.ui.pushButton_3, SIGNAL( "clicked()" ), self.Next)
        QObject.connect( self.dlg5.ui.pushButton, SIGNAL( "clicked()" ), self.Previous)
        QObject.connect( self.dlg5.ui.pushButton_4, SIGNAL( "clicked()" ), self.First)
        QObject.connect( self.dlg5.ui.pushButton_5, SIGNAL( "clicked()" ), self.Last)
        
        # Mapstack series visualization
        QObject.connect( self.dlg3.ui.btnBaseDir_3, SIGNAL( "clicked()" ), self.selectDir2 ) #link the button to the function of selecting the directory
        QObject.connect( self.dlg3.ui.btnBaseDir_3, SIGNAL( "clicked()" ), self.loadMapStackCoreName ) #link the button to the function of selecting the directory
        QObject.connect( self.dlg3.ui.pushButton_5, SIGNAL( "clicked()" ), self.actionStart)
        QObject.connect( self.dlg4.ui.pushButton_2, SIGNAL( "clicked()" ), self.ActionAnim)
        QObject.connect( self.dlg4.ui.pushButton_3, SIGNAL( "clicked()" ), self.actionNext)
        QObject.connect( self.dlg4.ui.pushButton, SIGNAL( "clicked()" ), self.actionPrevious)
        
        QObject.connect( self.dlg4.ui.pushButton_4, SIGNAL( "clicked()" ), self.actionStart)
        QObject.connect( self.dlg4.ui.pushButton_5, SIGNAL( "clicked()" ), self.actionLast)
        
        
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction( QIcon(":/plugins/spatialmetrics/icon2.png"), u"Spatial Indicator", self.iface.mainWindow())
        self.action2 = QAction( QIcon(":/plugins/spatialmetrics/icon1.png"), u"PCRaster Time series Viewer", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        self.action2.triggered.connect(self.TSS)
        # Add toolbar button and menu item
        self.iface.addPluginToMenu(u"&spatial planning tool ", self.action)
        self.iface.addPluginToMenu(u"&spatial planning tool ", self.action2)
        self.iface.addToolBarIcon(self.action)
        self.iface.addToolBarIcon(self.action2)
    
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&spatial planning tool ", self.action)
        self.iface.removeToolBarIcon(self.action)        
        self.iface.removePluginMenu(u"&spatial planning tool ", self.action2)
        self.iface.removeToolBarIcon(self.action2)
        
    def run(self):
        self.dlg.show() # show the dialog
        result = self.dlg.exec_() # Run the dialog event loop
        
    def view(self):
        self.dlg2.move(10, 300)
        self.dlg2.show()# show the dialog
        
    def TSSview(self):
        self.dlg6.move(10, 300)
        self.dlg6.show()# show the dialog        

    def TSS (self):
        self.dlg3.show()# show the dialog
        
    def AnimationDlg (self):
#        self.dlg4.move(2000, 150)
        self.dlg4.show()# show the dialog
        
    def SIAnimationDlg (self):
        self.dlg5.show()# show the dialog

    # Selecting the files in directory
    def selectFiles( self ):
        settings = QSettings()
        path = str(QFileDialog.getOpenFileNames(self.iface.mainWindow(), "Select Directory")) 
        if path: self.dlg.ui.txtBaseDir.setText( path ) #write the name of the directory path
        
   
    # Selecting the directory containg files 
    def selectDir1( self ):
        self.dlg.hide()
        settings = QSettings()
        path = QFileDialog.getExistingDirectory( self.iface.mainWindow(), "Select a directory")
        if path: self.dlg.ui.txtBaseDir2_5.setText( path )
        self.dlg.show()
        
        
    def selectDir2( self ):
        self.dlg3.hide()
        settings = QSettings()
        path = QFileDialog.getExistingDirectory( self.iface.mainWindow(), "Select a directory")
        if path: self.dlg3.ui.txtBaseDir2_5.setText( path )
        self.dlg3.show()
        
    def reloadLayers(self):
        for layer in self.iface.legendInterface().layers():
            QgsMapLayerRegistry.instance().removeMapLayer( layer.id()  )
        self.dlg2.ui.widget.canvas.ax.clear()
        
    def msgBox(self, text):
            text = "Please Confirm first"
            msgBox = QMessageBox()
            msgBox.setText(text)
            
    def desableinactivebuttons (self):
            self.dlg.ui.pushButton_5.setEnabled(False)
            self.dlg.ui.pushButton_6.setEnabled(False)
            self.dlg.ui.progressBar_2.setProperty("value",0)

############################################################################
    def Preprocessing(self):    
#        import formatting
        execfile("/home/mugwiza/workspace/MyPlugin/SpatialMetrics/preprocessing/formatting.py")
    def SMcalc(self): 
        import FilesNaming
        if self.dlg.ui.comboBox_3.currentText() == "SI NOT AVAILABLE" : 
            msgBox = QMessageBox()
            msgBox.setText("SI currently not available choose another SI")
            msgBox.exec_()            
        else: 
            classe = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText()))[0]
            Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText()))[1]
            Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText()))[2]
            for i in range(0,100+1,50):
                self.dlg.ui.progressBar_2.setProperty("value",i)
##                os.system( "python metrics2.py "+classe+"  "+Naming+"  "+Metric ) 
##                os.system("python imgshow.py "+Naming+"  "+Metric)            
                self.dlg.ui.progressBar_2.setProperty("value",i)
            self.dlg.ui.pushButton_5.setEnabled(True)
            self.dlg.ui.pushButton_6.setEnabled(True)
        
####################################################################           
    def loadES(self):
        import library
        ES = (library.ESlist ()) 
        self.dlg.ui.comboBox_2.addItems(ES)
            
    def loadSI(self):   
        import library
        ES = (library.ESlist ())
        SI = (library.SIlist ())
        self.di = {ES[0]:["SI NOT AVAILABLE" ],#SI[8], SI[15],SI[18] ], 
                         ES[1]:[ SI[1],SI[4]   ],#SI[10], SI[12],SI[16]   ], 
                         ES[2]:[ SI[4], SI[10]  ],#SI[7],SI[11],SI[14],SI[17] ], 
                         ES[3]:[ SI[0], SI[3]  ],#SI[22] ],
                         ES[4]:[ SI[2], SI[5]  ],#SI[13],SI[14],SI[22] ],
                         ES[5]:["SI NOT AVAILABLE" ], #SI[21], SI[18] ],
                         ES[6]:["SI NOT AVAILABLE" ],#SI[14] ],
                         ES[7]:[ SI[4],SI[5]  ],#SI[12],SI[13],SI[21], SI[20] ],
                         ES[8]:[SI[1]  ],#SI[23] ], 
                         ES[9]:["SI NOT AVAILABLE"], #SI[22], SI[14], SI[23] ], 
                         ES[10]:["SI NOT AVAILABLE"],#SI[15], SI[17], SI[23] ], 
                         ES[11]:["SI NOT AVAILABLE"], #SI[6], SI[7], SI[10], SI[11], SI[17] ], 
                         ES[12]:["SI NOT AVAILABLE"], #SI[9], SI[10], SI[16], SI[11] ]
                         }
        self.dlg.ui.comboBox_3.addItems (self.di[ES[0]])   
            
    def changeCombo(self, ind):
        self.dlg.ui.comboBox_3.clear()
        self.dlg.ui.comboBox_3.addItems(self.di[ind])
 
    def actionRemove(self):
        layers = self.iface.legendInterface().layers()
        for layer in layers :
            if layer.name() == self.PrincipalLayer : pass
            else : self.iface.legendInterface().moveLayer( layer, 0 )
        self.iface.legendInterface().removeGroup(0)
        
######################################################################################
    def AddLayer(self, input):        
        layerPath = os.path.join(self.dataDir, input)
        fileInfo = QFileInfo(layerPath)
        baseName = fileInfo.baseName()
        layer = QgsRasterLayer(layerPath, baseName)
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        layer.loadNamedStyle(uri)
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        
    def loadMaps(self):
        import FilesNaming
        import Styling
        if self.dlg.ui.progressBar_2.value () != 100: 
            msgBox = QMessageBox()
            msgBox.setText("Please Confirm first")
            msgBox.exec_()
            return
        else :
            self.dlg.hide()
            self.canvas.enableAntiAliasing(True)
            self.SIAnimationDlg()
            layers = self.iface.legendInterface().layers()
            for layer in layers : 
                if self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().setLayerVisible(layer, False)
            import numpy
            numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
            self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
            os.chdir(self.dataDir )
            Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
            Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
            filename = (FilesNaming.FilesNames(Naming, Metric))[1]
            canvas = qgis.utils.iface.mapCanvas()
            Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  )
            file_list = self.loadFiles(filename)            
            s = QSettings()
            oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
            s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
            self.AddLayer(str(file_list[0]))
            s.setValue( "/Projections/defaultBehaviour", oldValidation )            
            canvas = qgis.utils.iface.mapCanvas()
            canvas.zoomToFullExtent()
            canvas.refresh()
            layer = qgis.utils.iface.activeLayer()
            self.PrincipalLayer = layer.name()
            self.iface.legendInterface().setLayerExpanded(layer, True)
            
    def Anim(self):
        self.actionRemove()
        Group = self.iface.legendInterface().addGroup("group_foo")       
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)  
        legend = self.iface.legendInterface() 
        canvas = qgis.utils.iface.mapCanvas()
        for index, file  in enumerate(file_list):           
            import Styling
            Styling.eachStyle(file_list[index], self.dlg.ui.comboBox_3.currentText(), file_list, self.dataDir  )
            uri = os.path.join(self.dataDir, 'MyFile.qml')
            s = QSettings()
            oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
            s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
            self.iface.addRasterLayer(file, os.path.basename(str(file))).loadNamedStyle(uri)           
            s.setValue( "/Projections/defaultBehaviour", oldValidation )
            canvas.refresh()
            canvas.zoomToFullExtent()
            time.sleep(float(self.dlg5.ui.txtBaseDir2_5.text()))
            g = qgis.utils.iface.legendInterface().layers()
            if len(g) == 1 : pass
            else:
                Player = g[1] 
                self.iface.legendInterface().setLayerVisible(Player, False)
                legend.moveLayer( Player, 0 )

    def Next(self):
        self.actionRemove()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)
        layer = qgis.utils.iface.activeLayer()
        self.iface.legendInterface().setLayerVisible(layer, False)
        if layer is None :
            index = 0
        elif layer.name() not in file_list:
            index = 0
        else: 
            counter = file_list.index(layer.name())        
            index = counter + 1
            if counter == len(file_list) - 1 :
                layers = self.iface.legendInterface().layers()
                self.iface.legendInterface().addGroup("group_foo")
                for layer in layers : 
                    if layer.name() == self.PrincipalLayer : pass
                    elif self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().moveLayer( layer, 0 )
                index = 0
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], self.dlg.ui.comboBox_3.currentText(), file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation )        
        canvas.refresh()
        canvas.zoomToFullExtent()

    def Previous(self):        
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )        
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)
        layer = qgis.utils.iface.activeLayer()
#        self.iface.legendInterface().setLayerVisible(layer, False)
        if layer is None :
            index = len(file_list) - 1
        elif layer.name() not in file_list:
            index = len(file_list) - 1
        else: 
            counter = file_list.index(layer.name())
            index = counter - 1
            if counter == 0 :
                layers = self.iface.legendInterface().layers()
                self.iface.legendInterface().addGroup("group_foo")
                for layer in layers : 
                    if layer.name() == self.PrincipalLayer : pass
                    elif self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().moveLayer( layer, 0 )
                index = len(file_list) - 1
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], self.dlg.ui.comboBox_3.currentText(), file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')        
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation )   
        canvas.zoomToFullExtent()
        canvas.refresh()

    def Last(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)
        layer = qgis.utils.iface.activeLayer()
        self.iface.legendInterface().setLayerVisible(layer, False)
        index = len(file_list) - 1
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], self.dlg.ui.comboBox_3.currentText(), file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation )    
        canvas.zoomToFullExtent()
        canvas.refresh()

    def First(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )        
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)
        layer = qgis.utils.iface.activeLayer()
        self.iface.legendInterface().setLayerVisible(layer, False)
        index = 0
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], self.dlg.ui.comboBox_3.currentText(), file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation )   
        canvas.zoomToFullExtent()
        canvas.refresh()
        
######################################################################################
    def graphs(self):# wtih matplotlib
        import FilesNaming
        if self.dlg.ui.progressBar_2.value () != 100: 
            msgBox = QMessageBox()
            msgBox.setText("Please Confirm first")
            msgBox.exec_()
            return
        else :
            self.view()
            self.dlg.hide()
            self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
            os.chdir(self.dataDir )
            stripped = []
            Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
            Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
            filename = (FilesNaming.FilesNames(Naming, Metric))[2]
            Title = self.dlg.ui.comboBox_3.currentText()
            stripper =  open(filename, 'r')
            st_lines = stripper.readlines()[4:]
            stripper.close()
            for lines in st_lines:
                stripped_line = " ".join(lines.split())
                stripped.append(stripped_line)
            data = "\n".join(stripped)
            data = data.split('\n')
            values = []
            dates = []
            years = 2005
            yl = []
            for row in data:
                x, y = row.split()
                values.append(float(y))
                year = (int(x.translate(string.maketrans("\n\t\r", "   ")).strip()))
                dates.append(year)
                years = years +1
                yl.append(years)
            xlabels = yl
            self.dlg2.ui.widget.canvas.ax.clear()
            self.dlg2.ui.widget.canvas.ax.set_title(Title) 
            self.dlg2.ui.widget.canvas.ax.set_xlabel ('Years')
            self.dlg2.ui.widget.canvas.ax.set_ylabel ('Area in ha')
            self.dlg2.ui.widget.canvas.ax.bar(dates, values, align='center')
            self.dlg2.ui.widget.canvas.ax.set_xticks(dates)  # put the tick markers under your bars
            self.dlg2.ui.widget.canvas.ax.set_xticklabels(xlabels, rotation=45)    # set the labels to be your formatted years
            self.dlg2.ui.widget.canvas.draw()
            self.Description()

    def DescriptionText (self, period, condition, Status, quality, process):      
            print  'period', period
            Text = ''' During '''+str(period)+''', the '''+condition+''' of the  '''+self.dlg.ui.comboBox_3.currentText()+ \
            '''  reflects the  '''+Status+''' of '''+self.dlg.ui.comboBox_2.currentText()+'''.'''''' \
            This is due (to/of) '''+quality+'''  '''+process+'''.'''''
            return Text
        
    def Description(self):
        import SIanalysis 
        import FilesNaming
        import ESprocess
        if self.dlg.ui.comboBox_3.currentText() == "SI NOT AVAILABLE" : 
            msgBox = QMessageBox()
            msgBox.setText("SI currently not available choose another SI")
            msgBox.exec_()            
        else: 
            Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
            Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
            filename = (FilesNaming.FilesNames(Naming, Metric))[1]
            file_list = self.loadFiles(filename)            
            increase = (SIanalysis.myfunc(file_list))[0]
            decrease = (SIanalysis.myfunc(file_list))[1]
            stable = (SIanalysis.myfunc(file_list))[2]            
            A = ESprocess.selectprocess(self.dlg.ui.comboBox_3.currentText(), self.dlg.ui.comboBox_2.currentText())[0]
            B = ESprocess.selectprocess(self.dlg.ui.comboBox_3.currentText(), self.dlg.ui.comboBox_2.currentText())[1]
            process = ESprocess.selectprocess(self.dlg.ui.comboBox_3.currentText(), self.dlg.ui.comboBox_2.currentText())[2]                    
            self.dlg2.ui.textEdit.setFontWeight(63)
            self.dlg2.ui.textEdit.setFontItalic(True)
            self.dlg2.ui.textEdit.clear()
            if len(increase)!= 0: 
                condition = 'increase'
                if (self.dlg.ui.comboBox_3.currentText() in A)==True : Status = 'improvement'
                if (self.dlg.ui.comboBox_3.currentText() in B)==True : Status = 'degradation'
                if Status == 'improvement' : quality = 'more'
                else: quality = 'less'
                self.dlg2.ui.textEdit.append (self.DescriptionText(increase, condition, Status, quality, process))
                self.dlg2.ui.textEdit.append( ' ')
            if len(decrease)!= 0:
                condition = 'decrease'
                if (self.dlg.ui.comboBox_3.currentText() in A)==True : Status = 'degradation'
                if (self.dlg.ui.comboBox_3.currentText() in B)==True : Status = 'improvement' 
                if Status == 'improvement' : quality = 'more'
                else: quality = 'less'            
                self.dlg2.ui.textEdit.append (self.DescriptionText(decrease, condition, Status, quality, process))
                self.dlg2.ui.textEdit.append( ' ')                
            if len(stable)!= 0:
                condition = 'no change'
                Status = 'stability'
                if Status == 'improvement' : quality = 'more'
                else: quality = 'less'
                self.dlg2.ui.textEdit.append (self.DescriptionText(stable, condition, Status, quality, process))
                self.dlg2.ui.textEdit.append( ' ')
        
###################################################################################
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def loadFiles(self, filename):
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        file_list =  glob.glob(filename)
        for index in file_list:
            list = index.split(".")
            if (len(list)!= 2) :
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".tiff"):
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".xml") or index.endswith(".aux.xml") :
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".tss"):
                file_list.remove(index)
        file_list.sort()
        return file_list
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def loadMapStackCoreName(self):
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        files= os.listdir(self.dataDir)
        self.dlg3.ui.comboBox.clear()
        self.dlg3.ui.comboBox_2.clear()
        MyList=[]
        MyList2 =[]
        MyList3 = []
        for index in files:
            list = index.split(".")
            if (len(list)==2) and (len(list[0])== 8) and (len(list[1])== 3) and (list[1].isdigit()):
                MyList.append(index)
            if index.endswith(".tss"):
                MyList3.append(index)
        for index in MyList:
            list = index.split(".")
            words = list[0].replace("0", "")
            MyList2.append(words)
        FinalList = []
        for i in MyList2:
            if i not in FinalList:
                FinalList.append(i)
        self.dlg3.ui.comboBox.addItems(FinalList)
        self.dlg3.ui.comboBox_2.addItems(MyList3)

    def DisplayTSSnames(self):
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        filename = '*'+str(self.dlg3.ui.comboBox.currentText())+'*'
        file_list =  glob.glob(filename)
        for index in file_list:
            list = index.split(".")
            if (len(list)!= 2) :
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".tiff"):
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".xml") or index.endswith(".aux.xml") :
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".tss"):
                file_list.remove(index)
        file_list.sort()
        self.dlg3.ui.listWidget.clear()
        for index, file in enumerate(file_list):
            self.dlg3.ui.listWidget.addItem(file)
            
    def ActionAnim(self):# wtih matplotlib
        self.actionRemove()
        Group = self.iface.legendInterface().addGroup("group_foo")       
        import numpy
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        filename = '*'+str(self.dlg3.ui.comboBox.currentText())+'*'
        file_list = self.loadFiles(filename)       
        legend = self.iface.legendInterface() 
        for index, file in enumerate(file_list):
            canvas = qgis.utils.iface.mapCanvas()
            import Styling
            Styling.eachStyle(file_list[index], 'value', file_list, self.dataDir  )
            uri = os.path.join(self.dataDir, 'MyFile.qml')
            
            s = QSettings()
            oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
            s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
            self.iface.addRasterLayer(file, os.path.basename(str(file))).loadNamedStyle(uri)
            s.setValue( "/Projections/defaultBehaviour", oldValidation ) 
            
            canvas.refresh()
            canvas.zoomToFullExtent()   
            rlayer = qgis.utils.iface.activeLayer()
            legend.moveLayer( rlayer, 0 )
            time.sleep(float(self.dlg4.ui.txtBaseDir2_5.text()))

    def actionStart(self):
        self.actionRemove()
        self.dlg3.hide()
        self.AnimationDlg()
        import Styling
        layers = self.iface.legendInterface().layers()
        for layer in layers : 
            if self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().setLayerVisible(layer, False)
        import numpy
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        filename = '*'+str(self.dlg3.ui.comboBox.currentText())+'*'
        file_list = self.loadFiles(filename)
        Styling.style(filename, 'value', self.dataDir )
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.AddLayer(str(file_list[0]))
#        self.iface.addRasterLayer(file_list[0], os.path.basename(str(file_list[0]))).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) ) 
        s.setValue( "/Projections/defaultBehaviour", oldValidation ) 
        canvas = qgis.utils.iface.mapCanvas()
        canvas.zoomToFullExtent()
        canvas.refresh()
        layer = qgis.utils.iface.activeLayer()
        self.PrincipalLayer = layer.name()
        self.iface.legendInterface().setLayerExpanded(layer, True)
        
    def actionLast(self):
        self.dlg3.hide()
        self.AnimationDlg()
        self.iface.messageBar().clearWidgets ()
        layers = self.iface.legendInterface().layers()
        for layer in layers : 
            if self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().setLayerVisible(layer, False)
        import numpy
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        filename = '*'+str(self.dlg3.ui.comboBox.currentText())+'*'
        file_list = self.loadFiles(filename)
        index = len(file_list) - 1
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], 'value', file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation ) 
        canvas.refresh()
        canvas.zoomToFullExtent()

    def actionNext(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        filename = '*'+str(self.dlg3.ui.comboBox.currentText())+'*'
        file_list = self.loadFiles(filename)
        layer = qgis.utils.iface.activeLayer()
        if layer is None :
            index = 0
        elif layer.name() not in file_list:
            index = 0
        else :
            counter = file_list.index(layer.name())
            index = counter + 1
            if counter == len(file_list) - 1 :
                layers = self.iface.legendInterface().layers()
                self.iface.legendInterface().addGroup("group_foo")
                for layer in layers : 
                    if layer.name() == self.PrincipalLayer : pass
                    elif self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().moveLayer( layer, 0 )
                index = 0
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], 'value', file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation ) 
        canvas.refresh()
        canvas.zoomToFullExtent()  
         
    def actionPrevious(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        filename = '*'+str(self.dlg3.ui.comboBox.currentText())+'*'
        file_list = self.loadFiles(filename)
        layer = qgis.utils.iface.activeLayer()
        if layer is None :
            index = len(file_list) - 1
        elif layer.name() not in file_list:
            index = len(file_list) - 1
        else :
            counter = file_list.index(layer.name())
            index = counter - 1
            if counter == 0 :
                layers = self.iface.legendInterface().layers()
                self.iface.legendInterface().addGroup("group_foo")
                for layer in layers : 
                    if layer.name() == self.PrincipalLayer : pass
                    elif self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().moveLayer( layer, 0 )
                index = len(file_list) - 1
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        Styling.eachStyle(file_list[index], 'value', file_list, self.dataDir  )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        s = QSettings()
        oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
        s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        s.setValue( "/Projections/defaultBehaviour", oldValidation ) 
        canvas = qgis.utils.iface.mapCanvas()
        canvas.zoomToFullExtent()
        canvas.refresh()

    def TSSgraphs(self):# wtih matplotlib
        self.dlg3.hide()
        self.TSSview()
        self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        stripped = []
        filename = str(self.dlg3.ui.comboBox_2.currentText())   
        stripper =  open(filename, 'r')
        st_lines = stripper.readlines()[4:]
        stripper.close()
        for lines in st_lines:
            stripped_line = " ".join(lines.split())
            stripped.append(stripped_line)
        data = "\n".join(stripped)
        data = data.split('\n')
        values = []
        dates = []
        years = 2004
        yl = []
        for row in data:
            x, y = row.split()
            values.append(float(y))
            year = (int(x.translate(string.maketrans("\n\t\r", "   ")).strip()))
            dates.append(year)
            years = years +1
            yl.append(years)
        xlabels = yl
        self.dlg6.ui.widget.canvas.ax.clear()
        self.dlg6.ui.widget.canvas.ax.set_title(filename) 
        self.dlg6.ui.widget.canvas.ax.set_xlabel ('Years')
        self.dlg6.ui.widget.canvas.ax.set_ylabel ('Area in ha')
        self.dlg6.ui.widget.canvas.ax.bar(dates, values, align='center')
        self.dlg6.ui.widget.canvas.ax.set_xticks(dates)  # put the tick markers under your bars
        self.dlg6.ui.widget.canvas.ax.set_xticklabels(xlabels)    # set the labels to be your formatted years
        self.dlg6.ui.widget.canvas.draw()
