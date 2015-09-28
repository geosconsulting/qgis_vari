layer_registry = QgsMapLayerRegistry.instance()
for layer in layer_registry.mapLayersByName("paesi"):
    layer_registry.removeMapLayer(layer.id())
    
for layer in layer_registry.mapLayersByName("population"):
    layer_registry.removeMapLayer(layer.id())

layer = iface.addVectorLayer(r"D:\temporaggi\world\world.shp","paesi","ogr")
layer_pop = iface.addVectorLayer(r"D:\temporaggi\world\world.shp","population","ogr")

from PyQt4.QtGui import QColor
categories = []

for value,color,label in [(0, "#660000","Antartica"),
                                   (2, "#006600","Africa"),
                                   (9, "#000066","Oceania"),
                                   (19, "#660066","The Americas"),
                                   (142, "#666600","Asia"),
                                   (150, "#006666","Europe")]:
        symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(color))
        categories.append(QgsRendererCategoryV2(value,symbol,label))

layer.setRendererV2(QgsCategorizedSymbolRendererV2("REGION",categories))
layer.triggerRepaint()

ranges = []

for min_pop,max_pop,color in [(0, 99999, "#332828"),
                                              (100000, 999999, "#4c3535"),
                                              (1000000, 4999999, "#663d3d"),
                                              (5000000, 9999999, "#804040"),
                                              (10000000, 19999999, "#993d3d"),
                                              (20000000, 49999999, "#b33535"),
                                              (50000000, 9999999999, "#cc2828")]:
        symbol_pop = QgsSymbolV2.defaultSymbol(layer_pop.geometryType())
        symbol_pop.setColor(QColor(color))
        ranges.append(QgsRendererRangeV2(min_pop,max_pop,symbol_pop,""))

layer_pop.setRendererV2(QgsGraduatedSymbolRendererV2("POP2005",ranges))
layer_pop.triggerRepaint()
        