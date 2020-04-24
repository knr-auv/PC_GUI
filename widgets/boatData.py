from PyQt5 import QtWidgets, QtCore
from .boatData_ui import Ui_boatData



class boatData(QtWidgets.QWidget,Ui_boatData):


    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.setStyleSheet(open('style/boatData.css').read())
      
       