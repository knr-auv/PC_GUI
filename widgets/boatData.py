from PyQt5 import QtWidgets, QtCore
from .boatData_ui import Ui_boatData



class boatData(QtWidgets.QWidget,Ui_boatData):
    sendData = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.setStyleSheet(open('style/boatData.css').read())
       self.b_start_sending.clicked.connect(self.start_clicked)
       #self.b_stop_sending.clicked.connect(self.stop_clicked)
       self.b_stop_sending.hide()

    def update(self, data):
        text = data.decode('utf-8')
        text = text.split(',')
        self.mode_data.setText(text[0])
        self.grasper_data.setText(text[1])

       

    def start_clicked(self):
        data = int(self.t_interval.text())
        self.sendData.emit([1,data])

    def stop_clicked(self):
        data = [2]
        self.sendData.emit(data)