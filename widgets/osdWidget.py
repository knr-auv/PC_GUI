from PyQt5 import QtWidgets,QtGui,QtCore
from math import sin, cos, radians, sqrt
class osdWidget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.logo = QtGui.QImage("img/LOGO_OKON1.png")
        self.img= self.logo
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self.client = False
        self.roll = 0
        self.pitch = 0
        self.yaw = 0 
        self. depth = 0
        self.setSizePolicy(sizePolicy)
        self.show()
        self.store = self.windowFlags()
        self.hintTimer = QtCore.QTimer()
        self.hintTimer.timeout.connect(self.setHintVisibility)
        self.hint = False
        self.config ={}

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        self.scaleImg()
        if self.client ==True:
            if self.hint == True:
                self.displayHint()
            if self.config['horizon_active']:
                x,y = self.grid(self.config['horizon_x'],self.config['horizon_y'])
                self.drawArtificialHorizont(x,y,60,qp)
            if self.config['depth_active']:
                x,y = self.grid(self.config['depth_x'],self.config['depth_y'])
                self.drawDepth(x,y,qp)
            if self.config['heading_active']:
                x,y = self.grid(self.config['heading_x'],self.config['heading_y'])
                self.drawHeading(x,y,qp)
        self.displayStream(qp)

    def setConfig(self, arg):
        self.config = arg
    def showFull(self):
        self.setWindowFlag(QtCore.Qt.Window)
        self.setCursor(QtCore.Qt.BlankCursor)
        self.showFullScreen()
        self.hint= True
        self.hintVisibility = 1
        self.hintTimer.start(30)

    def setHintVisibility(self):
        if self.hintVisibility>0:
            self.hintVisibility -=0.01
        elif self.hintVisibility == 0:
            self.hint = False
            self.hintTimer.stop()

    def displayHint(self):
        painter = QtGui.QPainter(self.scaledImg)
        text = "Press 'Esc' to exit."
        metrics = QtGui.QFontMetrics(self.font())
        border = max(4, metrics.leading())

        rect = metrics.boundingRect(0, 0, self.width() - 2*border,
                int(self.height()*0.125), QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap,
                text)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.setPen(QtGui.QColor(255, 255, 255, int(255*self.hintVisibility)))
        painter.fillRect(QtCore.QRect(0, 0, self.width(), rect.height() + 2*border),
                QtGui.QColor(255, 0, 0, int(127*self.hintVisibility)))
        painter.drawText((self.width() - rect.width())/2, border, rect.width(),
                rect.height(), QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap, text)

    def exitFullScreen(self):
        self.unsetCursor()
        self.setWindowFlags(self.store)
        self.showNormal()

    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Escape:
            self.exitFullScreen()

    def storeData(self, data):
        self.roll = data[0]
        self.pitch = data[1]
        self.yaw = data[2]
        self.depth = data[3]

    def setLogo(self):
        self.img = self.logo

    def update(self, img):

        if self.client == True:
            self.img.loadFromData(img)
            
        else:
            print("Here")
            self.img = self.logo
        self.repaint()




    def grid(self, x,y):
        X = self.scaledImg.width()/100*x
        Y = self.scaledImg.height()/100*y
        return X, Y

    def drawDepth(self, centerX, centerY, painter):
        painter.begin(self.scaledImg)
        pen = QtGui.QPen()
        #pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        font = QtGui.QFont()
        #font.setWeight(1)
        font.setPixelSize(20)
        painter.setFont(font)
        text = '{:.2f}'.format(self.depth)+' m'
        painter.drawText(centerX-painter.fontMetrics().width(text)/2, centerY+painter.fontMetrics().height()/3, text)
        painter.end()

    def drawHeading(self,centerX,centerY,painter):
        painter.begin(self.scaledImg)
        width = 4
        height = 10
        font = QtGui.QFont()
        font.setPixelSize(10)
        painter.setFont(font)
        for i in range(-45+int(self.yaw%10), 45+int(self.yaw)%10):  
            if i%10 ==0:
                painter.drawLine(centerX-((self.yaw%10)-i)*width,centerY+height,centerX-((self.yaw%10)-i)*width,centerY-height)
                val = int(self.yaw+i-self.yaw%10)
                if val<0:
                    val+=360
                text=str(val)
                painter.drawText(centerX-((self.yaw%10)-i)*width-painter.fontMetrics().width(text)/2,centerY+2*painter.fontMetrics().height(),text)
            if i%5 ==0:
                painter.drawLine(centerX-((self.yaw%10)-i)*width,centerY+height/2,centerX-((self.yaw%10)-i)*width,centerY-height/2)
        path = QtGui.QPainterPath()
        painter.setPen(QtCore.Qt.green)
        painter.setBrush(QtCore.Qt.green)
        path.moveTo(centerX-height/2, centerY-2*height)
        path.lineTo(centerX+height/2, centerY-2*height)
        path.lineTo(centerX, centerY-1.2*height)
        path.lineTo(centerX-height/2, centerY-2*height)
        painter.drawPath(path)

        painter.end()

    def drawArtificialHorizont(self,centerX,centerY, width, painter):
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('#66ff66'))
        pen.setWidthF(2.)
        painter.begin(self.scaledImg)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform , True)        
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.LosslessImageRendering, True)
        painter.setPen(pen)

        halfWidth = width/2
        sinl = sin(radians(self.roll))
        cosl = cos(radians(self.roll))
        endHeightAdjust = halfWidth*sinl
        endWidthAdjust = halfWidth*cosl
        centerSize = 15
        centerHalf= centerSize/2
        centerHeightAdjust = centerHalf*sinl
        centerWidthAdjust = centerHalf*cosl

        #fancy rotating bar
        painter.drawLine(centerX-endWidthAdjust, centerY+endHeightAdjust, centerX-centerWidthAdjust,centerY+centerHeightAdjust)
        painter.drawLine(centerX-centerWidthAdjust,centerY+centerHeightAdjust, centerX+centerHeightAdjust,centerY+centerWidthAdjust)
        painter.drawLine(centerX+centerHeightAdjust,centerY+centerWidthAdjust, centerX+centerWidthAdjust,centerY-centerHeightAdjust)
        painter.drawLine( centerX+centerWidthAdjust,centerY-centerHeightAdjust,centerX+endWidthAdjust, centerY-endHeightAdjust)
      
        painter.end()
    def scaleImg(self):
        self.scaledImg  = self.img.scaled(self.size(),QtCore.Qt.KeepAspectRatio)

    def displayStream(self,painter):
        painter.begin(self)
        painter.drawImage(QtCore.QRectF((self.width()-self.scaledImg.width())/2,(self.height()-self.scaledImg.height())/2, self.scaledImg.width(),self.scaledImg.height()), self.scaledImg)
        painter.end()
        