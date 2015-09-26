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
        
    tot_length = 0
    tot_area = 0
    
    crs = provider.crs()
    calculator = QgsDistanceArea()
    calculator.setSourceCrs(crs)
    calculator.setEllipsoid(crs.ellipsoidAcronym())
    calculator.setEllipsoidalMode(crs.geographicFlag())
        
analyze_shapefile()