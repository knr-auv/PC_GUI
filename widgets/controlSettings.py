from PyQt5 import QtWidgets, QtCore
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
       self.padTimer = QtCore.QTimer()
       self.expo_plot = expo_plot()
       self.expo_plot.setObjectName("expo_plot")
       self.verticalLayout.addWidget(self.expo_plot)
       config = self.get_config()
       self.control = PadSteering(config)
       self.control.setAutoDelete(False)
       self.padIsRunning = False

       self.b_start.clicked.connect(self.start_pad)
       self.b_arm.setEnabled(False)
       self.e_pitch.valueChanged.connect(self.expo_plot.update)
       self.e_yaw.valueChanged.connect(self.expo_plot.update)
       self.e_roll.valueChanged.connect(self.expo_plot.update)
       self.e_vertical.valueChanged.connect(self.expo_plot.update)
       self.e_throttle.valueChanged.connect(self.expo_plot.update)

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

        self.control.signals.getData_callback.connect(lambda arg: self.odroidClient.sendPad(arg))

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

    def start_pad(self):
        print("starting pad stuff")
        self.b_start.hide()
        self.threadpool.start(self.control)
        self.connectSettings()
        self.b_arm.setEnabled(True)
        self.padTimer.setInterval(int(self.l_interval.text()))
        self.padTimer.timeout.connect(self.control.get_data)
        self.padTimer.start()
        self.padIsRunning = True

    def stop_pad(self):
        self.padIsRunning = False
        #print(self.padTimer.receivers(self.padTimer.timeout))
        self.padTimer.stop()
        self.padTimer.timeout.disconnect()
        self.disconnectSettings()
        self.b_start.show()
        self.b_arm.setEnabled(False)
        self.control.active = False

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