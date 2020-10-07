from PyQt5 import QtWidgets, QtCore, QtGui
from .controlSettings_ui import Ui_controlSettings
import numpy as np
import math, threading
import json
from tools.Control.pad import *
from tools.Control.keyboard import *
from tools.autonomyStream import autonomyStream
from widgets.controlSettings.autonomy import autonomyWidget
from widgets.controlSettings.keyboard import keyboard_widget
from widgets.controlSettings.expo_plot import expo_plot

class controlSettings(QtWidgets.QWidget,Ui_controlSettings):
    armSignal = QtCore.pyqtSignal(object)
    disarmSignal = QtCore.pyqtSignal()
    escapeClicked = QtCore.pyqtSignal()
    odroidClient = None
    threadpool = None
    padConnected = False

    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)
       self.lock = threading.Lock()
       self.b_arm.clicked.connect(self.arm)
       self.armTimeout = QtCore.QTimer()
       self.controlTimer = QtCore.QTimer()
       self.expo_plot = expo_plot(self)
       self.verticalLayout.insertWidget(2,self.expo_plot)
       
       self.keyboard_widget = keyboard_widget(self)
       self.autonomy_widget =autonomyWidget(self)
       self.vSpacer = QtWidgets.QSpacerItem(0,0,QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
       self.verticalLayout.insertItem(3, self.vSpacer)
       self.verticalLayout.insertWidget(1,self.keyboard_widget)
       self.verticalLayout.insertWidget(1,self.autonomy_widget)
       self.s_control.activated.connect(self.manage_control)
       self.b_refresh.clicked.connect(lambda: self.manage_control(1))
       self.b_start.clicked.connect(self.startCtr)
       self.b_arm.setEnabled(False)
       self.e_pitch.valueChanged.connect(self.expo_plot.update)
       self.e_yaw.valueChanged.connect(self.expo_plot.update)
       self.e_roll.valueChanged.connect(self.expo_plot.update)
       self.e_vertical.valueChanged.connect(self.expo_plot.update)
       self.e_throttle.valueChanged.connect(self.expo_plot.update)
       self.manage_control(1)
       self.controlStarted = False
       self.mode_btn.clicked.connect(lambda: self.odroidClient.setMode(self.mode_box.currentIndex()))
       self.mode_btn.setEnabled(False)

    def detectDevice(self):
        self.padConnected =  padSteering.checkDevice()

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
        self.getData_callback.connect(lambda arg: self.odroidClient.sendInput(arg))
        self.b_arm.clicked.connect(self.disarmSignal.emit)
        self.odroidConnected = True

    #stuff todo after receiving disarm acknowledge or timeout
    def disarmed(self):
        #self.b_arm.setEnabled(True)
        self.b_arm.disconnect()
        self.b_arm.clicked.connect(self.arm)
        self.b_arm.setText("Arm")
        self.stopCtr()
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
        self.padSpec.hide()
        self.expo_plot.hide()
        self.keyboard_widget.hide()
        self.autonomy_widget.hide()
        self.l_interval.show()
        self.label_13.show()
        if self.s_control.currentText()=="Keyboard":
            self.vSpacer.changeSize(0,0,QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
            self.keyboard_widget.setFocus()
            self.keyboard_widget.show()
            self.b_start.setEnabled(True)
            
            pass
        elif self.s_control.currentText()=="Pad":
            self.detectDevice()

            self.vSpacer.changeSize(0,0,QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

            if not self.padConnected:
               self.b_start.setEnabled(False)
               self.w_pad_select.show()
               self.l_padStatus.setText("Device not detected")
            else:
                self.w_pad_select.hide()
                self.b_start.setEnabled(True)
            self.padSpec.show()
            self.expo_plot.show()
            pass
        elif self.s_control.currentText()=="Autonomy":
            self.vSpacer.changeSize(0,0,QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
       
            self.l_interval.hide()
            self.label_13.hide()
            self.b_start.setEnabled(True)
            self.autonomy_widget.show()
            #self.
        if not self.odroidClient:
            self.b_start.setEnabled(False)
    getData_callback = QtCore.pyqtSignal(object)
    def startCtr(self):
        self.s_control.setEnabled(False)

        if self.s_control.currentText() == "Keyboard":
            self.control = Keyboard()
            self.keyboard_widget.disableButtons()
            self.controlStarted = True
            self.control.setKeyAssignment(self.keyboard_widget.key_assignment)
            self.control.setConfig(self.keyboard_widget.getConfig())
            self.control.getData_callback = self.getData_callback 
            self.keyboard_widget.configChanged.connect(self.control.setConfig)
            self.control.escapeClicked.connect(self.escapeClicked)
            self.control.start_control()
            logging.debug("Keyboard controll started")

        if self.s_control.currentText() == "Pad":
            self.control=padSteering(self.get_config())
            self.controlStarted = True
            self.control.getData_callback = self.getData_callback 
            self.threadpool.start(self.control)

        if self.s_control.currentText()=="Autonomy":
            self.controlStarted = True
            self.odroidClient.startAutonomy()
            self.detectionStream = autonomyStream(port = 6969)
            self.threadpool.start(self.detectionStream)
            self.autonomy_widget.client = True
            self.detectionStream.signals.newDetection.connect(lambda x:self.autonomy_widget.menage_detection(x))
            self.b_start.hide()
            self.b_arm.setEnabled(True)
            logging.debug("detection tream started")
            return

        #common stuff for each controller except autonomy...
        self.b_start.hide()
        self.b_arm.setEnabled(True)
        self.controlTimer.setInterval(int(self.l_interval.text()))
        self.controlTimer.timeout.connect(self.control.get_data)
        self.controlTimer.start()

    def stopCtr(self):
        if self.controlStarted==False:
            return
        self.s_control.setEnabled(True)
        if self.s_control.currentText()=="Keyboard":
            self.keyboard_widget.saveConfig()
            #self.keyPressEvent = self.memKP
            #self.keyReleaseEvent = self.memKR
            #self.releaseKeyboard()
            self.control.stop_control()
            self.keyboard_widget.enableButtons()
            try:
                self.keyboard_widget.configChanged.disconnect()
            except TypeError:
                pass

        elif self.s_control.currentText()=="Pad":
            self.control.active = False
        elif self.s_control.currentText()=="Autonomy":
            self.odroidClient.stopAutonomy()
            self.b_start.show()
            self.b_arm.setEnabled(False)
            self.detectionStream.signals.newDetection.disconnect()
            self.detectionStream.stop()
            
            return
        #common stuff for each controller except autonomy...

        self.controlTimer.stop()
        try:
            self.controlTimer.timeout.disconnect()
        except TypeError:
            pass
        self.b_start.show()
        self.b_arm.setEnabled(False)


       

       
       


