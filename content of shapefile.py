from PyQt4.QtGui import *

def analyze_shapefile():
    
    filename =QFileDialog.getOpenFileName(iface.mainWindow(),
                                                                "Select Shapefile",
                                                                "~",'*.shp')
    
    if not filename:
        print "Cancelled"
        return
        
    registry = QgsProviderRegistry.instance()
    provider = registry.provider("ogr",filename)
    if not provider.isValid():
        print "Invalid shapefile"
        return
        
    attr_names=[]
    for field in provider.fields():
        attr_names.append(field.name())    
        QgsMessageLog.logMessage("%s, %s"% (field.name(),field.type()),tag="SPARC")
        
    tot_length = 0
    tot_area = 0
    
    crs = provider.crs()
    calculator = QgsDistanceArea()
    calculator.setSourceCrs(crs)
    calculator.setEllipsoid(crs.ellipsoidAcronym())
    calculator.setEllipsoidalMode(crs.geographicFlag())
    
    for feature in provider.getFeatures(QgsFeatureRequest()):
        #cerca un campo con varianti di name
        if "name" in attr_names:
            feature_label = feature.attribute("name")
        elif "Name" in attr_names:
            feature_label = feature.attribute("name")
        elif "NAME" in attr_names:
            feature_label = feature.attribute("name")
        else:            
            feature_label = str(feature.id())
        
        #che tipo di shape?
        geometry = feature.geometry()
        
        if geometry.type() == QGis.Line:
            length = int(calculator.measure(geometry)/1000)
            tot_length = tot_length + length
            feature_info ="line of length %d kilometers" % length
        elif geometry.type() == QGis.Polygon:
            area = int(calculator.measure(geometry)/1000000)
            tot_area = tot_area + area
            feature_info ="polygon of area %d square kilometers" % area
        else:
            geom_type = qgis.vectorGeometryType(geometry.type())
            feature_info = "geometry of type %s" % geom_type
        
        #Programma iniziale che mostra area per paese
        QgsMessageLog.logMessage("%s: %s" % (feature_label,feature_info),tag="SPARC")
    
    #Status bar in basso sulla finestra principale...poco efficace
    #iface.mainWindow().statusBar().showMessage("Finito di analizzare i records.....")
    #iface.mainWindow().statusBar().clearMessage()
        
    #print "Total length of all line features: %d" % tot_length
    #print "Total area of all polygon features: %d" % tot_area
    
    from qgis.gui import *
    titolo = "Finito di analizzare i records.....\n"
    messaggio = "Total length of all line features: %d \n" % tot_length
    messaggio += "Total area of all polygon features: %d" % tot_area
    iface.messageBar().pushMessage(titolo,messaggio, level = QgsMessageBar.INFO)
    
analyze_shapefile()