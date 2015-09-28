from PyQt4.QtCore import QSettings
QSettings().setValue("/Projections/defaultBehaviour", "useGlobal")

registry = QgsProviderRegistry.instance()
provider = registry.provider("gdal","d:/temporaggi/world/e10g")

raster_extent = provider.extent()
raster_width = provider.xSize()
raster_height = provider.ySize()
no_data_value = provider.srcNoDataValue(1)

histogram = {}
block = provider.block(1, raster_extent, raster_width,raster_height)

#QgsMessageLog.logMessage("larghezza %.2f altezza %.2f" % (raster_width,raster_height),tag="SPARC")

if block.isValid():
    for x in range(raster_width):
        for y in range(raster_height):
            elevation = block.value(x,y)
            QgsMessageLog.logMessage("elevazione %.2f" % (elevation),tag="SPARC")
#            if elevation != no_data_value:
#                try:
#                    histogram[elevation]+=1
#                except KeyError:
#                    histogram[elevation] = 1
                    
#    for height in sorted(histogram.keys()):
#        print height,histogram[height]