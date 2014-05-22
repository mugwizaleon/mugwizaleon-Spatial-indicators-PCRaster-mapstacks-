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
        QObject.connect( self.dlg.ui.btnBaseDir_3, SIGNAL( "clicked()" ), self.selectDir ) #link the button to the function of selecting the directory
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
        QObject.connect( self.dlg3.ui.btnBaseDir_3, SIGNAL( "clicked()" ), self.selectDir ) #link the button to the function of selecting the directory
        QObject.connect( self.dlg3.ui.btnBaseDir_3, SIGNAL( "clicked()" ), self.loadMapStackCoreName ) #link the button to the function of selecting the directory
        QObject.connect( self.dlg3.ui.pushButton_5, SIGNAL( "clicked()" ), self.actionStart)
        QObject.connect( self.dlg4.ui.pushButton_2, SIGNAL( "clicked()" ), self.ActionAnim)
        QObject.connect( self.dlg4.ui.pushButton_3, SIGNAL( "clicked()" ), self.actionNext)
        QObject.connect( self.dlg4.ui.pushButton, SIGNAL( "clicked()" ), self.actionPrevious)
        
        QObject.connect( self.dlg4.ui.pushButton_4, SIGNAL( "clicked()" ), self.actionStart)
        QObject.connect( self.dlg4.ui.pushButton_5, SIGNAL( "clicked()" ), self.actionLast)
        QObject.connect(self.dlg3.ui.comboBox, SIGNAL("currentIndexChanged (const QString&)"), self.changelist) #Change the list of mapstacks
        
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction( QIcon(":/plugins/spatialmetrics/icon2.png"), u"Spatial Indicator", self.iface.mainWindow())
        self.action2 = QAction( QIcon(":/plugins/spatialmetrics/icon1.png"), u"PCRaster Time series Viewer", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        self.action2.triggered.connect(self.TSS)
        # Add toolbar button and menu item
        self.iface.addPluginToRasterMenu(u"&spatial planning tool ", self.action)
        self.iface.addPluginToRasterMenu(u"&spatial planning tool ", self.action2)
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
        self.dlg.move(0, 100)
        result = self.dlg.exec_() # Run the dialog event loop
        
    def view(self):
        self.dlg2.move(10, 300)
        self.dlg2.show()# show the dialog
        
    def TSSview(self):
        self.dlg6.move(10, 300)
        self.dlg6.show()# show the dialog        

    def TSS (self):
        self.dlg3.show()# show the dialog
        self.dlg3.move(0, 100)       
        
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
    def selectDir( self ):
        settings = QSettings()
        path = QFileDialog.getExistingDirectory( self.iface.mainWindow(), "Select a directory")
        if path: self.dlg.ui.txtBaseDir2_5.setText( path )
        if path: self.dlg3.ui.txtBaseDir2_5.setText( path )
        
        
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
#                execfile("/home/mugwiza/workspace/MyPlugin/SpatialMetrics/preprocessing/metrics2.py")
#                os.system( "python calculatemetrics.py "+classe+"  "+Naming+"  "+Metric ) 
#                os.system("python imgshow.py "+Naming+"  "+Metric)            
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
        self.di = {ES[0]:[SI[0] ],
                         ES[1]:[ SI[1],SI[2], SI[3]    ],
                         ES[2]:[ SI[4] ],
                         ES[3]:[ SI[2], SI[5], SI[6], SI[3], SI[7]],
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
######################################################################################
    def ReadValues(self, filename):
        import FilesNaming
        import SIanalysis 
        import library
        SI = (library.SIlist ())
        stripped = []
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
        dates.sort()
        return (values, dates, xlabels)
        
    def autolabel(self, bars):
        for bar in bars:
            h = bar.get_height()
            self.dlg2.ui.widget.canvas.ax.text(bar.get_x()+bar.get_width()/2., 1.05*h, '%.1f'%float(h), ha='center', va='bottom', fontsize=6)
        
    def graphs(self):# wtih matplotlib
        import FilesNaming
        import SIanalysis 
        import library
        self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
        os.chdir(self.dataDir )
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename1 = (FilesNaming.FilesNames(Naming, Metric))[2]
        filename2 = (FilesNaming.FilesNames(Naming, Metric))[3]
        SI = (library.SIlist ())
        if self.dlg.ui.progressBar_2.value () != 100: 
            msgBox = QMessageBox()
            msgBox.setText("Please Confirm first")
            msgBox.exec_()
            return
        else :
            if os.path.isfile(filename1):
                self.view()
                self.dlg.hide()
                values = self.ReadValues(filename1)[0]
                dates = self.ReadValues(filename1)[1]
                xlabels = self.ReadValues(filename1)[2] 
                try:
                    values2 = self.ReadValues(filename2)[0]
                except IOError :
                    pass
                TargetValue = (SIanalysis.TargetValues(self.dlg.ui.comboBox_3.currentText()))
                self.dlg2.ui.widget.canvas.ax.clear()
                self.dlg2.ui.widget.canvas.ax.set_xlim(left= dates[0]) #the left maximum horizontal axis
                self.dlg2.ui.widget.canvas.ax.set_xlim(right= dates[len(dates) - 1]) # the right maximum horizontal axis
                self.dlg2.ui.widget.canvas.ax.set_title((FilesNaming.GraphLabel (self.dlg.ui.comboBox_3.currentText() ))[0]) 
                self.dlg2.ui.widget.canvas.ax.set_xlabel ((FilesNaming.GraphLabel (self.dlg.ui.comboBox_3.currentText() ))[1])
                self.dlg2.ui.widget.canvas.ax.set_ylabel ((FilesNaming.GraphLabel (self.dlg.ui.comboBox_3.currentText() ))[2])
                self.dlg2.ui.widget.canvas.ax.yaxis.set_label_position("right")            
                HorValue = self.dlg2.ui.widget.canvas.ax.get_xlim()          
                self.dlg2.ui.widget.canvas.ax.set_xticklabels(xlabels, rotation=30, fontsize=10)    # set the labels to be your formatted years
                width = 0.4
                if self.dlg.ui.comboBox_3.currentText() in [SI[4], SI[2], SI[5]] :
                    LimValue = (values[0], TargetValue )
                    bar1 = self.dlg2.ui.widget.canvas.ax.bar(dates, values, width, color='g')
                    bar2 = self.dlg2.ui.widget.canvas.ax.bar([date + width for date in dates], values2, width, color='r')
                    self.dlg2.ui.widget.canvas.ax.set_xticks([date + width for date in dates])  # put the tick markers under your bars
                    self.dlg2.ui.widget.canvas.ax.set_ylim([0, 110])
                    self.dlg2.ui.widget.canvas.ax.set_xticklabels( ('2006', '2007', '2008', '2009', '20010', '20011', '20012', '2013', '2014', '2015', '2016', '2017', '2018') )  
                    legend = self.dlg2.ui.widget.canvas.ax.legend ((bar1[0], bar2[0]), ((FilesNaming.GraphLabel (self.dlg.ui.comboBox_3.currentText() ))[3], (FilesNaming.GraphLabel (self.dlg.ui.comboBox_3.currentText() ))[4] ), loc='center right')
                    for label in legend.get_texts():
                        label.set_fontsize('small')
                    self.autolabel(bar1)
                    self.autolabel(bar2)
                else:
                    LimValue = (values[0], TargetValue )
                    self.dlg2.ui.widget.canvas.ax.plot(dates, values)
                    self.dlg2.ui.widget.canvas.ax.plot(HorValue, LimValue,linestyle='--', color='r' ) #Trend of desired state
                    self.dlg2.ui.widget.canvas.ax.set_xticks(dates)
                self.dlg2.ui.widget.canvas.draw()
                self.Description()
            else: QMessageBox.information( self.iface.mainWindow(),"Info", "The are no calculated SM in this directory")

    def DescriptionText (self, spatialIndicator, ecosService):      
            Text = (" The "+spatialIndicator+" indicates the trend of "+ecosService+ "."
            "On the maps, the color representing the "+spatialIndicator+" varies as the the value of spatial indicator changes dynamicaly in time."
            "On the graph, the desired state of "+ecosService+" in 2030 is achieved when the value of spatial indicator is above the red dotted line")
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
            self.dlg2.ui.textEdit.setFontWeight(63)
            self.dlg2.ui.textEdit.setFontItalic(True)
            self.dlg2.ui.textEdit.clear()
            self.dlg2.ui.textEdit.append (self.DescriptionText(self.dlg.ui.comboBox_3.currentText(), self.dlg.ui.comboBox_2.currentText()))
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
            if index.endswith(".tss"):
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".xml") or index.endswith(".aux.xml") :
                file_list.remove(index)
        for index in file_list:
            if index.endswith(".tss"):
                file_list.remove(index)
        file_list.sort()
        return file_list
        
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
        import library
        if self.dlg.ui.progressBar_2.value () != 100: 
            msgBox = QMessageBox()
            msgBox.setText("Please Confirm first")
            msgBox.exec_()
            return
        else :
            self.dlg.hide()
            self.canvas.enableAntiAliasing(True)
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
            file_list = self.loadFiles(filename)
            if len(file_list) == 0:
                QMessageBox.information( self.iface.mainWindow(),"Info", "The are no calculated SM in this directory")
                return
            else: 
                self.SIAnimationDlg()
                SI = (library.SIlist ())
                if self.dlg.ui.comboBox_3.currentText() == SI[2] : 
                    Styling.ClusterSize(file_list[0], "size" , file_list, self.dataDir )
                if self.dlg.ui.comboBox_3.currentText() == SI[4] :
                    Styling.Mydistance (file_list[0], "Distance" , file_list, self.dataDir )
                if self.dlg.ui.comboBox_3.currentText() == SI[5] :
                    Styling.MeanClusterSize (file_list[0], "mps" , file_list, self.dataDir )
                if self.dlg.ui.comboBox_3.currentText() == SI[7] :
                    Styling.Wetness(file_list[0], "wwi" , file_list, self.dataDir )
                if self.dlg.ui.comboBox_3.currentText() in [SI[0], SI[1], SI[3], SI[6]]:
                    Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  ) 
                s = QSettings()
                oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
                s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
                self.AddLayer(str(file_list[0]))
                s.setValue( "/Projections/defaultBehaviour", oldValidation )
                layer = qgis.utils.iface.activeLayer()
                self.PrincipalLayer = layer.name()
                self.iface.legendInterface().setLayerExpanded(layer, True)
        

    def Anim(self):
        self.actionRemove()
        Group = self.iface.legendInterface().addGroup("group_foo")       
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)   
        legend = self.iface.legendInterface() 
        canvas = qgis.utils.iface.mapCanvas()
        for index, file in enumerate(file_list):  
            canvas = qgis.utils.iface.mapCanvas()  
            import Styling
            import library
            SI = (library.SIlist ())
            if self.dlg.ui.comboBox_3.currentText() == SI[2] : 
                Styling.ClusterSize(file_list[0], "size" , file_list, self.dataDir )
            if self.dlg.ui.comboBox_3.currentText() == SI[4] :
                Styling.Mydistance (file_list[0], "Distance" , file_list, self.dataDir )
            if self.dlg.ui.comboBox_3.currentText() == SI[5] :
                Styling.MeanClusterSize (file_list[0], "mps" , file_list, self.dataDir )
            if self.dlg.ui.comboBox_3.currentText() == SI[7] :
                Styling.Wetness(file_list[0], "wwi" , file_list, self.dataDir )
            if self.dlg.ui.comboBox_3.currentText() in [SI[0], SI[1], SI[3], SI[6]]:
                Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  ) 
            uri = os.path.join(self.dataDir, 'MyFile.qml')
            self.iface.addRasterLayer(file, os.path.basename(str(file))).loadNamedStyle(uri)
            canvas.refresh()
            canvas.zoomToFullExtent()
        
            rlayer = qgis.utils.iface.activeLayer()
            legend.moveLayer( rlayer, 0 )
            time.sleep(float(self.dlg5.ui.txtBaseDir2_5.text()))
            
    def Next(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
#        filename = '*LSDensit*'
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
        import library
        file_list = self.loadFiles(filename)
        SI = (library.SIlist ())
        if self.dlg.ui.comboBox_3.currentText() == SI[2] : 
            Styling.ClusterSize(file_list[0], "size" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[4] :
            Styling.Mydistance (file_list[0], "Distance" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[5] :
            Styling.MeanClusterSize (file_list[0], "mps" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[7] :
            Styling.Wetness(file_list[0], "wwi" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() in [SI[0], SI[1], SI[3], SI[6]]:
            Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  ) 
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        canvas.refresh()
        canvas.zoomToFullExtent()
        
    def Previous(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
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
        import library
        SI = (library.SIlist ())
        if self.dlg.ui.comboBox_3.currentText() == SI[2] : 
            Styling.ClusterSize(file_list[0], "size" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[4] :
            Styling.Mydistance (file_list[0], "Distance" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[5] :
            Styling.MeanClusterSize (file_list[0], "mps" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[7] :
            Styling.Wetness(file_list[0], "wwi" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() in [SI[0], SI[1], SI[3], SI[6]]:
            Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  ) 
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        canvas.refresh()
        canvas.zoomToFullExtent()
        
    def Last(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)
        index = len(file_list) - 1
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        import library
        SI = (library.SIlist ())
        if self.dlg.ui.comboBox_3.currentText() == SI[2] : 
            Styling.ClusterSize(file_list[0], "size" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[4] :
            Styling.Mydistance (file_list[0], "Distance" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[5] :
            Styling.MeanClusterSize (file_list[0], "mps" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[7] :
            Styling.Wetness(file_list[0], "wwi" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() in [SI[0], SI[1], SI[3], SI[6]]:
            Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  ) 
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        canvas.refresh()
        canvas.zoomToFullExtent()
        
    def First(self):
        self.actionRemove()
        self.iface.messageBar().clearWidgets ()
        import numpy
        import FilesNaming
        numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
        Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
        Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
        filename = (FilesNaming.FilesNames(Naming, Metric))[1]
        file_list = self.loadFiles(filename)
        index = 0
        canvas = qgis.utils.iface.mapCanvas()  
        import Styling
        import library
        SI = (library.SIlist ())
        if self.dlg.ui.comboBox_3.currentText() == SI[2] : 
            Styling.ClusterSize(file_list[0], "size" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[4] :
            Styling.Mydistance (file_list[0], "Distance" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[5] :
            Styling.MeanClusterSize (file_list[0], "mps" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() == SI[7] :
            Styling.Wetness(file_list[0], "wwi" , file_list, self.dataDir )
        if self.dlg.ui.comboBox_3.currentText() in [SI[0], SI[1], SI[3], SI[6]]:
            Styling.style(filename, self.dlg.ui.comboBox_3.currentText(),self.dataDir  ) 
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        canvas.refresh()
        canvas.zoomToFullExtent()

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
        file_list = self.loadFiles(filename) 
        self.dlg3.ui.listWidget.clear()
        for index, file in enumerate(file_list):
            self.dlg3.ui.listWidget.addItem(file)
    def changelist(self):
        self.dlg3.ui.listWidget.clear()
            
    def ActionAnim(self):
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
            Styling.style1(file_list[index], 'value', self.dataDir, file_list )
            uri = os.path.join(self.dataDir, 'MyFile.qml')
            self.iface.addRasterLayer(file, os.path.basename(str(file))).loadNamedStyle(uri)
            canvas.refresh()
            canvas.zoomToFullExtent()   
            rlayer = qgis.utils.iface.activeLayer()
            legend.moveLayer( rlayer, 0 )
            time.sleep(float(self.dlg4.ui.txtBaseDir2_5.text()))


    def actionStart(self):
        self.actionRemove()
        import Styling
        self.actionRemove()
        self.dlg3.hide()        
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
        if not self.dlg3.ui.comboBox.currentText():
            QMessageBox.information( self.iface.mainWindow(),"Info", "The are no PCRaster mapstacksin this directory")
            return
        else:
            self.AnimationDlg()
            Styling.style1(filename, 'value', self.dataDir, file_list )
            s = QSettings()
            oldValidation = s.value( "/Projections/defaultBehaviour", "useGlobal" )
            s.setValue( "/Projections/defaultBehaviour", "useGlobal" )
            self.AddLayer(str(file_list[0]))
            s.setValue( "/Projections/defaultBehaviour", oldValidation )
            layer = qgis.utils.iface.activeLayer()
            self.PrincipalLayer = layer.name()
            self.iface.legendInterface().setLayerExpanded(layer, True)
        
    def actionLast(self):
        self.actionRemove()
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
        Styling.style1(file_list[index], 'value', self.dataDir, file_list )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
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
        Styling.style1(file_list[index], 'value', self.dataDir, file_list )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
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
        Styling.style1(file_list[index], 'value', self.dataDir, file_list )
        uri = os.path.join(self.dataDir, 'MyFile.qml')
        self.iface.addRasterLayer(file_list[index], os.path.basename(str(file_list[index]))).loadNamedStyle(uri)
        canvas.refresh()
        canvas.zoomToFullExtent() 

    def TSSgraphs(self):# wtih matplotlib
        self.dlg3.hide()
        filename = str(self.dlg3.ui.comboBox_2.currentText())   
        if os.path.isfile(filename):
            self.TSSview()
            self.dataDir = str(self.dlg3.ui.txtBaseDir2_5.text())
            os.chdir(self.dataDir )
            stripped = []
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
        else: QMessageBox.information( self.iface.mainWindow(),"Info", "The are no PCRaster timeseries this directory")        
