from PyQt5 import QtWidgets, QtCore
from .connectionBar_ui import Ui_connectionBar


class connectionBar(QtWidgets.QWidget,Ui_connectionBar):
    #if widget send something to odroid you must create signal to comunicate with connection thread
    sendData = QtCore.pyqtSignal(object)    #the argument can be anything -> 'int', 'QString'... object is for passing python objects

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.timer = QtCore.QTimer(self)
       
       
       

#now you can add labels stylesheets... whatever you need
       self.b_connect.pressed.connect(self.b_connectAction)         
       self.setStyleSheet(open('./style/connectionBar.css').read())

    def b_connectAction(self):
            if self.b_connect.text()=="Connect":
                self.b_connect.setText("Disconnect")
                self.ip_text.hide()
                self.l_ip.hide()
                #self.l_connection.setAlignment(QtCore.Qt.AlignTop)
                

                
            else:
                self.b_connect.setText("Connect")
                self.l_ip.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.ip_text.show()

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
