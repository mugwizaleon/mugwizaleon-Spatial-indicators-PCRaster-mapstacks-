# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialMetricsDialog
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

from PyQt4 import QtCore, QtGui
from ui_QgsMapCanvas import ui_QgsMapCanvas



class QgsMapCanvas(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = ui_QgsMapCanvas()
        self.ui.setupUi(self)
