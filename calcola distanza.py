import QgsMapTool

class DistanceCalculator(QgsMapTool):
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        self.iface = iface

    def canvasPressEvent(self, event):
        transform = self.iface.mapCanvas().getCoordinateTransform()
        self._startPt = transform.toMapCoordinates(event.pos().x(),
                                                   event.pos().y())



    def canvasReleaseEvent(self, event):
        transform = self.iface.mapCanvas().getCoordinateTransform()
        endPt = transform.toMapCoordinates(event.pos().x(),
                                           event.pos().y())

        crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        distance_calc = QgsDistanceArea()
        distance_calc.setSourceCrs(crs)
        distance_calc.setEllipsoid(crs.ellipsoidAcronym())
        distance_calc.setEllipsoidalMode(crs.geographicFlag())
        distance = distance_calc.measureLine([self._startPt,
                                                  endPt]) / 1000

        messageBar = self.iface.messageBar()
        messageBar.pushMessage("Distance = %d km" % distance,
                               level=QgsMessageBar.INFO,
                               duration=2)

calculator = DistanceCalculator(iface)
iface.mapCanvas().setMapTool(calculator)
