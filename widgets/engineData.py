
from PyQt5 import QtWidgets,QtGui,QtCore

class engineData(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(engineData,self).__init__(*args,**kwargs)
        self.resize(400,400)#set size

        self.mainlayout = QtWidgets.QVBoxLayout()
        self.englayout=QtWidgets.QHBoxLayout()
        self.pwmlayout = QtWidgets.QHBoxLayout()

        self.engines=["engine 0:","engine 1:","engine 2:","engine 3:","engine 4:"]
        self.pwm=["","","","",""]

        # just for test (random number) !!!!!!!!!!!!!!
        pwm=[12,35,47,90,60]
        self.update(pwm)

        for n in range(len(self.engines)):
            label=QtWidgets.QLabel(str(self.engines[n]))
            pom="PWM: "+str(self.pwm[n])+"%"
            pwmlabel=QtWidgets.QLabel(pom)
            self.pwmlayout.addWidget((pwmlabel))
            self.englayout.addWidget(label)

        self.mainlayout.addLayout(self.englayout)
        self.mainlayout.addLayout(self.pwmlayout)

        self.model=QtWidgets.QLabel()
        self.model.setPixmap(QtGui.QPixmap("./img/engines.jpg"))
        self.model.setScaledContents(True)
        self.mainlayout.addWidget(self.model)
        self.setLayout(self.mainlayout)

        #engine numbering
        #engine0
        self.draw_engine_line(50,155,90,155)
        self.model_text(33,160,0)
        self.progressbar(5, 175, int(self.pwm[0]))
        #engine1
        self.draw_engine_line(310,155,350,155)
        self.model_text(355,160,1)
        self.progressbar(328,175, int(self.pwm[1]))
        #engine 2
        self.draw_engine_line(65,48,110,105)
        self.model_text(50,50,2)
        self.progressbar(5, 70, int(self.pwm[2]))
        #engine 3
        self.draw_engine_line(200,370,250,370)
        self.model_text(260,380,3)
        self.progressbar(280, 365, int(self.pwm[3]))
        #engine4
        self.draw_engine_line(290,105,335,48)
        self.model_text(340,53,4)
        self.progressbar(328,70,int(self.pwm[4]))

    def draw_engine_line(self,x1,y1,x2,y2):
        painter=QtGui.QPainter(self.model.pixmap())
        pen=QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)
        painter.drawLine(x1,y1,x2,y2)
        painter.end()

    def model_text(self,x,y,label):
        painter = QtGui.QPainter(self.model.pixmap())
        pen=QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)
        font=QtGui.QFont()
        font.setFamily("Times")
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(x,y,str(label))
        painter.end()

    def progressbar(self,x,y,pwm):
        painter = QtGui.QPainter(self.model.pixmap())
        # background parameters
        width=70
        height=15
        #black background
        brush=QtGui.QBrush()
        brush.setColor((QtGui.QColor("black")))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect=QtCore.QRect(x,y,width,height)
        painter.fillRect(rect,brush)
        #green progressbar
        #progressbar parameters
        pheight=int(0.8*height)
        pwidth=int(pwm/100*(width-5))
        brush = QtGui.QBrush()
        brush.setColor((QtGui.QColor("green")))
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect=QtCore.QRect(x+2.5,y+int(0.1*height),pwidth,pheight)
        painter.fillRect(rect, brush)
        painter.end()

    def update(self,pwm):  ## variable pwm must be a list of filling individual PWM
        #sequence must be the same as the setting of the engines in the picture
        for i in range(5):
            self.pwm[i]+=str(pwm[i])

   



#import sys
#app=QtWidgets.QApplication(sys.argv)
#window=engineData()
#window.show()
#app.exec_()