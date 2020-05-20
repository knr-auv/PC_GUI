from PyQt5 import QtWidgets, QtCore, QtGui
from .controlSettings_ui import Ui_controlSettings
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
import math, threading
from tools.pad import *

class controlSettings(QtWidgets.QWidget,Ui_controlSettings):
    armSignal = QtCore.pyqtSignal(object)
    disarmSignal = QtCore.pyqtSignal()

    odroidClient = None
    threadpool = None

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)   
       self.lock = threading.Lock()
       self.b_arm.clicked.connect(self.arm)
       self.armTimeout = QtCore.QTimer()
       self.controlTimer = QtCore.QTimer()
       self.expo_plot = expo_plot()
       self.expo_plot.setObjectName("expo_plot")
       self.verticalLayout.addWidget(self.expo_plot)
       self.keyboard_widget = keyboard_widget()
       self.verticalLayout.addWidget(self.keyboard_widget)
       self.s_control.activated.connect(self.manage_control)
       self.b_start.clicked.connect(self.start_keyboard)
       self.b_arm.setEnabled(False)
       self.e_pitch.valueChanged.connect(self.expo_plot.update)
       self.e_yaw.valueChanged.connect(self.expo_plot.update)
       self.e_roll.valueChanged.connect(self.expo_plot.update)
       self.e_vertical.valueChanged.connect(self.expo_plot.update)
       self.e_throttle.valueChanged.connect(self.expo_plot.update)

       self.manage_control(1)

    def get_config(self):
        config={'pad_deadzone':int(self.e_deadzone.text()),
                'roll_expo': float(self.e_roll.text().replace(',','.')),
                'pitch_expo': float(self.e_pitch.text().replace(',','.')),
                'throttle_expo':float(self.e_throttle.text().replace(',','.')),
                'yaw_expo':float(self.e_yaw.text().replace(',','.')),
                'vertical_expo':float(self.e_vertical.text().replace(',','.')),
                'max_roll': int(self.l_roll.text().replace('°','')),
                'max_pitch':int(self.l_pitch.text().replace('°','')),
                'max_vertical':int(self.l_vertical.text()),
                'max_throttle':int(self.l_throttle.text()),
                'max_yaw':int(self.l_yaw.text())}
        return config

    def arm(self):
        self.b_arm.setEnabled(False)
        self.b_arm.setText("Arming")
        self.armSignal.emit(int(self.l_PIDInterval.text()))
        self.armTimeout.setSingleShot(True)
        self.armTimeout.timeout.connect(self.disarmed)
        self.armTimeout.start(3000)

    #stuff todo after receiving arm acknowledge
    def armed(self):
        self.armTimeout.stop()
        self.b_arm.setEnabled(True)
        self.b_arm.setText("Disarm")
        self.b_arm.disconnect()
        self.b_arm.clicked.connect(self.disarmSignal.emit)
        self.odroidConnected = True
        self.keyboard_widget.getData_callback.connect(lambda arg: self.odroidClient.sendPad(arg))
        #self.control.signals.getData_callback.connect(lambda arg: self.odroidClient.sendPad(arg))

    #stuff todo after receiving disarm acknowledge or timeout
    def disarmed(self):
        self.b_arm.setEnabled(True)
        self.b_arm.disconnect()
        self.b_arm.clicked.connect(self.arm)
        self.b_arm.setText("Arm")
        if self.padIsRunning:
            self.stop_pad()
        #handling pad control thread. TODO make a class capable of selecting control methods
    def connectSettings(self):
       self.e_pitch.valueChanged.connect(self.update_config)
       self.e_yaw.valueChanged.connect(self.update_config)
       self.e_roll.valueChanged.connect(self.update_config)
       self.e_vertical.valueChanged.connect(self.update_config)
       self.e_throttle.valueChanged.connect(self.update_config)
       self.l_pitch.valueChanged.connect(self.update_config)
       self.l_yaw.valueChanged.connect(self.update_config)
       self.l_roll.valueChanged.connect(self.update_config)
       self.l_vertical.valueChanged.connect(self.update_config)
       self.l_throttle.valueChanged.connect(self.update_config)

    def disconnectSettings(self):
       self.e_pitch.valueChanged.disconnect()
       self.e_yaw.valueChanged.disconnect()
       self.e_roll.valueChanged.disconnect()
       self.e_vertical.valueChanged.disconnect()
       self.e_throttle.valueChanged.disconnect()
       self.l_pitch.valueChanged.disconnect()
       self.l_yaw.valueChanged.disconnect()
       self.l_roll.valueChanged.disconnect()
       self.l_vertical.valueChanged.disconnect()
       self.l_throttle.valueChanged.disconnect()

    def update_config(self):
        with self.lock:
            self.control.config=self.get_config()
    
    def manage_control(self, x):
        if self.s_control.currentText()=="Keyboard":
            self.keyboard_widget.setFocus()
            self.keyboard_widget.show()
            self.padSpec.hide()
            self.expo_plot.hide()
            pass
        if self.s_control.currentText()=="Pad":
            self.keyboard_widget.hide()
            self.padSpec.show()
            self.expo_plot.show()
            pass

    def start_keyboard(self):
        logging.debug("starting keyboard control")
        self.b_start.hide()
        self.b_arm.setEnabled(True)
        self.controlTimer.setInterval(int(self.l_interval.text()))
        self.controlTimer.timeout.connect(self.keyboard_widget.get_data)
        self.controlTimer.start()

    def stop_keyboard(self):
        self.b_start.show()
        self.controlTimer.stop()
        self.controlTimer.timeout.disconnect()
        self.b_start.show()
        self.b_arm.setEnabled(False)

    def start_pad(self):
        print("starting pad stuff")
        self.b_start.hide()
        config = self.get_config()
        self.control = PadSteering(config)
        self.padIsRunning = False
        self.threadpool.start(self.control)
        self.connectSettings()
        self.b_arm.setEnabled(True)
        self.controlTimer.setInterval(int(self.l_interval.text()))
        self.controlTimer.timeout.connect(self.control.get_data)
        self.controlTimer.start()
        self.padIsRunning = True


    def stop_pad(self):
        self.padIsRunning = False
        #print(self.controlTimer.receivers(self.controlTimer.timeout))
        self.controlTimer.stop()
        self.controlTimer.timeout.disconnect()
        self.disconnectSettings()
        self.b_start.show()
        self.b_arm.setEnabled(False)
        self.control.active = False

class keyboard_widget(QtWidgets.QWidget):
    getData_callback = QtCore.pyqtSignal(object)

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       mainLayout= QtWidgets.QVBoxLayout()
       joystickLayout = QtWidgets.QHBoxLayout()
       joystick_l_Layout = QtWidgets.QVBoxLayout()
       self.l1 = QtWidgets.QLabel(parent)
       self.l2 = QtWidgets.QLabel(parent)
       self.jb = pg.JoystickButton()
       self.jb.setFixedWidth(200)
       self.jb.setFixedHeight(200)
       #self.setStyleSheet("background-color: green;")
       font = QtGui.QFont()
       font.setPointSize(15)
       self.l1.setFont(font)
       self.l2.setFont(font)
       joystickLayout.addWidget(self.jb)
       joystick_l_Layout.addWidget(self.l1)
       joystick_l_Layout.addWidget(self.l2)
       self.l1.setMaximumSize(QtCore.QSize(16777215, 95))
       self.l2.setMaximumSize(QtCore.QSize(16777215, 95))
       self.l1.setText("  X :")
       self.l2.setText("  Y :")
       self.output = {"vertical": 0, 'roll':0, 'pitch':0, "yaw":0, "throttle":0}
       self.key_assignment ={"forward":0,
                             "backward":0,
                             "roll":0,
                             "pitch":0,
                             "left":0,
                             "right":0,
                             "up":QtCore.Qt.Key_W,
                             "down":QtCore.Qt.Key_S
                             }
       self.key_mem = {QtCore.Qt.Key_W:0, QtCore.Qt.Key_S:0}
       joystickLayout.addLayout(joystick_l_Layout)
       #keeping focus while using arrows...
       for child in self.findChildren(QtGui.QWidget):
                child.setFocusPolicy(QtCore.Qt.NoFocus)
       self.x = 0
       self.y = 0

       self.setLayout(mainLayout)
       mainLayout.addLayout(joystickLayout)


    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            self.key_mem[event.key()] = True

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.key_mem[event.key()] = False

    def get_data(self):
       self.x, self.y = self.jb.getState()
       self.x *=300
       self.y *= 800
       self.output["throttle"] = self.y
       self.output["yaw"]= self.x
       try:
           if self.key_mem[self.key_assignment["up"]] == True:
               self.output["vertical"]+=10
           if self.key_mem[self.key_assignment["down"]] == True:
              self.output["vertical"]-=10
           if self.key_mem[self.key_assignment["down"]] == False and self.key_mem[self.key_assignment["up"]] == False:
               self.output["vertical"]*=-0.7
       except KeyError:
           self.output["vertical"] = 0
       self.l1.setText("  X : %.2f" %self.x)
       self.l2.setText("  Y : %.2f" %self.y)

       self.getData_callback.emit([self.output["roll"],self.output["pitch"],int(self.output["yaw"]),int(self.output["vertical"]),int(self.output["throttle"])])

class expo_plot(pg.PlotWidget):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setBackground("w")
        self.x= list(np.arange(-1,1,0.01))
        self.y= self.calculate_expo(2)
        
        expo_pen = pg.mkPen(color = (0,255,0), width = 2)
        linear_pen = pg.mkPen(color = (0,0,255), width = 2)
        self.addLine(y=0)
        self.addLine(x=0)
       # self.setLimits(xMin=-1, xMax=1,
       #          minXRange=2, maxXRange=2, 
        #         yMin=-1, yMax=1,
         #        minYRange=2, maxYRange=2)
        self.setMouseEnabled(x = False, y = False)
        self.enableAutoRange()
        self.setMenuEnabled(enableMenu = False)
        self.hideButtons()
        self.linear_plot = self.plot(self.x,self.x,pen = linear_pen)
        self.expo_plot = self.plot(self.x, self.y, pen = expo_pen)

    def expo(self, input, out_max, index):
        return math.copysign(1,input)*(pow(abs(input), index)/pow(out_max, index))

    def calculate_expo(self,index):
        ret=[]
        for a in range(-100,100):
            if a ==0:
                ret.append(0)
            else:
                ret.append(self.expo(a/100,1,index))
        return ret
    def update(self, arg):
        self. y =self.calculate_expo(arg)
        self.expo_plot.setData(self.x, self.y)