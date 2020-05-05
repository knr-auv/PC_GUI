from PyQt5 import QtWidgets, QtCore
from .connectionBar_ui import Ui_connectionBar


class connectionBar(QtWidgets.QWidget,Ui_connectionBar):
    sendData = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.timer = QtCore.QTimer(self)
       #self.b_connect.pressed.connect(self.b_connectAction)         
       #self.setStyleSheet(open('./style/connectionBar.css').read())

    def b_connectAction(self,text):
            if text == "Connecting...":
                self.b_connect.setText(text)
                self.ip_text.setEnabled(False)
                self.b_connect.setEnabled(False)

            elif text == "Connect":
                self.b_connect.setEnabled(True)
                self.ip_text.setEnabled(True)
                self.b_connect.setText("Connect")
                #self.l_ip.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.ip_text.show()
                self.l_ip.show()
            elif text == "Disconnect":
                
                self.b_connect.setEnabled(True)
                self.b_connect.setText("Disconnect")
                self.ip_text.hide()
                self.l_ip.hide()

    def display(self, data):
        self.timer.setSingleShot(True)
        self.timer.start(5000)
        self.timer.timeout.connect(lambda: self.l_connection.setText(""))    
        
        self.l_connection.setText(data)

    def update(self, humidity):
        val ="humidity: "
        val+=str(humidity)
        self.l_connection.setText(val)

    def getAddr(self):
        val = self.ip_text.text()
        try:
            val = val.split(":")
            host = val[0]
            port = int(val[1])
        except IndexError:
            return None
        return (host, port)

#just provide data, and attach this function to send button
    def send(self, data=()):
        self.sendData.emit(data)

   

#Each widget can work like an standalone app. Just uncomment the code bellow and remove dot from import function.
#import sys
#app=QtWidgets.QApplication(sys.argv)
#window = connectionBar()
#window.show()
#app.exec_()
