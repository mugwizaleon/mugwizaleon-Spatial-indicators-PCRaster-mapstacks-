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
from SIAnimation import Ui_SIDialog



class SIAnimationDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        # Set up the user interface from Designer.
        self.ui = Ui_SIDialog()
        self.ui.setupUi(self)
