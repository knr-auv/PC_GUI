# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from pidSetup_ui import Ui_pidSetup

'''
Each regulator has its own send method and send signal.
There is also update method which can be connected to a thread providing current pid settings from odroid
'''

class PID:
    def __init__(self,P=0.,I=0.,D=0.):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        
    def setKp(self,P):
        self.Kp=P
    
    def getKp(self):
        return self.Kp
    
    def setKi(self,I):
        self.Ki=I
    
    def getKi(self):
        return self.Ki

    def setKd(self,D):
        self.Kd=D
    
    def getKd(self):
        return self.Kd

    def setAll(self,P=0.,I=0.,D=0.):
        self.Kp=P
        self.Ki=I
        self.Kd=D

    def setAllFromList(self, params):
        self.Kp=params[0]
        self.Ki=params[1]
        self.Kd=params[2]

    def getAll(self):
        return [self.Kp, self.Ki,self.Kd]
        

class pidSetup(QtWidgets.QWidget, Ui_pidSetup):
    send_roll_pid=QtCore.pyqtSignal(object)
    send_pitch_pid=QtCore.pyqtSignal(object)
    send_yaw_pid=QtCore.pyqtSignal(object)
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.variables_setup()
        self.connect_buttons()
        self.setStyleSheet(open("../style/pidSetup.css").read())

    def variables_setup(self):
        self.roll_pid=PID()
        self.pitch_pid=PID()
        self.yaw_pid=PID()

    def connect_buttons(self):
        self.roll_set_btn.clicked.connect(self.roll_send)
        self.roll_restore_btn.clicked.connect(self.roll_restore)
        self.pitch_set_btn.clicked.connect(self.pitch_send)
        self.pitch_restore_btn.clicked.connect(self.pitch_restore)
        self.yaw_set_btn.clicked.connect(self.yaw_send)
        self.yaw_restore_btn.clicked.connect(self.yaw_restore)
        self.all_set_btn.clicked.connect(self.all_send)
        self.all_restore_btn.clicked.connect(self.all_restore)

    @QtCore.pyqtSlot()
    def roll_send(self):
        self.roll_pid.setKp(float(self.roll_kp_edit.value()))
        self.roll_pid.setKi(float(self.roll_ki_edit.value()))
        self.roll_pid.setKd(float(self.roll_kd_edit.value()))
        self.send_roll_pid.emit(self.roll_pid)

        message="Roll PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
        self.status.setText(message)

    def roll_restore(self):
        self.roll_kp_edit.setValue(self.roll_pid.getKp())
        self.roll_ki_edit.setValue(self.roll_pid.getKi())
        self.roll_kd_edit.setValue(self.roll_pid.getKd())
        message="Roll PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
        self.status.setText(message)

    @QtCore.pyqtSlot()
    def pitch_send(self):
        self.pitch_pid.setKp(self.pitch_kp_edit.value())
        self.pitch_pid.setKi(self.pitch_ki_edit.value())
        self.pitch_pid.setKd(self.pitch_kd_edit.value())
        self.send_pitch_pid.emit(self.pitch_pid)

        message="Pitch PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
        self.status.setText(message)
        
    def pitch_restore(self):
        self.pitch_kp_edit.setValue(self.pitch_pid.getKp())
        self.pitch_ki_edit.setValue(self.pitch_pid.getKi())
        self.pitch_kd_edit.setValue(self.pitch_pid.getKd())
        message="Pitch PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
        self.status.setText(message)

    @QtCore.pyqtSlot()
    def yaw_send(self):
        self.yaw_pid.setKp(self.yaw_kp_edit.value())
        self.yaw_pid.setKi(self.yaw_ki_edit.value())
        self.yaw_pid.setKd(self.yaw_kd_edit.value())
        self.send_yaw_pid.emit(self.yaw_pid)

        message="Yaw PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
        self.status.setText(message)
        
    def yaw_restore(self):
        self.yaw_kp_edit.setValue(self.yaw_pid.getKp())
        self.yaw_ki_edit.setValue(self.yaw_pid.getKi())
        self.yaw_kd_edit.setValue(self.yaw_pid.getKd())
        message="Yaw PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
        self.status.setText(message)

    def all_send(self):
        self.roll_send()
        self.pitch_send()
        self.yaw_send()
        message="All PIDs set"
        message+="\nRoll PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
        message+="\nPitch PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
        message+="\nYaw PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
        self.status.setText(message)

    def all_restore(self):
        self.roll_restore()
        self.pitch_restore()
        self.yaw_restore()
        message="All PIDs restored from odroid"
        message+="\nRoll PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
        message+="\nPitch PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
        message+="\nYaw PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
        self.status.setText(message)

    @QtCore.pyqtSlot(object,object,object)
    def update(self, roll_pid=PID(),pitch_pid=PID(),yaw_pid=PID()):
        self.roll_pid.setAllFromList(roll_pid.getAll())
        self.pitch_pid.setAllFromList(pitch_pid.getAll())
        self.yaw_pid.setAllFromList(yaw_pid.getAll())

if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    window=pidSetup()
    window.show()
    app.exec_()
