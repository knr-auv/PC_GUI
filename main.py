import sys, struct
from PyQt5 import QtWidgets, uic, QtGui, QtCore


from mainwindow import Ui_MainWindow
from connectionHandler import *




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        #self.setStyleSheet(open('style/mainWindow.css').read())
        self.setWindowIcon(QtGui.QIcon('img/KNR_logo.png'))
        self.connectButtons()
      
    def connectButtons(self):
        self.connectionBar.b_connect.pressed.connect(self.manageConnection)
        
    def startConnection(self):
        addr = self.connectionBar.getAddr()
        if not addr:
            return
        self.clientThread=QtCore.QThread()
        self.client = connectionHandler(addr)
        self.client.moveToThread(self.clientThread)
        self.clientThread.started.connect(self.client.run)
        self.client.connectionButton.connect(self.connectionBar.b_connectAction)
        self.client.connectionInfo.connect(self.connectionBar.display)
        self.client.clientConnected.connect(self.updateWidgets)
        self.client.clientConnected.connect(self.sendData)
        self.client.connectionRefused.connect(self.stopConnection)
        self.client.connectionTerminated.connect(self.stopConnection)
        self.clientThread.finished.connect(self.clientThread.deleteLater)
        self.clientThread.start()

    def updateWidgets(self):
        #self.client.receivedPID.connect(self.pidSetup.update)
        self.client.receivedMotors.connect(self.engineData.update)
        self.client.receivedBoatData.connect(self.boatData.update)

    def sendData(self):
        #for example self.pidsetup.signal.connet(self.client.pidSend)
        pass
    def stopConnection(self):
        self.client.stop() 
        self.clientThread.quit()


    def manageConnection(self):
        try:
            if self.clientThread.isRunning():
                self.stopConnection()
            else:
                self.startConnection()
        except (AttributeError, RuntimeError):
            self.startConnection()
        
def main():
    app=QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

main()