import sys, struct, threading, logging,json
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from mainwindow import Ui_MainWindow
from tools.odroidClient import *
from tools.streamClient import *
from tools.pad import *
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        #self.setStyleSheet(open('style/mainWindow.css').read())
        logging.basicConfig(level=logging.DEBUG)
        self.setWindowIcon(QtGui.QIcon('img/KNR_logo.png'))
        self.threadpool = QtCore.QThreadPool()
        with open("tools/protocol.json",'r') as fd:
            self.protocol = json.load(fd)
        self.streamClientIsRunning = False
        self.odroidClientIsRunning = False
        self.odroidClientConnected = False
        self.padTimer = QtCore.QTimer()
        self.changeWidgets()
        self.connectButtons()
    
    
    def updateWidgets(self):
        self.odroidClient.signals.armed.connect(self.controlSettings.armed)
        self.odroidClient.signals.disarmed.connect(self.controlSettings.disarmed)
        self.odroidClient.signals.receivedPID.connect(self.pidSetup.update)
        self.odroidClient.signals.receivedMotors.connect(self.engineData.update)
        self.odroidClient.signals.receivedBoatData.connect(self.boatData.update)
        self.odroidClient.signals.receivedIMUData.connect(self.IMUGraph.update)

    def sendData(self):
        self.controlSettings.armSignal.connect(lambda arg: self.odroidClient.arm(arg))
        self.controlSettings.disarmSignal.connect(self.odroidClient.disarm)
        self.pidSetup.request_pid.connect(lambda arg: self.odroidClient.sendPIDRequest(arg))
        self.pidSetup.send_pid.connect(lambda arg: self.odroidClient.sendPID(arg))
        self.boatData.sendData.connect(lambda arg: self.odroidClient.sendControl(arg))

    def disconnectSignals(self):
        self.controlSettings.armSignal.disconnect()
        self.controlSettings.disarmSignal.disconnect()
        self.odroidClient.signals.receivedPID.disconnect()
        self.odroidClient.signals.receivedMotors.disconnect()
        self.odroidClient.signals.receivedBoatData.disconnect()
        self.pidSetup.request_pid.disconnect()
        self.pidSetup.send_pid.disconnect()
        self.boatData.sendData.disconnect()

    #changing few settings on camera clones
    def changeWidgets(self):
        self.pidCamera.connectButton.hide()
        self.pidCamera.clientData.hide()
        self.controlCamera.connectButton.hide()
        self.controlCamera.clientData.hide()
        pass
    #stuff that will happen after succesful connection    
    def whenConnected(self):
        self.odroidClientConnected = True
        self.controlSettings.padSettings.connect(lambda arg: self.start_control(arg))
        self.controlSettings.disarmSignal.connect(self.stop_control)

    #connectiong buttons for controlling connection
    def connectButtons(self):
        self.connectionBar.b_connect.pressed.connect(self.manageOdroidConnection)
        self.cameraContainer.connectButton.clicked.connect(self.manageStreamConnection)

    #handling pad control thread. TODO make a class capable of selecting control methods
    def start_control(self, config):
        print("starting pad stuff")
        self.control = PadSteering(config)
        self.threadpool.start(self.control)
        self.control.signals.getData_callback.connect(lambda arg: self.odroidClient.sendPad(arg))
        self.padTimer.setInterval(int(self.controlSettings.l_interval.text()))
        self.padTimer.timeout.connect(self.control.get_data)
        self.padTimer.start()

    def stop_control(self):
        self.padTimer.stop()
        self.padTimer.timeout.disconnect()
        self.control.active = False

    #establishing connection with odroid
    def manageOdroidConnection(self):
        if self.odroidClientIsRunning:
            self.stopOdroidConnection()        
        else:
            self.startOdroidConnection()

    def startOdroidConnection(self):
        addr = self.connectionBar.getAddr()
        if not addr:
            return
        self.odroidClient = odroidClient(addr, self.protocol)
        self.odroidClient.signals.connectionButton.connect(self.connectionBar.b_connectAction)
        self.odroidClient.signals.connectionInfo.connect(self.connectionBar.display)
        self.odroidClient.signals.clientConnected.connect(self.updateWidgets)
        self.odroidClient.signals.clientConnected.connect(self.sendData)
        self.odroidClient.signals.clientConnected.connect(self.whenConnected)
        self.odroidClient.signals.connectionRefused.connect(self.stopOdroidConnection)
        self.odroidClient.signals.connectionTerminated.connect(self.stopOdroidConnection)
        self.threadpool.start(self.odroidClient)
        self.odroidClientIsRunning= True

    def stopOdroidConnection(self):
        if self.odroidClientConnected:
            self.disconnectSignals()

            self.odroidClientConnected = False
        self.odroidClient.stop() 
        self.odroidClientIsRunning = False

    #establishing connection with jetson/simulation
    #since this is other client 
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
        self.tabs.currentChanged.connect(self.updateStream)
        self.streamClientIsRunning = True

    def stopStreamConnection(self):
        self.streamClient.active = False
        self.streamClientIsRunning = False
    
    def updateStream(self, index=None):
        if index == None:
            self.streamClient.signals.newFrame.connect(self.cameraContainer.update_frame)
            return
        self.disconnectStream()
        if index ==0:
            self.streamClient.signals.newFrame.connect(self.cameraContainer.update_frame)
        elif index ==1:
            self.streamClient.signals.newFrame.connect(self.pidCamera.update_frame)
        elif index ==2:
            self.streamClient.signals.newFrame.connect(self.controlCamera.update_frame)

    def disconnectStream(self):
        self.streamClient.signals.newFrame.disconnect()

def main():
    app=QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

main()