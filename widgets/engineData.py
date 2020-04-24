from PyQt5 import QtWidgets,QtGui,QtCore

class engineData(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(engineData,self).__init__(*args,**kwargs)
        self.resize(400,400)#set size

        self.mainlayout = QtWidgets.QVBoxLayout()
        self.englayout=QtWidgets.QHBoxLayout()
        self.pwmlayout=QtWidgets.QHBoxLayout()
        self.engines=["engine 0:","engine 1:","engine 2:","engine 3:","engine 4:"]
        # just for test (random number) !!!!!!!!!!!!!!
        self.pwm=[10,10,10,10,10]

        self.labele1=QtWidgets.QLabel(str(self.engines[0]))
        self.labele2=QtWidgets.QLabel(str(self.engines[1]))
        self.labele3=QtWidgets.QLabel(str(self.engines[2]))
        self.labele4=QtWidgets.QLabel(str(self.engines[3]))
        self.labele5=QtWidgets.QLabel(str(self.engines[4]))

        self.englayout.addWidget(self.labele1)
        self.englayout.addWidget(self.labele2)
        self.englayout.addWidget(self.labele3)
        self.englayout.addWidget(self.labele4)
        self.englayout.addWidget(self.labele5)

        self.labelp1=QtWidgets.QLabel("PWM: "+str(self.pwm[0])+"%")
        self.labelp2 = QtWidgets.QLabel("PWM: " + str(self.pwm[1]) + "%")
        self.labelp3 = QtWidgets.QLabel("PWM: " + str(self.pwm[2]) + "%")
        self.labelp4 = QtWidgets.QLabel("PWM: " + str(self.pwm[3]) + "%")
        self.labelp5 = QtWidgets.QLabel("PWM: " + str(self.pwm[4]) + "%")

        self.pwmlayout.addWidget(self.labelp1)
        self.pwmlayout.addWidget(self.labelp2)
        self.pwmlayout.addWidget(self.labelp3)
        self.pwmlayout.addWidget(self.labelp4)
        self.pwmlayout.addWidget(self.labelp5)

        self.mainlayout.addLayout(self.englayout)
        self.mainlayout.addLayout(self.pwmlayout)


        self.model=QtWidgets.QLabel()
        self.model.setPixmap(QtGui.QPixmap("./img/engines.jpg"))
        self.model.setScaledContents(True)
        self.mainlayout.addWidget(self.model)
        self.setLayout(self.mainlayout)

        #engine numbering
        #engine0
        self.model_text(5,168,"engine 0:")
        self.progressbar(1, 175, int(self.pwm[0]))
        #engine1
        self.model_text(335,168,"engine 1:")
        self.progressbar(330,175, int(self.pwm[1]))
        #engine 2
        self.model_text(5,63,"engine 2:")
        self.progressbar(1, 70, int(self.pwm[2]))
        #engine 3
        self.model_text(235,363,"engine 3:")
        self.progressbar(230, 370, int(self.pwm[3]))
        #engine4
        self.model_text(335,63,"engine :4")
        self.progressbar(330,70,int(self.pwm[4]))


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
        pen.setColor(QtGui.QColor("black"))
        painter.setPen(pen)
        font=QtGui.QFont()
        font.setFamily("Times")
        font.setPointSize(12)
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

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def setprogress(self,pwm):
        self.model.deleteLater()
        self.clearLayout(self.pwmlayout)
        self.labelp1 = QtWidgets.QLabel("PWM: " + str(self.pwm[0]) + "%")
        self.labelp2 = QtWidgets.QLabel("PWM: " + str(self.pwm[1]) + "%")
        self.labelp3 = QtWidgets.QLabel("PWM: " + str(self.pwm[2]) + "%")
        self.labelp4 = QtWidgets.QLabel("PWM: " + str(self.pwm[3]) + "%")
        self.labelp5 = QtWidgets.QLabel("PWM: " + str(self.pwm[4]) + "%")
        self.pwmlayout.addWidget(self.labelp1)
        self.pwmlayout.addWidget(self.labelp2)
        self.pwmlayout.addWidget(self.labelp3)
        self.pwmlayout.addWidget(self.labelp4)
        self.pwmlayout.addWidget(self.labelp5)
        self.mainlayout.removeItem(self.pwmlayout)
        self.mainlayout.addLayout(self.pwmlayout)
        self.model = QtWidgets.QLabel()
        self.model.setPixmap(QtGui.QPixmap("./img/engines.jpg"))
        self.model.setScaledContents(True)
        self.mainlayout.addWidget(self.model)
        self.setLayout(self.mainlayout)
        # engine numbering
        # engine0
        self.model_text(5, 168, "engine 0:")
        self.progressbar(1, 175, int(self.pwm[0]))
        # engine1
        self.model_text(335, 168, "engine 1:")
        self.progressbar(330, 175, int(self.pwm[1]))
        # engine 2
        self.model_text(5, 63, "engine 2:")
        self.progressbar(1, 70, int(self.pwm[2]))
        # engine 3
        self.model_text(235, 363, "engine 3:")
        self.progressbar(230, 370, int(self.pwm[3]))
        # engine4
        self.model_text(335, 63, "engine :4")
        self.progressbar(330, 70, int(self.pwm[4]))

    def update(self,pwm):  ## variable pwm must be a list of filling individual PWM
        #sequence must be the same as the setting of the engines in the picture
        for i in range(len(self.pwm)):
            self.pwm[i]=pwm[i]
        self.setprogress(self.pwm)

#import sys
#app=QtWidgets.QApplication(sys.argv)
#window=engineData()
#window.show()
#app.exec_()
