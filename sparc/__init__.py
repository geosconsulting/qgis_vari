# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sparc
                                 A QGIS plugin
 The resutl of the SPARC project for WFP
                             -------------------
        begin                : 2015-08-07
        copyright            : (C) 2015 by Fabio Lana
        email                : fabiolana.notizie@gmail.com
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load sparc class from file sparc.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .sparc_analysis import sparc
    return sparc(iface)
