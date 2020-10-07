from PyQt5 import QtWidgets, QtCore, QtGui
import math
class expo_plot(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self,parent)
        sizePolicy = QtWidgets.QSizePolicy()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setWidthForHeight(True)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(200,200)
        self.setMaximumSize(200,200)
        self.data = []
        self.points = 100
        for i in range(-self.points,self.points+1):
            self.data.append(QtCore.QPointF(i,self.points*self.expo(i,self.points,2.)))
        self.expo_pen = QtGui.QPen()
        self.linear_pen = QtGui.QPen()
        self.box_pen = QtGui.QPen()

        self.box_pen.setWidthF(0.5)
        self.expo_pen.setWidthF(1.5)
        self.linear_pen.setWidthF(1.)

        self.linear_pen.setColor(QtGui.QColor("green"))
        self.expo_pen.setColor(QtGui.QColor("blue"))
    def map(self,input,in_min,in_max,out_min,out_max):
            return (input-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

    def adjustData(self):
        ret =[]
        for i in self.data:
            ret.append(QtCore.QPointF(self.map(i.x(),-self.points, self.points,self.width(), 0),self.map(i.y(),-self.points, self.points,0, self.height())))
        return ret

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        adjustedData = self.adjustData()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        leftBottom = QtCore.QPointF(0, painter.device().size().height())
        rightTop = QtCore.QPointF(painter.device().size().width(), 0)
        xCenter = rightTop.x()/2
        yCenter = leftBottom.y()/2
        device = QtCore.QRectF(leftBottom, rightTop)
        painter.setPen(self.box_pen)
        painter.drawRect(device)
        painter.drawLine(xCenter, 0,xCenter, leftBottom.y())
        painter.drawLine(0,yCenter, rightTop.x(),yCenter)
        painter.setPen(self.linear_pen)
        painter.drawLine(leftBottom, rightTop)
        painter.setPen(self.expo_pen)
        painter.drawPolyline(*(adjustedData))
        painter.end()

    def expo(self, input, out_max, index):
        return math.copysign(1,input)*(pow(abs(input), index)/pow(out_max, index))

    def update(self, arg):
        ret =[]
        for i in range(-self.points,self.points+1):
            ret.append(QtCore.QPointF(i,self.points*self.expo(i,self.points,arg)))
        self.data = ret
        self.repaint()