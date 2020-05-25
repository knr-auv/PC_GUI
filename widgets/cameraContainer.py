from PyQt5 import QtCore, QtGui, QtWidgets

from .cameraContainer_ui import Ui_cameraContainer


class cameraContainer(QtWidgets.QWidget, Ui_cameraContainer):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connectButton.clicked.connect(self.start_client)
        self.client = False
        self.logo = QtGui.QPixmap("img/LOGO_OKON1.png")
        self.framelabel.setPixmap(self.logo.scaled(self.framelabel.size(),QtCore.Qt.KeepAspectRatio))

    def set_logo(self):
        self.framelabel.setPixmap(self.logo.scaled(self.framelabel.size(),QtCore.Qt.KeepAspectRatio))

    def resizeEvent(self,event):
        QtGui.QWidget.resizeEvent(self, event)
        if self.client == False:
            self.framelabel.setPixmap(self.logo.scaled(self.framelabel.size(),QtCore.Qt.KeepAspectRatio))

    def start_client(self):
        if self.client is False:
            self.connectButton.setText("Disconnect")
            self.client = True
        else:
            self.connectButton.setText("Connect")
            self.client = False
            self.set_logo()

    def update_frame(self, frame):
        if self.client == True:
            self.displayImage(frame)
        else:
            self.set_logo()


    def displayImage(self, img):
        p = QtGui.QPixmap()
        p.loadFromData(img)
        #resizing to fit label and keep aspect ratio 1200/720
        p = p.scaled(self.framelabel.size(),QtCore.Qt.KeepAspectRatio)
        self.framelabel.setPixmap(p)

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = cameraContainer()
    window.show()
    sys.exit(app.exec_())
