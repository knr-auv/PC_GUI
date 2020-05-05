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
        self.client.connectionStatus.connect(self.connectionBar.b_connectAction)
        self.client.connectionInfo.connect(self.connectionBar.display)
        self.client.connectionInfo.connect(self.connectionRefused)
        self.client.dataReceived.connect(self.updateWidgets)
        self.client.connectionTerminated.connect(self.client.dataReceived.disconnect)
        self.client.connectionTerminated.connect(self.stopConnection)
        self.clientThread.finished.connect(self.clientThread.deleteLater)
        self.clientThread.start()

    def stopConnection(self):
        self.client.stop() 
        self.clientThread.quit()

    def connectionRefused(self,text):
        if text == "Connection refused" and self.client.active:
           self.stopConnection()
    def manageConnection(self):
        
        try:
            if self.clientThread.isRunning():
                self.stopConnection()
                
            else:
                self.startConnection()
        except (AttributeError, RuntimeError):
            self.startConnection()
        
            



    def updateWidgets(self, data):
        
        self.engineData.update([data[0],data[1],data[2],data[3],data[4]])
        self.boatData.update(data[0],data[1],data[2])


def main():
    app=QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

main()