def loadMaps(self):
    import FilesNaming
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
        filename = (FilesNaming.FilesNames(Naming, Metric))[0]
        file_list =  glob.glob(filename)
        file_list.sort()
        self.iface.addRasterLayer(str(file_list[0])).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) ) 
        canvas = qgis.utils.iface.mapCanvas()
        canvas.zoomToFullExtent()
        canvas.refresh()
        
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
    filename = (FilesNaming.FilesNames(Naming, Metric))[0]
    file_list =  glob.glob(filename)   
    for index in file_list:            
        self.iface.addRasterLayer(str(index)).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) ) 
        canvas = qgis.utils.iface.mapCanvas()
        canvas.zoomToFullExtent()
        canvas.refresh()
        time.sleep(float(self.dlg5.ui.txtBaseDir2_5.text()))
        g = qgis.utils.iface.legendInterface().layers()
        if len(g) == 1 : pass
        else:
            Player = g[1] 
            self.iface.legendInterface().setLayerVisible(Player, False)
        


def Next(self):
    self.actionRemove()
    import numpy
    import FilesNaming
    numpy.seterr(divide='ignore', invalid='ignore', over='ignore')
    self.dataDir = str(self.dlg.ui.txtBaseDir2_5.text())
    os.chdir(self.dataDir )
    Naming = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[1]
    Metric = (FilesNaming.argments(self.dlg.ui.comboBox_3.currentText() ))[2]
    filename = (FilesNaming.FilesNames(Naming, Metric))[0]
    file_list =  glob.glob(filename)
    file_list.sort()
    layer = qgis.utils.iface.activeLayer()
    self.iface.legendInterface().setLayerVisible(layer, False)
    if layer is None :
        index = 0
    elif layer.name()+'.tiff' not in file_list:
        index = 0
    else: 
        counter = file_list.index(layer.name()+'.tiff')        
        index = counter + 1
        if counter == len(file_list) - 1 :
            layers = self.iface.legendInterface().layers()
            self.iface.legendInterface().addGroup("group_foo")
            for layer in layers : 
                self.iface.legendInterface().moveLayer( layer, 0 )
            index = 0
    rlayer = self.iface.addRasterLayer(str(file_list[index])).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) ) 
    canvas = qgis.utils.iface.mapCanvas()
    canvas.zoomToFullExtent()
    canvas.refresh()
    
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
    filename = (FilesNaming.FilesNames(Naming, Metric))[0]
    file_list =  glob.glob(filename)
    file_list.sort()
    layer = qgis.utils.iface.activeLayer()
    self.iface.legendInterface().setLayerVisible(layer, False)
    if layer is None :
        index = len(file_list) - 1
    elif layer.name()+'.tiff' not in file_list:
        index = len(file_list) - 1
    else: 
        counter = file_list.index(layer.name()+'.tiff')
        index = counter - 1
        if counter == 0 :
            layers = self.iface.legendInterface().layers()
            self.iface.legendInterface().addGroup("group_foo")
            for layer in layers : 
                if self.iface.legendInterface().isLayerVisible(layer) : self.iface.legendInterface().moveLayer( layer, 0 )
            index = len(file_list) - 1
    self.iface.addRasterLayer(str(file_list[index])).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) ) 
    canvas = qgis.utils.iface.mapCanvas()
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
    filename = (FilesNaming.FilesNames(Naming, Metric))[0]
    file_list =  glob.glob(filename)
    file_list.sort()
    layer = qgis.utils.iface.activeLayer()
    self.iface.legendInterface().setLayerVisible(layer, False)
    index = len(file_list) - 1
    self.iface.addRasterLayer(str(file_list[index])).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) ) 
    canvas = qgis.utils.iface.mapCanvas()
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
    filename = (FilesNaming.FilesNames(Naming, Metric))[0]
    file_list =  glob.glob(filename)
    file_list.sort()
    layer = qgis.utils.iface.activeLayer()
    self.iface.legendInterface().setLayerVisible(layer, False)
    index = 0
    self.iface.addRasterLayer(str(file_list[index])).setCrs( QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId) )
    canvas = qgis.utils.iface.mapCanvas()
    canvas.zoomToFullExtent()
    canvas.refresh()
