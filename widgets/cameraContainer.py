from PyQt5 import QtCore, QtGui, QtWidgets




class cameraContainer(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.connectButton = QtWidgets.QPushButton(self, text = "Connect")
        self.clientData = QtWidgets.QLineEdit(self,text = "127.0.0.1:44209")
        self.connectButton.clicked.connect(self.start_client)
        self.client = False
        self.logo = QtGui.QImage("img/LOGO_OKON1.png")
        self.img = self.logo
        self.stream = QtWidgets.QWidget(self)
        self.stream.paintEvent=self.pEvent
        #self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.stream)
        self.horizontalLayout.addWidget(self.clientData)
        self.horizontalLayout.addWidget(self.connectButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.repaint()


    def start_client(self):
        if self.client is False:
            self.connectButton.setText("Disconnect")
            self.client = True
        else:
            self.connectButton.setText("Connect")
            self.client = False
            self.setLogo()


    def update_frame(self, img):
        if self.client == True:
            self.img.loadFromData(img)
        else:
            self.img = self.logo
        self.repaint()

    def setLogo(self):
        self.img = self.logo
        self.repaint()

    def pEvent(self,e):
        qp = QtGui.QPainter()
        qp.begin(self.stream)
        #qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        #qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        img  = self.img.scaled(self.size(),QtCore.Qt.KeepAspectRatio)
        qp.drawImage(QtCore.QRectF((self.width()-img.width())/2,(self.height()-img.height())/2, img.width(),img.height()), img)
        #qp.end()

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = cameraContainer()
    window.show()
    sys.exit(app.exec_())
