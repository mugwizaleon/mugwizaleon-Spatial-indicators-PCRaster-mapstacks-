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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load SpatialMetrics class from file SpatialMetrics
    from spatialmetrics import SpatialMetrics
    return SpatialMetrics(iface)
