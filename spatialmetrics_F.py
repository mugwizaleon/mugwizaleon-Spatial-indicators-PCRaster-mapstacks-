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
import resources_rc
# Import the code for the dialog
from spatialmetricsdialog import SpatialMetricsDialog
import os.path
from LoadRasters import *
from Filter import *



class SpatialMetrics:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'spatialmetrics_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
        
        # Create the dialog (after translation) and keep reference
        self.dlg = SpatialMetricsDialog()
        
        #Initial  variables for opening files
        QObject.connect( self.dlg.ui.btnBaseDir, SIGNAL( "clicked()" ), self.selectDir ) #link the button to the function of selecting the directory
        self.loadFormats()
        self.buttonOk = self.dlg.ui.buttonBox.button( QDialogButtonBox.Ok )
        self.dlg.ui.progressBar.setMinimum( 0 )
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/spatialmetrics/icon.png"),
            u"Spatial Metrics", self.iface.mainWindow())
            
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&SM", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&SM", self.action)
        self.iface.removeToolBarIcon(self.action)
        
  # Selecting the directory containg files
    def selectDir( self ):
        settings = QSettings()
        path = str(QFileDialog.getExistingDirectory(self.iface.mainWindow(), "Select Directory")) 
        if path: self.dlg.ui.txtBaseDir.setText( path ) #write the name of the directory path
        
        
    def loadFormats(self): 
        self.dlg.ui.cboFormats.addItem( "PCRaster Raster File (*.map)")#, QVariant( [".map"] ) )
        
##    def getFilesToLoad( self, baseDir ):
##        """ Go through directories to fill a list with layers ready to be loaded """
##    dlg = SpatialMetricsDialog()
##    dlg.ui.progressBar.setMaximum( 0 ) # ProgressBar in busy mode
##    lstFilesToLoad = []
##    layerPaths = []
##    baseDir = os.getcwd()
##    for root, dirs, files in os.walk(baseDir.decode("utf-8") ):
##        for file in files: 
##          QApplication.processEvents() # ProgressBar in busy mode
###          if self.progressBar.parent().processStatus == False: return #The process was canceled
##          
##          extension = str.lower( str( os.path.splitext( file )[ 1 ] ) )
##          if extension in extension:
##            layerPath = os.path.join( root, file )
##            if extension == ".gpx":
##              layerPaths.extend([layerPath + "?type=" + t for t in ["track","route","waypoint"]])
##            else:
##              layerPaths.append( layerPath )
##    
##    for path in layerPaths:        
##        lstFilesToLoad.append( path )
##    dlg.ui.progressBar.setMaximum( len(lstFilesToLoad ) ) 
    
##def addGroup
##    dicGroups = {} # layerDir : index
##    if path not in self.dicGroups: 
##        name = os.path.split( path )[ 1 ] # Get the last dir in the path
##        index = self.toc.addGroup( name )
##        self.dicGroups[ path ] = index
##        
##def addLayer( self, layerPath, layerBaseName ):
##""" Add a raster layer """
##    layerBaseName = os.path.splitext( os.path.basename( layerPath ) )[0]
##return self.iface.addRasterLayer( layerPath, layerBaseName )
##    
##def orderLayer
##    toc = iface.legendInterface()
##    layerDir = os.path.dirname( layerPath )
##    self.toc.moveLayer( mapLayer,  self.getGroupIndex( layerDir ) )
##
##def loadLayers( self ):
##    """ Load the layer to the map """
##    ml = addLayer( layerPath, os.path.splitext( os.path.basename( layerPath ) )[ 0 ] )
##    
##    
##    
##    for layerPath in self.lstFilesToLoad:      
##      # Finally add the layer and apply the options the user chose
##      if self.bGroups: self.groups.addGroup( os.path.dirname( layerPath ) )
##      ml = self.addLayer( layerPath, os.path.splitext( os.path.basename( layerPath ) )[ 0 ] )
##      if self.bLayersOff: self.iface.legendInterface().setLayerVisible( ml, False )
##      if self.bGroups: self.groups.orderLayer( ml, layerPath )
##    
##      step += 1
##      self.progressBar.setValue( step )
##    self.iface.mapCanvas().setRenderFlag( True ) # Finish the loading process 
##    
##    if self.bIsDoneDialog:
##        QMessageBox.information( self.iface.mainWindow(), "Load Them All", 
##          QCoreApplication.translate( "Load Them All", "There have been " ) + 
##          QCoreApplication.translate( "Load Them All", "loaded " ) + str( numLayers ) + 
##          QCoreApplication.translate( "Load Them All", " layers succesfully." ), QMessageBox.Ok )
##    return
##    
##    self.progressBar.reset() 
##    self.progressBar.setMaximum( 100 )
##    self.progressBar.setValue( 0 )
##    
##    if numLayers == 0:   
##        if len(self.extension) == 1: 
##            msgExtensions = str(self.extension[0])[1:]
##    else:
##        msgExtensions = ", ".join(str(x)[1:] for x in self.extension[:-1]) + \
##        QCoreApplication.translate( "Load Them All", " or " ) + \
##        str(self.extension[len(self.extension)-1])[1:]
##        QMessageBox.information( self.iface.mainWindow(), "Load Them All", 
##        QCoreApplication.translate( "Load Them All", "There are no <i>" ) + msgExtensions + 
##        QCoreApplication.translate( "Load Them All", "</i> files to load from the base directory with this filter.\n") +
##        QCoreApplication.translate( "Load Them All", "Change those parameters and try again." ), 
##        QMessageBox.Ok )
    
    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            self.dataDir = str(self.dlg.ui.txtBaseDir.text()) #selecting the directory 
            LoadFiles(self.iface)
            
class LoadFiles():
#          """ Abstract Class to inherit two common methods to Vector and Raster Load classes """
    def __init__( self, iface):#, baseDir, extension, iface, progressBar, bGroups, bLayersOff, bDoNotEmpty, bIsDoneDialog, numLayersToConfirm ):
        self.dlg = SpatialMetricsDialog()
        self.baseDir = os.path.dirname(os.path.realpath(__file__))
        self.progressBar = self.dlg.ui.progressBar
        self.filter = Filter()
        self.iface = iface
        self.lstFilesToLoad = []
        
        # Configuration parameters
        self.bGroups = Group( self.iface )
        if self.bGroups: self.groups = Group( self.iface )
#        self.bLayersOff = bLayersOff
#        self.bDoNotEmpty = bDoNotEmpty
#        self.bIsDoneDialog = bIsDoneDialog
#        self.numLayersToConfirm = numLayersToConfirm
        
    def applyFilter( self, layerBaseName ):
#            """ Method to encapsulate the filter's application  """
        return self.filter.apply( layerBaseName )

    def getFilesToLoad( self ):
#            """ Go through directories to fill a list with layers ready to be loaded """
        self.progressBar.setMaximum( 0 ) # ProgressBar in busy mode
        layerPaths = []

        for root, dirs, files in os.walk( self.baseDir.decode("utf-8") ):
            for file in files: 
              QApplication.processEvents() # ProgressBar in busy mode
              if self.progressBar.parent().processStatus == False: return #The process was canceled
              
              extension = str.lower( str( os.path.splitext( file )[ 1 ] ) )
              if extension in self.extension:
                layerPath = os.path.join( root, file )
    
                if extension == ".gpx":
                  layerPaths.extend([layerPath + "?type=" + t for t in ["track","route","waypoint"]])
                else:
                  layerPaths.append( layerPath )
    
        for path in layerPaths:
          if self.applyFilter( path ): # The layer pass the filter?
            if self.bDoNotEmpty: # Do not load empty layers
              if not self.isEmptyLayer( path ): self.lstFilesToLoad.append( path )
            else:
              self.lstFilesToLoad.append( path )
    
        self.progressBar.setMaximum( len( self.lstFilesToLoad ) )    

    def loadLayers( self ):
#        """ Load the layer to the map """
        if self.progressBar.parent().processStatus == False: return #The process was canceled
        numLayers = len( self.lstFilesToLoad )
    
        if numLayers > 0: 
          result = QMessageBox.Ok # Convenient variable to pass an upcoming condition
    
          if numLayers >= self.numLayersToConfirm:
            result = QMessageBox.question( self.iface.mainWindow(), 
                QCoreApplication.translate( "Load Them All", "Load Them All" ),
                QCoreApplication.translate( "Load Them All", "There are " ) + str( numLayers ) + 
                QCoreApplication.translate( "Load Them All", " layers to load.\n Do you want to continue?" ), 
                QMessageBox.Ok | QMessageBox.Cancel , QMessageBox.Ok )
    
          if result == QMessageBox.Ok:
            self.iface.mapCanvas().setRenderFlag( False ) # Start the loading process 
            step = 0
    
            for layerPath in self.lstFilesToLoad:      
              if self.progressBar.parent().processStatus == False: return #The process was canceled
    
              # Finally add the layer and apply the options the user chose
              if self.bGroups: self.groups.addGroup( os.path.dirname( layerPath ) )
              ml = self.addLayer( layerPath, os.path.splitext( os.path.basename( layerPath ) )[ 0 ] )
              if self.bLayersOff: self.iface.legendInterface().setLayerVisible( ml, False )
              if self.bGroups: self.groups.orderLayer( ml, layerPath )
    
              step += 1
              self.progressBar.setValue( step )
            self.iface.mapCanvas().setRenderFlag( True ) # Finish the loading process 
    
            if self.bIsDoneDialog:
                QMessageBox.information( self.iface.mainWindow(), "Load Them All", 
                  QCoreApplication.translate( "Load Them All", "There have been " ) + 
                  QCoreApplication.translate( "Load Them All", "loaded " ) + str( numLayers ) + 
                  QCoreApplication.translate( "Load Them All", " layers succesfully." ), QMessageBox.Ok )
            return

        self.progressBar.reset() 
        self.progressBar.setMaximum( 100 )
        self.progressBar.setValue( 0 )
    
        if numLayers == 0:   
          if len(self.extension) == 1: 
            msgExtensions = str(self.extension[0])[1:]
          else:
            msgExtensions = ", ".join(str(x)[1:] for x in self.extension[:-1]) + \
              QCoreApplication.translate( "Load Them All", " or " ) + \
              str(self.extension[len(self.extension)-1])[1:]
          QMessageBox.information( self.iface.mainWindow(), "Load Them All", 
            QCoreApplication.translate( "Load Them All", "There are no <i>" ) + msgExtensions + 
            QCoreApplication.translate( "Load Them All", "</i> files to load from the base directory with this filter.\n") +
            QCoreApplication.translate( "Load Them All", "Change those parameters and try again." ), 
            QMessageBox.Ok )

    def addLayer( self, layerPath, layerBaseName ):
#        """ To be overriden by subclasses """
        pass
  
    def isEmptyLayer( self, layerPath ):
#        """ To be overriden by subclasses """
        pass
###############################
class LoadRasters( LoadFiles ):
  """ Subclass to load raster layers """
  def __init__( self, Loadfiles):#, baseDir, extension, iface, progressBar, bGroups, bLayersOff, bDoNotEmpty, bIsDoneDialog, numLayersToConfirm, filterType, params ):
    self.extension = extension
    self.baseDir = baseDir
    self.progressBar = progressBar
    self.filter = Filter()
    self.iface = iface
    self.lstFilesToLoad = []
    LoadFiles.__init__( self, baseDir, extension, iface, progressBar, bGroups, 
      bLayersOff, bDoNotEmpty, bIsDoneDialog, numLayersToConfirm )

    # Instantiate the appropriate Filter
    if filterType == 'NoFilter': self.filter = NoFilter() 
    elif filterType == 'AlphaNumericFilter': self.filter = AlphanumericFilter( *params )
    elif filterType == 'RasterTypeFilter': self.filter = RasterTypeFilter( *params )
    elif filterType == 'ComposedRasterFilter': self.filter = ComposedRasterFilter( *params )

    self.getFilesToLoad()
    self.loadLayers()

  def addLayer( self, layerPath, layerBaseName ):
    """ Add a raster layer """
    return self.iface.addRasterLayer( layerPath, layerBaseName )

  def isEmptyLayer( self, layerPath ):
    """ Do not check this on raster layers """
    return False

class Group():
  """ Class to deal with layer groups """
  def __init__( self, iface ):
    self.dicGroups = {} # layerDir : index
    self.toc = iface.legendInterface()
    #iface.connect( self.toc, SIGNAL( "groupIndexChanged(int old, int new)" ), self.updateIndexes )

  #def updateIndexes( self, old, new ):
    #indexOfOld = self.dicGroups.values().index( old )
    #keyOfNew = self.dicGroups.keys()[ indexOfOld ]
    #self.dicGroups[ keyOfNew ] = new

  def addGroup( self, path ):
    """ Add a group based on a layer's directory """
    if path not in self.dicGroups: 
      name = os.path.split( path )[ 1 ] # Get the last dir in the path
      index = self.toc.addGroup( name )
      self.dicGroups[ path ] = index

  def orderLayer( self, mapLayer, layerPath ):
    """ Put a layer in its group """
    layerDir = os.path.dirname( layerPath )
    self.toc.moveLayer( mapLayer,  self.getGroupIndex( layerDir ) )

  def getGroupIndex( self, layerDir ):
    """ Convenient method to get a group index based on the built dictionary """
    return self.dicGroups[ layerDir ] + 1
