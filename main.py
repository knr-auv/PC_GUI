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
        self.serverRunning = False
        self.connectButtons()
        


    def connectButtons(self):
        self.connectionBar.b_connect.pressed.connect(self.manageConnection)

   
    #starting server
    def startConnection(self):
        addr = self.connectionBar.getAddr()
        if not addr:
            return
        self.serverRunning = True
        self.serverThread=QtCore.QThread()
        self.server = connectionHandler(addr)
        self.server.moveToThread(self.serverThread)
        self.serverThread.started.connect(self.server.run)
        self.server.connectionInfo.connect(self.connectionBar.display)
        self.server.clientConnected.connect(lambda: self.server.dataReceived.connect(self.updateWidgets))
        self.server.connectionTerminated.connect(self.server.dataReceived.disconnect)
        self.serverThread.finished.connect(self.serverThread.deleteLater)
        self.serverThread.start()

    def stopConnection(self):
        self.serverRunning = False
        self.server.stop()            
        self.serverThread.quit()
   
    def manageConnection(self):
        if not self.serverRunning:
            self.startConnection()
        else:
            self.stopConnection()
           



    def updateWidgets(self, data):
        
        self.engineData.update([data[0],data[1],data[2],data[3],data[4]])
        self.boatData.update(data[0],data[1],data[2])


def main():
    app=QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

main()