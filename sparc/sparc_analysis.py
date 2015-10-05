# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sparc
                                 A QGIS plugin
 The resutl of the SPARC project for WFP
                              -------------------
        begin                : 2015-08-07
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Fabio Lana
        email                : fabiolana.notizie@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox 
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from sparc_analysis_dialog import sparcDialog
import os.path
from opengeo.config import iface


class sparc:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'sparc_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = sparcDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&sparc')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'sparc')
        self.toolbar.setObjectName(u'sparc')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('sparc', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/sparc/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'SPARC'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&sparc'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        
        self.dlg.cmbCountries.clear()
        self.dlg.cmbPopulation.clear()
        self.dlg.cmbHazard.clear()        
        
        # Collect all loaded layers            
        from qgis.core import QgsMapLayerRegistry
        layersDict = QgsMapLayerRegistry.instance().mapLayers()
        
        # Classifying layers
        from qgis.core import QgsMapLayer
        vectors = [] 
        rasters = []
        for (id, map) in layersDict.items():
            if (map.type() == QgsMapLayer.VectorLayer):
                vectors.append( map.name() )
            elif (map.type() == QgsMapLayer.RasterLayer):
                rasters.append( map.name() )
            else:
                print "Not Raster nor Vector for layer with id:", id
        
        # Populating the combo box        
        self.dlg.cmbCountries.insertItems(0, vectors)
        self.dlg.cmbPopulation.insertItems(0, rasters)
        self.dlg.cmbHazard.insertItems(0, rasters)
        
        
        # show the dialog
        self.dlg.show()
        
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        # See if OK was pressed
        if result:            
            # Do something useful here - delete the line containing pass and
            # substitute with your code.        
            #msgBox = QMessageBox()            
            #msgBox.information(self.iface.mainWindow(),"Layer Scelto", "Il layer scelto nel primo combo e' %s" % self.dlg.cmbCountries.currentText())
            
            pass
