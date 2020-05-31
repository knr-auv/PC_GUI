from PyQt5 import QtWidgets, QtCore, QtGui
from math import radians
from .connectionBar_ui import Ui_connectionBar


class connectionBar(QtWidgets.QWidget,Ui_connectionBar):
    sendData = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)       
       self.timer = QtCore.QTimer(self)
       #self.b_connect.pressed.connect(self.b_connectAction)         
       #self.setStyleSheet(open('./style/connectionBar.css').read())
       self.w_batt.paintEvent = self.pEvent
       self.w_batt.repaint()
       self.batt_percentage = 1
       self.voltage = 16
       self.w_batt.setMaximumWidth(100)
       #self.w_batt.hide()
       #self.w_batt.setStyleSheet("background-color: black;")
       self.atimer = QtCore.QTimer()
       self.atimer.timeout.connect(self.a)
       self.atimer.start(50)

    def a(self):
        def map(input,in_min,in_max,out_min,out_max):
            return (input-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
        self.voltage-=0.01
        self.batt_percentage = map(self.voltage,9,16,0,1)
        if self.voltage <=9:
            self.voltage =16
        
        self.repaint()

    def pEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self.w_batt)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        width = painter.device().width()
        height = painter.device().height()
        leftTop = QtCore.QPointF(2,2)
        rightBottom = QtCore.QPoint(width -10, height-2)

        contour = QtGui.QPainterPath()
        contourRadius = 2
        contour.moveTo(leftTop.x()+contourRadius, leftTop.y())
        r = QtCore.QRectF(leftTop,QtCore.QSizeF(contourRadius, contourRadius))
        contour.arcTo(r,90,90)
        contour.lineTo(leftTop.x(), rightBottom.y()-contourRadius)
        r = QtCore.QRectF(QtCore.QPointF(leftTop.x(), rightBottom.y()-contourRadius),QtCore.QSizeF(contourRadius, contourRadius))
        contour.arcTo(r,180,90)
        contour.lineTo(rightBottom.x()-contourRadius, rightBottom.y())
        r = QtCore.QRectF(QtCore.QPointF(rightBottom.x()-contourRadius, rightBottom.y()-contourRadius),QtCore.QSizeF(contourRadius, contourRadius))
        contour.arcTo(r,270,90)
        contour.lineTo(rightBottom.x(),height/2+5)
        contour.lineTo(rightBottom.x()+5,height/2+5)
        contour.lineTo(rightBottom.x()+5,height/2-5)
        contour.lineTo(rightBottom.x(),height/2-5)
        contour.lineTo(rightBottom.x(),leftTop.y()+contourRadius)
        r = QtCore.QRectF(QtCore.QPointF(rightBottom.x()-contourRadius, leftTop.y()),QtCore.QSizeF(contourRadius, contourRadius))
        contour.arcTo(r,360,90)
        contour.lineTo(leftTop.x()+contourRadius,leftTop.y())

        contourRect = contour.controlPointRect()
        r=QtCore.QRectF(contourRect.x(),contourRect.y(),contourRect.width()*self.batt_percentage, contourRect.height())
        battArea = QtGui.QPainterPath()
        battArea.addRect(r)
        battArea = contour.intersected(battArea)        

        brush = QtGui.QBrush()
        pen = QtGui.QPen()
        color = QtGui.QColor()
        color.setRgbF(1-self.batt_percentage/2, self.batt_percentage,0,1.)
        brush.setColor(color)
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.fillPath(battArea,brush)

        pen.setWidthF(1)
        painter.setPen(pen)
        painter.drawPath(battArea)

        pen.setWidthF(2)
        painter.setPen(pen)
        painter.drawPath(contour)

        painter.setFont(QtGui.QFont('roboto'))
        text = '{:.2f}'.format(self.voltage)+' V'
        painter.drawText(width/2-painter.fontMetrics().width(text)/2, height/2 + (painter.fontMetrics().height())/3, text)
        painter.end()

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
