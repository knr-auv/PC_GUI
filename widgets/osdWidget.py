from PyQt5 import QtWidgets,QtGui,QtCore

class osdWidget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.img = QtGui.QPixmap("img/engines.jpg")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        #self.resize(100,100)
        self.setSizePolicy(sizePolicy)
        self.show()

    def update(self, img):
        self.img.loadFromData(img)
        self.repaint()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self.img)
        qp.drawLine(0,self.img.height()/2,self.img.width(),self.img.height()/2)
        qp.end()
        qp.begin(self)
        self.img  = self.img.scaled(self.size(),QtCore.Qt.KeepAspectRatio)
        #qp.scale(self.width(),self.height())
        #print(self.rect())
        qp.drawPixmap((self.width()-self.img.width())/2,(self.height()-self.img.height())/2, self.img.width(),self.img.height(), self.img)
        qp.end()
        

