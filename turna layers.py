#for layer in iface.legendInterface().layers():
 #   print layer.name()
   
#layer = iface.addVectorLayer(r"D:\temporaggi\nathearth\ne_50m_admin_0_countries.shp","paesi","ogr")

registry = QgsProviderRegistry.instance()
provider = registry.provider("ogr",r"D:\temporaggi\nathearth\ne_50m_admin_0_countries.shp")

if not provider.isValid():
    print "Invalido"


for field in provider.fields():
    print field.name(),field.typeName()
       
for feature in provider.getFeatures(QgsFeatureRequest()):
    print feature.attribute("region_wb")
    