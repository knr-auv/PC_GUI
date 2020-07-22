from .osdSettings_ui import Ui_osdSettings
from PyQt5 import QtWidgets, QtCore
import json
class osdSettings(QtWidgets.QWidget, Ui_osdSettings):
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self) 
        #self.setMinimumSize(100,500)
        self.osdWidget = None
        self.config = {}
        self.loadConfig()
        for i in self.findChildren(QtWidgets.QSpinBox):
            i.setAlignment(QtCore.Qt.AlignCenter)
            i.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            i.setMaximum(100)
            i.setMinimum(0)
            i.valueChanged.connect(lambda: self.osdWidget.setConfig(self.getConfig()))
        for i in self.findChildren(QtWidgets.QRadioButton):
            i.toggled.connect(lambda: self.osdWidget.setConfig(self.getConfig()))

    def doWhenConnected(self):
        self.b_setFS.setEnabled(True)

    def doWhenDisconnected(self):
        self.b_setFS.setEnabled(False)

    def setWidget(self, arg):
        self.b_setFS.setEnabled(False)
        self.osdWidget = arg
        self.b_setFS.clicked.connect(self.osdWidget.showFull)
        self.osdWidget.setConfig(self.getConfig())
    
    def getConfig(self):
        for i in self.findChildren(QtWidgets.QSpinBox):
            self.config[i.objectName()]=i.value()
        for i in self.findChildren(QtWidgets.QRadioButton):
            self.config[i.objectName()]=i.isChecked()
        self.saveConfig()
        return self.config

    def saveConfig(self):
        with open('config/osdConfig.json','w')as fd:
            json.dump(self.config, fd, indent=1)

    def loadConfig(self):
        try:
            with open("config/osdConfig.json",'r') as fd:
                self.config = json.load(fd)
            for i in self.findChildren(QtWidgets.QSpinBox):
                i.setValue(self.config[i.objectName()])
            for i in self.findChildren(QtWidgets.QRadioButton):
                i.setChecked(self.config[i.objectName()])

        except: 
            pass
            