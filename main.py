import sys, struct
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from mainwindow import Ui_MainWindow
from connectionHandler import *




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setStyleSheet(open('style/mainWindow.css').read())
        self.serverRunning = False
        self.connectButtons()
        self.engineData.update([1,1,1,1,1])


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
        self.server.serverStarted.connect(lambda data: self.connectionBar.l_connection.setText(("server listening on: " + str(data))))
        self.server.clientConnected.connect(self.clientHandler)
        self.server.connectionTerminated.connect(self.server.dataReceived.disconnect)
        self.serverThread.finished.connect(self.serverThread.deleteLater)
        self.serverThread.start()

    #stoping server
    def stopConnection(self):
        self.serverRunning = False
        self.server.stop()            
        self.serverThread.quit()

    def clientHandler(self,data):
        self.connectionBar.l_connection.setText("client connected: " + str(data))
        self.server.dataReceived.connect(self.updateWidgets)
       
    def manageConnection(self):
        if not self.serverRunning:
            self.startConnection()
        else:
            self.stopConnection()
            


    def updateWidgets(self, data):
        self.connectionBar.update(len(data))
        pwm = struct.unpack('iiiii',data) 
        self.engineData.update(list(pwm))


def main():
    app=QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

main()