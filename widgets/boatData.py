from PyQt5 import QtWidgets, QtCore
from .boatData_ui import Ui_boatData



class boatData(QtWidgets.QWidget,Ui_boatData):


    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.setStyleSheet(open('style/boatData.css').read())
       self.mode_data.setText("simulation")
    def update(self, data):
        
        self.hum_data.setText(str(data[1]))
        self.grasper_data.setText("not connected")
        self.bat_data.setText("----")
        self.depth_data.setText(str([2]))
       