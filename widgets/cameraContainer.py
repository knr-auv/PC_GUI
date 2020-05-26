from PyQt5 import QtCore, QtGui, QtWidgets

from .cameraContainer_ui import Ui_cameraContainer


class cameraContainer(QtWidgets.QWidget, Ui_cameraContainer):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connectButton.clicked.connect(self.start_client)
        self.client = False
        self.logo = QtGui.QPixmap("img/LOGO_OKON1.png")
        self.img = self.logo
        self.repaint()


    def start_client(self):
        if self.client is False:
            self.connectButton.setText("Disconnect")
            self.client = True
        else:
            self.connectButton.setText("Connect")
            self.client = False
            self.set_logo()

    def update_frame(self, img):
        if self.client == True:
            self.img.loadFromData(img)
        else:
            self.self.img = self.logo
        self.repaint()

    def paintEvent(self,e):
        qp = QtGui.QPainter()
        
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        self.img  = self.img.scaled(self.size(),QtCore.Qt.KeepAspectRatio)
        #qp.scale(self.width(),self.height())
        #print(self.rect())
        qp.drawPixmap((self.width()-self.img.width())/2,(self.height()-self.img.height())/2, self.img.width(),self.img.height(), self.img)
        qp.end()

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = cameraContainer()
    window.show()
    sys.exit(app.exec_())
