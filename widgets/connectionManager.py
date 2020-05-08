from PyQt5 import QtCore, QtGui, QtWidgets

from .connectionManager_ui import Ui_connectionManager

class connectionManager(QtWidgets.QWidget,  Ui_connectionManager):
    sendData = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)     
       self.b_start_sending.clicked.connect(self.start_clicked)
       self.b_stop_sending.clicked.connect(self.stop_clicked)
    def start_clicked(self):
        data = int(self.t_interval.text())
        self.sendData.emit([1,data])

    def stop_clicked(self):
        data = [2]
        self.sendData.emit(data)