from PyQt4.QtGui import *

class MyDialog(QDialog):
    
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Enter Coordinate")
        
        layout = QFormLayout(self)
        
        self.lat_label =QLabel("Latitude",self)
        self.lat_field =QLineEdit(self)
        
        self.long_label =QLabel("Longitude",self)
        self.long_field =QLineEdit(self)
        
        self.ok_btn =QPushButton("OK",self)
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn =QPushButton("Cancel",self)
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout = QHBoxLayout(self)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addRow(self.lat_label, self.lat_field)
        layout.addRow(self.long_label, self.long_field)
        layout.addRow(btn_layout)
        self.setLayout(layout)

from qgis.gui import *

dialog = MyDialog()
if dialog.exec_() == QDialog.Accepted:
    messaggio = "Ci Passo"
    iface.messageBar().pushMessage(messaggio, level = QgsMessageBar.INFO)
    lat = dialog.lat_field.text()
    long = dialog.long_field.text()
    print lat,long
else:
    messaggio = "Non Ci Passo"
    iface.messageBar().pushMessage(messaggio, level = QgsMessageBar.INFO)
