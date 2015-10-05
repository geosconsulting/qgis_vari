from PyQt4.QtCore import *
from PyQt4.QtGui import *
import resources
from qgis.core import *
from qgis.gui import *

class GeometryInfoPlugin:
	def __init__(self,iface):
		self.iface = iface
		
	def initGui(self):
		icon = QIcon(":/plugins/geometryInfo/icon.png")
		self.action = QAction(icon,"Get Geometry Info",self.iface.mainWindow())
		self.action.setCheckable(True)
		QObject.connect(self.action,SIGNAL("triggered()"),self.onClick)
		self.iface.addPluginToMenu("Geometry Info",self.action)
		self.iface.addToolBarIcon(self.action)
		
	def unload(self):
		self.iface.removePluginMenu("Geometry Info",self.action)
		self.iface.removeToolBarIcon(self.action)
		
	def onClick(self):
		#QMessageBox.information(self.iface.mainWindow(),"debug","Click")
		if not self.action.isChecked():
			self.iface.mapCanvas().unsetMapTool(self.mapTool)
			self.mapTool = None
			return
		self.action.setChecked(True)
		self.mapTool = GeometryInfoMapTool(self.iface)
		self.mapTool.setAction(self.action)
		self.iface.mapCanvas().setMapTool(self.mapTool)
		

class GeometryInfoMapTool(QgsMapToolIdentify):
	def __init__(self,iface):
		QgsMapToolIdentify.__init__(self, iface.mapCanvas())
		self.iface = iface
		
	def canvasReleaseEvent(self,event):
		#print self
		found_features = self.identify(event.x(), event.y(),
				self.TopDownStopAtFirst,
				self.VectorLayer)
		if len(found_features) > 0:
			#for feature in found_features:				
			#	print feature.mFeature.attributes()
			layer = found_features[0].mLayer
			feature = found_features[0].mFeature
			geometry = feature.geometry()			
		#AGGIUNTA MIA SI APRE UN MESSAGGIO CON IL NOME DEL LAYER SU CUI HO FATTO CLICK
		#QMessageBox.information(self.iface.mainWindow(),"debug", " Si trova sul layer " + str(found_features[0].mLayer.name()))
		info = {}
		self.analyzeGeometry(geometry, layer, info)
		#QMessageBox.information(self.iface.mainWindow(),"debug", repr(info))
		fields = [("num_multi", "Number of multiparte geometries",""),
				  ("num_points", "Number of point geometries",""),
				  ("num_lines", "Number of line geometries",""),
				  ("tot_line_length","Total length of lines geometries","km"),
				  ("num_polygons", "Number of polygon geometries",""),
				  ("tot_poly_area","Total area of polygon geometries","square km"),
				  ("tot_poly_perimeter","Total perimeter of polygon geometries","km")]
		results = []
		for field,label,suffix in fields:
			if field in info:
				results.append("%s = %s %s" % (label,str(info[field]),suffix))
		QMessageBox.information(self.iface.mainWindow(),"Geometry Info", "\n".join(results))
	
	def analyzeGeometry(self, geometry, layer, info):
		crs = layer.dataProvider().crs()
		calculator = QgsDistanceArea()
		calculator.setSourceCrs(crs)
		calculator.setEllipsoid(crs.ellipsoidAcronym())
		calculator.setEllipsoidalMode(crs.geographicFlag())
		
		if geometry.isMultipart():
			self.add(info, 'num multi',1)
			parts = geometry.asGeometryCollection()
			for sub_geometry in parts:
				self.analyzeGeometry(sub_geometry,layer,info)
		elif geometry.type() == QGis.Point:
			self.add(info, 'num_points', 1)
		elif geometry.type() == QGis.Line:
			self.add(info, 'num_lines', 1)
			self.add(info,'tot_line_length',int(calculator.measure(geometry)/1000))
		elif geometry.type() == QGis.Polygon:
			self.add(info, 'num_polygons', 1)
			area=int(calculator.measure(geometry)/1000000)
			self.add(info,'tot_poly_area', area)
			perimetro = int(calculator.measurePerimeter(geometry)/1000)
			self.add(info,'tot_poly_perimeter', perimetro)
			#print(area,perimetro)
		
	def add(self, info,key,n):
		if key in info:
			info[key] = info[key] + n
		else:
			info[key] = n
				