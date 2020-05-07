from PyQt5 import QtCore, QtGui, QtWidgets

from .connectionManager_ui import Ui_connectionManager

class connectionManager(QtWidgets.QWidget,  Ui_connectionManager):
    sendData = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)     
       self.b_start_sending.clicked.connect(self.clicked)

    def clicked(self):
        data = [1,0.03]
        self.sendData.emit(data)
        