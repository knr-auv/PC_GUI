from PyQt5 import QtWidgets, QtCore, QtGui
import time
from random import *
from math import *
def map(input,in_min,in_max,out_min,out_max):
        return (input-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
#on windows changin pyqtgraph/ptimes.py systime.clock() to systime.process_time() is necesary
class plotDepth(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        #QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.time = [] 
        self.depth_data = []

        self.marginTop = 9
        self.marginBottom = 9
        self.marginLeft = 5
        self.marginRight = 5
        self.textSpacer = 30

        self.legend_x = 80
        self.legend_y = 50
        self.legend_width = 80
        self.legend_height =30

        self.minValue = 0
        self.maxValue = 2
        self.yRange =2


        self.depth_pen = QtGui.QPen()
        self.line_pen = QtGui.QPen()
        self.grid_pen = QtGui.QPen()

        self.depth_pen.setColor(QtGui.QColor('black'))
        self.line_pen.setColor(QtGui.QColor(153,255,51,255))
        self.grid_pen.setColor(QtGui.QColor("gray"))

        self.line_pen.setWidthF(1.5)
        self.grid_pen.setWidthF(0.5)
        self.depth_pen.setWidthF(2.)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        try:
            depth = self.adjustData(self.time, self.depth_data)
            self.paintGrid(painter)
           

            painter.begin(self)
            painter.setPen(self.depth_pen)
            painter.drawPolyline(*(depth))
            painter.end()
            
        except:
            painter.end()
        self.drawLegend(self.legend_x, self.legend_y,self.legend_width,self.legend_height, painter)

    def adjustData(self, time, data):
        maxValue = 0
        minValue = 0
        adjustedData = []
        adjustedTime =[]
        for i in data:
            if i > maxValue:
                maxValue = i
            if i <minValue:
                minValue = i
            if minValue == maxValue:
                minValue =0
                maxValue = 2
        if maxValue<self.maxValue:
            maxValue = self.maxValue
        self.minValue = minValue
        self.maxValue = maxValue
        for i in range(len(data)):
            adjustedData.append(QtCore.QPointF(map(time[i], time[0], time[len(time)-1],self.marginLeft+self.textSpacer,self.width()-self.marginRight),map(data[i],self.minValue, self.maxValue,self.marginTop, self.height()-self.marginBottom)))
        return adjustedData
        
    pressed = False
    pX=0
    pY=0

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            if event.x()>=self.legend_x-self.legend_width/2 and event.x()<=self.legend_x+self.legend_width/2 and event.y()>=self.legend_y-self.legend_height/2 and event.y()<=self.legend_y+self.legend_height/2:
                self.pressed = True
                self.pX=event.x()
                self.pY=event.y()
            return
        
    def mouseMoveEvent(self, event):
        if not self.pressed:
            return
        self.legend_x -=self.pX-event.x()
        self.legend_y -= self.pY-event.y()
        self.pX = event.x()
        self.pY = event.y()
        self.repaint()

    def mouseReleaseEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.pressed = False
            return

    def drawLegend(self,centerX,centerY, width,height,painter):
        painter.begin(self)
        rect = QtGui.QPainterPath()
        rect.addRoundedRect(QtCore.QRectF(centerX-width/2, centerY-height/2, width, height),5,5)
        painter.fillPath(rect, QtGui.QColor(0, 0, 0, int(127)))
        text = 'Depth'
        painter.drawText(centerX,centerY+painter.fontMetrics().height()/3,text)
        spaceLeft= 5
        spaceRight = 5
        painter.setPen(self.depth_pen)
        painter.drawLine(centerX - width/2+spaceLeft, centerY,centerX-spaceRight,centerY)
        painter.end()

    def paintGrid(self, painter):
        painter.begin(self)
        painter.setPen(self.grid_pen)
        a = 25
        for i in range(self.minValue, int(self.maxValue*50)+a):
            if i%a ==0:
              
                h=map(i/50,self.minValue, self.maxValue,self.marginTop,self.height()-self.marginBottom)
                text = '{:.1F}'.format(i/50)+'m'
                painter.drawText(self.marginLeft, h + (painter.fontMetrics().height())/3, text)
                painter.drawLine(self.marginLeft+self.textSpacer,h,self.width()-self.marginRight,h)
        painter.setPen(self.line_pen)
        #middle = map(0,self.minValue, self.maxValue,self.marginTop,self.height()-self.marginBottom)
        #painter.drawLine(self.textSpacer,middle, self.width(), middle)
        painter.end()

class plot(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.time = [] 
        self.roll_data = []
        self.pitch_data = []
        self.yaw_data = []
        self.setMinimumSize(500,200)

        self.marginTop = 9
        self.marginBottom = 9
        self.marginLeft = 5
        self.marginRight = 5
        self.textSpacer = 30


        self.legend_x = 80
        self.legend_y = 50
        self.legend_width = 80
        self.legend_height =60

        self.minValue = 10
        self.maxValue = 10
        self.yRange =10

        self.line_pen = QtGui.QPen()
        self.grid_pen = QtGui.QPen()
        self.roll_pen = QtGui.QPen()
        self.pitch_pen = QtGui.QPen()
        self.yaw_pen = QtGui.QPen()

        self.line_pen.setColor(QtGui.QColor(153,255,51,255))
        self.grid_pen.setColor(QtGui.QColor("gray"))
        self.roll_pen.setColor(QtGui.QColor('red'))
        self.pitch_pen.setColor(QtGui.QColor('green'))
        self.yaw_pen.setColor(QtGui.QColor('blue'))

        self.line_pen.setWidthF(1.5)
        self.grid_pen.setWidthF(0.5)
        self.roll_pen.setWidthF(2)
        self.yaw_pen.setWidthF(2)
        self.pitch_pen.setWidthF(2)
        self.repaint()

    def adjustData(self, time, roll, pitch, yaw):
        adjustedTime = []
        adjustedRoll = []
        adjustedPitch = []
        adjustedYaw = []
        maxValue = 0
        minValue = 0
        for i in roll:
            if i > maxValue:
                maxValue = i
            if i <minValue:
                minValue = i
        for i in pitch:
            if i > maxValue:
                maxValue = i
            if i <minValue:
                minValue = i
        for i in yaw:
            if i > maxValue:
                maxValue = i
            if i <minValue:
                minValue = i
        if minValue==maxValue:
            minValue = -10
            maxValue =10
        self.minValue=min(minValue, - self.yRange)
        self.maxValue  = max(maxValue, self.yRange)
        for i in time:
            adjustedTime.append(map(i, time[0], time[len(time)-1],self.marginLeft+self.textSpacer,self.width()-self.marginRight))
        for i in range(len(roll)):
            adjustedRoll.append(QtCore.QPointF(adjustedTime[i],map(roll[i],self.minValue, self.maxValue, self.height()-self.marginBottom,self.marginTop)))
        for i in range(len(pitch)):
            adjustedPitch.append(QtCore.QPointF(adjustedTime[i],map(pitch[i],self.minValue, self.maxValue, self.height()-self.marginBottom,self.marginTop)))
        for i in range(len(yaw)):
            adjustedYaw.append(QtCore.QPointF(adjustedTime[i],map(yaw[i],self.minValue, self.maxValue, self.height()-self.marginBottom,self.marginTop)))
        
        return adjustedRoll, adjustedPitch, adjustedYaw
    pressed = False
    pX=0
    pY=0
    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            if event.x()>=self.legend_x-self.legend_width/2 and event.x()<=self.legend_x+self.legend_width/2 and event.y()>=self.legend_y-self.legend_height/2 and event.y()<=self.legend_y+self.legend_height/2:
                self.pressed = True
                self.pX=event.x()
                self.pY=event.y()
            return
        
    def mouseMoveEvent(self, event):
        if not self.pressed:
            return
        self.legend_x -=self.pX-event.x()
        self.legend_y -= self.pY-event.y()
        self.pX = event.x()
        self.pY = event.y()
        self.repaint()

    def mouseReleaseEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.pressed = False
            return
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()         
        try:
            roll, pitch, yaw = self.adjustData(self.time,self.roll_data, self.pitch_data, self.yaw_data)
            self.paintGrid(painter)
            painter.begin(self)
            painter.setRenderHint(painter.Antialiasing, True)
            painter.setPen(self.roll_pen)
            painter.drawPolyline(*(roll))
            painter.setPen(self.pitch_pen)
            painter.drawPolyline(*(pitch))
            painter.setPen(self.yaw_pen)
            painter.drawPolyline(*(yaw))
            painter.end()

        except:
            painter.end()
        self.drawLegend(self.legend_x, self.legend_y,self.legend_width,self.legend_height,painter)
          
    def drawLegend(self,centerX,centerY, width,height,painter):
        painter.begin(self)
        rect = QtGui.QPainterPath()
        rect.addRoundedRect(QtCore.QRectF(centerX-width/2, centerY-height/2, width, height),5,5)
        painter.fillPath(rect, QtGui.QColor(0, 0, 0, int(127)))
        text = 'Roll'
        painter.drawText(centerX,centerY-height/3+painter.fontMetrics().height()/3 ,text)
        text = 'Pitch'
        painter.drawText(centerX,centerY+painter.fontMetrics().height()/3,text)
        text = 'Yaw'
        painter.drawText(centerX,centerY+height/3+painter.fontMetrics().height()/3,text)
        spaceLeft= 5
        spaceRight = 5
        painter.setPen(self.roll_pen)
        painter.drawLine(centerX - width/2+spaceLeft, centerY-height/3,centerX-spaceRight,centerY-height/3)
        painter.setPen(self.pitch_pen)
        painter.drawLine(centerX - width/2+spaceLeft, centerY,centerX-spaceRight,centerY)
        painter.setPen(self.yaw_pen)
        painter.drawLine(centerX - width/2+spaceLeft, centerY+height/3,centerX-spaceRight,centerY+height/3)
        painter.end()

    def paintGrid(self, painter):
        painter.begin(self)
        painter.setPen(self.grid_pen)
        #painter.setRenderHint(painter.Antialiasing, True)
        maxx = max(-self.minValue, self.maxValue)
        if maxx<15:
            a=5
        elif maxx<30:
            a = 10
        elif maxx<60:
            a=15
        elif maxx < 180:
            a=30
        for i in range(int(self.minValue)-a, int(self.maxValue)+a):
            if i%a ==0:
                h=map(i,self.minValue, self.maxValue,self.height()-self.marginBottom,self.marginTop)
                text = '{:d}'.format(i)+'°'
                painter.drawText(self.marginLeft, h + (painter.fontMetrics().height())/3, text)
                painter.drawLine(self.marginLeft+self.textSpacer,h,self.width()-self.marginRight,h)
        painter.setPen(self.line_pen)
        middle = map(0,self.minValue, self.maxValue,self.height()-self.marginBottom,self.marginTop)
        painter.drawLine(self.textSpacer,middle, self.width(), middle)
        painter.end()

class IMUGraph(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(IMUGraph, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout()
        self.plot = plot(self)
        self.plotDepth = plotDepth()
        self.plotDepth.setMaximumHeight(200)
        spacer = QtWidgets.QSpacerItem(0, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addWidget(self.plot)
        layout.addItem(spacer)
        layout.addWidget(self.plotDepth)
        self.setLayout(layout)
        self.start_time = time.time()
        self.repaint()
        self.plot.repaint()
    def update(self, arg):
        if len(self.plot.time) > 1000:
            self.plot.time = self.plot.time[1:]
            self.plot.time.append(time.time()-self.start_time)
            self.plotDepth.time = self.plot.time

            self.plot.roll_data = self.plot.roll_data[1:]
            self.plot.pitch_data = self.plot.pitch_data[1:]
            self.plot.yaw_data = self.plot.yaw_data[1:]
            self.plotDepth.depth_data = self.plotDepth.depth_data[1:]
            self.plot.roll_data.append(arg[0])
            self.plot.pitch_data.append(arg[1])
            self.plot.yaw_data.append(arg[2])
            self.plotDepth.depth_data.append(arg[3])
        else:
            self.plot.time.append(time.time()-self.start_time)
            self.plotDepth.time = self.plot.time
            self.plot.roll_data.append(arg[0])
            self.plot.pitch_data.append(arg[1])
            self.plot.yaw_data.append(arg[2])
            self.plotDepth.depth_data.append(arg[3])
        if self.isVisible:
            self.repaint()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = accGraph()
    main.show()
    sys.exit(app.exec_())




if __name__ == '__main__':
    main()