from PyQt5 import QtCore, QtGui, QtWidgets

from .cameraContainer_ui import Ui_cameraContainer


class cameraContainer(QtWidgets.QWidget, Ui_cameraContainer):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connectButton.clicked.connect(self.start_client)
        self.client = False
        self.logo = QtGui.QImage("img/LOGO_OKON1.png")
        self.img = self.logo
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

    def paintEvent(self,e):
        qp = QtGui.QPainter()
        
        qp.begin(self)
        #qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        #qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        img  = self.img.scaled(self.size(),QtCore.Qt.KeepAspectRatio)
        qp.drawImage(QtCore.QRectF((self.width()-img.width())/2,(self.height()-img.height())/2, img.width(),img.height()), img)
        qp.end()

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = cameraContainer()
    window.show()
    sys.exit(app.exec_())
