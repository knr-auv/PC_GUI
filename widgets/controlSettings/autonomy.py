from PyQt5 import QtWidgets, QtCore, QtGui
from .autonomy_ui import Ui_autonomy

class autonomyWidget(QtWidgets.QWidget,Ui_autonomy):

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self) 
       self.logo = QtGui.QImage("img/LOGO_OKON1.png")
       self.img = self.logo.copy()

       self.stream.paintEvent = self.pe
       self.client = False

    def pe(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self.stream)
        img  = self.img.scaled(self.size(),QtCore.Qt.KeepAspectRatio)
        qp.drawImage(QtCore.QRectF(0,0, img.width(),img.height()), img)
        self.stream.setMinimumSize(img.size())
    def setOsdWidget(self, arg):
        self.osdWidget = arg

    def menage_detection(self, detection):
        if detection ==-1:
            return
        fps, detections, img = detection
        self.fps_lineEdit.setText("{:.1f}".format(fps))
        self.update_frame(img)
        self.draw_rectangles(detections)
        self.repaint()

    def draw_rectangles(self, detections):
        painter = QtGui.QPainter()
        painter.begin(self.img)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('#66ff66'))
        pen.setWidthF(5.)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform , True)        
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.LosslessImageRendering, True)
        painter.setPen(pen)
        font = QtGui.QFont()
        #font.setWeight(1)
        font.setPixelSize(30)
        painter.setFont(font)
        for i in detections:
            print(i)

            name,accuracy,dist, pos = i
            dist =0
            x,y,w,h = pos
            text = name+" "+accuracy+" "+"{:.2f} m".format(dist)
            painter.drawText(x-w/2,y-h/2-painter.fontMetrics().height(), text)
            painter.drawRect(x-w/2,y-h/2,w,h)
        painter.end()

    def update_frame(self, img):
        if self.client == True:
            self.img.loadFromData(img)
        else:
            self.img = self.logo.copy()



    def start_telemetry(self):
        pass