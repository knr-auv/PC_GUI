from PyQt5 import QtWidgets, QtCore
from .controlSettings_ui import Ui_controlSettings


class controlSettings(QtWidgets.QWidget,Ui_controlSettings):
    armSignal = QtCore.pyqtSignal(object)
    disarmSignal = QtCore.pyqtSignal()
    padSettings = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)
       self.setupUi(self)   
       self.b_arm.clicked.connect(self.arm)
       self.armTimeout = QtCore.QTimer()

    def arm(self):
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
        print(config)
        self.b_arm.setEnabled(False)
        self.b_arm.setText("Arming")
        self.padSettings.emit(config)
        self.armSignal.emit(30)
        self.armTimeout.setSingleShot(True)
        self.armTimeout.timeout.connect(self.disarmed)
        self.armTimeout.start(3000)

    #stuff todo after receiving arm acknowledge
    def armed(self):
        self.armTimeout.stop()
        self.b_arm.setEnabled(True)
        self.b_arm.setText("Disarm")
    #stuff todo after receiving disarm acknowledge or timeout
    def disarmed(self):
        self.b_arm.setEnabled(True)
        self.b_arm.setText("Arm")