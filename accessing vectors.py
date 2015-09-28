#registry = QgsProviderRegistry.instance()
#provider = registry.provider("ogr",r"D:\temporaggi\world\world.shp")


#symbol = QgsMarkerSymbolV2.createSimple({'width':1.0,'color' :"255,0,0"})
#renderer = QgsSingleSymbolRendererV2(symbol)
#layer = iface.addVectorLayer(r"D:\temporaggi\world\world.shp","paesi","ogr")
#layer.setRendererV2(renderer)

#layer = iface.addVectorLayer(r"D:\temporaggi\world\world.shp","paesi","ogr")
layer = iface.addVectorLayer(r"D:\temporaggi\nathearth\ne_50m_admin_0_countries.shp","paesi","ogr")
provider = layer.dataProvider()
request = QgsFeatureRequest()
request.setFilterExpression("'continent' = 'Africa'")
for feature in provider.getFeatures(QgsFeatureRequest()):
    print feature.attribute("NAME")

