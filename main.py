import sys, struct, threading, logging
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from mainwindow import Ui_MainWindow
from odroidClient import *
from streamClient import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open('style/mainWindow.css').read())
        logging.basicConfig(level=logging.DEBUG)
        self.setWindowIcon(QtGui.QIcon('img/KNR_logo.png'))
        self.threadpool = QtCore.QThreadPool()
        self.streamClientIsRunning = False
        self.odroidClientIsRunning = False
        self.odroidClientConnected = False
        self.connectButtons()

    def updateWidgets(self):
        self.odroidClient.signals.receivedPID.connect(self.pidSetup.update)
        self.odroidClient.signals.receivedMotors.connect(self.engineData.update)
        self.odroidClient.signals.receivedBoatData.connect(self.boatData.update)
        self.odroidClient.signals.receivedIMUData.connect(self.IMUGraph.update)
    def sendData(self):
        self.odroidClientConnected = True
        self.pidSetup.request_pid.connect(lambda arg: self.odroidClient.sendPIDRequest(arg))
        self.pidSetup.send_pid.connect(lambda arg: self.odroidClient.sendPID(arg))
        self.boatData.sendData.connect(lambda arg: self.odroidClient.sendControl(arg))

    def connectButtons(self):
        self.connectionBar.b_connect.pressed.connect(self.manageOdroidConnection)
        self.cameraContainer.connectButton.clicked.connect(self.manageStreamConnection)
    
    def manageOdroidConnection(self):
        if self.odroidClientIsRunning:
            self.stopOdroidConnection()        
        else:
            self.startOdroidConnection()

    def startOdroidConnection(self):
        addr = self.connectionBar.getAddr()
        if not addr:
            return
        self.odroidClient = odroidClient(addr)
        self.odroidClient.signals.connectionButton.connect(self.connectionBar.b_connectAction)
        self.odroidClient.signals.connectionInfo.connect(self.connectionBar.display)
        self.odroidClient.signals.clientConnected.connect(self.updateWidgets)
        self.odroidClient.signals.clientConnected.connect(self.sendData)
        self.odroidClient.signals.connectionRefused.connect(self.stopOdroidConnection)
        self.odroidClient.signals.connectionTerminated.connect(self.stopOdroidConnection)
        self.threadpool.start(self.odroidClient)
        self.odroidClientIsRunning= True

    def stopOdroidConnection(self):
        if self.odroidClientConnected:
            self.odroidClient.signals.receivedPID.disconnect()
            self.odroidClient.signals.receivedMotors.disconnect()
            self.odroidClient.signals.receivedBoatData.disconnect()
            self.pidSetup.request_pid.disconnect()
            self.pidSetup.send_pid.disconnect()
            self.boatData.sendData.disconnect()
            self.odroidClientConnected = False
        self.odroidClient.stop() 
        self.odroidClientIsRunning = False

    def manageStreamConnection(self):
            if self.streamClientIsRunning:
                self.stopStreamConnection()
            else:
                self.startStreamConnection()
    def startStreamConnection(self):
        ip, port = self.cameraContainer.clientData.displayText().split(":")
        self.streamClient = SimulationClient(ip=str(ip), port=int(port))
        self.updateStream()
        self.threadpool.start(self.streamClient)
        self.streamClientIsRunning = True

    def stopStreamConnection(self):
        self.streamClient.active = False
        self.streamClientIsRunning = False
    
    def updateStream(self):
        self.streamClient.signals.newFrame.connect(self.cameraContainer.update_frame)
def main():
    app=QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

main()