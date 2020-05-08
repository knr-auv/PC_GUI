from PyQt5 import QtWidgets, QtCore
from .boatData_ui import Ui_boatData



class boatData(QtWidgets.QWidget,Ui_boatData):
    sendData = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.setStyleSheet(open('style/boatData.css').read())
       self.mode_data.setText("simulation")
       self.b_start_sending.clicked.connect(self.start_clicked)
       self.b_stop_sending.clicked.connect(self.stop_clicked)
    def update(self, data): 
        self.hum_data.setText(str(data[1]))
        self.grasper_data.setText("not connected")
        self.bat_data.setText("----")
        self.depth_data.setText(str([2]))
       

    def start_clicked(self):
        data = int(self.t_interval.text())
        self.sendData.emit([1,data])

    def stop_clicked(self):
        data = [2]
        self.sendData.emit(data)