# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from .pidSetup_ui import Ui_pidSetup


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
    send_pid=QtCore.pyqtSignal(object)
    request_pid=QtCore.pyqtSignal(str)
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.variables_setup()
        self.connect_buttons()
        #self.setStyleSheet(open("style/pidSetup.css").read())

    def variables_setup(self):
        self.roll_pid=PID()
        self.pitch_pid=PID()
        self.yaw_pid=PID()

    def connect_buttons(self):
        self.roll_set_btn.clicked.connect(lambda x: self.pidSend('roll'))
        self.roll_restore_btn.clicked.connect(lambda x: self.pidRequest('roll'))
        self.pitch_set_btn.clicked.connect(lambda x: self.pidSend('pitch'))
        self.pitch_restore_btn.clicked.connect(lambda x: self.pidRequest('pitch'))
        self.yaw_set_btn.clicked.connect(lambda x: self.pidSend('yaw'))
        self.yaw_restore_btn.clicked.connect(lambda x: self.pidRequest('yaw'))
        self.all_set_btn.clicked.connect(lambda x: self.pidSend('all'))
        self.all_restore_btn.clicked.connect(lambda x: self.pidRequest('all'))

    @QtCore.pyqtSlot(str)
    def pidRequest(self, data):
        self.request_pid.emit(data)

    @QtCore.pyqtSlot(str)
    def pidSend(self, data):
        if data=='roll':
            self.roll_pid.setKp(float(self.roll_kp_edit.value()))
            self.roll_pid.setKi(float(self.roll_ki_edit.value()))
            self.roll_pid.setKd(float(self.roll_kd_edit.value()))
            self.send_pid.emit(['roll',self.roll_pid.getKp(),self.roll_pid.getKi(),self.roll_pid.getKd()])
            message="Roll PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
            self.status.setText(message)
        if data=='pitch':
            self.pitch_pid.setKp(float(self.pitch_kp_edit.value()))
            self.pitch_pid.setKi(float(self.pitch_ki_edit.value()))
            self.pitch_pid.setKd(float(self.pitch_kd_edit.value()))
            self.send_pid.emit(['pitch',self.pitch_pid.getKp(),self.pitch_pid.getKi(),self.pitch_pid.getKd()])
            message="Pitch PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
            self.status.setText(message)
        if data=='yaw':
            self.yaw_pid.setKp(float(self.yaw_kp_edit.value()))
            self.yaw_pid.setKi(float(self.yaw_ki_edit.value()))
            self.yaw_pid.setKd(float(self.yaw_kd_edit.value()))
            self.send_pid.emit(['yaw',self.yaw_pid.getKp(),self.yaw_pid.getKi(),self.yaw_pid.getKd()])
            message="Yaw PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
            self.status.setText(message)
        if data=='all':
            self.roll_pid.setKp(float(self.roll_kp_edit.value()))
            self.roll_pid.setKi(float(self.roll_ki_edit.value()))
            self.roll_pid.setKd(float(self.roll_kd_edit.value()))
            self.pitch_pid.setKp(float(self.pitch_kp_edit.value()))
            self.pitch_pid.setKi(float(self.pitch_ki_edit.value()))
            self.pitch_pid.setKd(float(self.pitch_kd_edit.value()))
            self.yaw_pid.setKp(float(self.yaw_kp_edit.value()))
            self.yaw_pid.setKi(float(self.yaw_ki_edit.value()))
            self.yaw_pid.setKd(float(self.yaw_kd_edit.value()))
            self.send_pid.emit([
                'all',self.roll_pid.getKp(),self.roll_pid.getKi(),self.roll_pid.getKd(),
                self.pitch_pid.getKp(),self.pitch_pid.getKi(),self.pitch_pid.getKd(),
                self.yaw_pid.getKp(),self.yaw_pid.getKi(),self.yaw_pid.getKd()
                ])
            message="All PIDs set"
            message+="\nRoll PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
            message+="\nPitch PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
            message+="\nYaw PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
            self.status.setText(message)

    def update(self, data):
        if data[0]=='roll':
            self.roll_pid.setKp(float(data[1]))
            self.roll_pid.setKi(float(data[2]))
            self.roll_pid.setKd(float(data[3]))
            self.roll_kp_edit.setValue(self.roll_pid.getKp())
            self.roll_ki_edit.setValue(self.roll_pid.getKi())
            self.roll_kd_edit.setValue(self.roll_pid.getKd())
            message="Roll PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
            self.status.setText(message)

        if data[0]=='pitch':
            self.pitch_pid.setKp(float(data[1]))
            self.pitch_pid.setKi(float(data[2]))
            self.pitch_pid.setKd(float(data[3]))
            self.pitch_kp_edit.setValue(self.pitch_pid.getKp())
            self.pitch_ki_edit.setValue(self.pitch_pid.getKi())
            self.pitch_kd_edit.setValue(self.pitch_pid.getKd())
            message="Pitch PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
            self.status.setText(message)

        if data[0]=='yaw':
            self.yaw_pid.setKp(float(data[1]))
            self.yaw_pid.setKi(float(data[2]))
            self.yaw_pid.setKd(float(data[3]))
            self.yaw_kp_edit.setValue(self.yaw_pid.getKp())
            self.yaw_ki_edit.setValue(self.yaw_pid.getKi())
            self.yaw_kd_edit.setValue(self.yaw_pid.getKd())
            message="Yaw PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
            self.status.setText(message)

        if data[0]=='all':
            self.roll_pid.setKp(float(data[1]))
            self.roll_pid.setKi(float(data[2]))
            self.roll_pid.setKd(float(data[3]))
            self.pitch_pid.setKp(float(data[4]))
            self.pitch_pid.setKi(float(data[5]))
            self.pitch_pid.setKd(float(data[6]))
            self.yaw_pid.setKp(float(data[7]))
            self.yaw_pid.setKi(float(data[8]))
            self.yaw_pid.setKd(float(data[9]))
            self.roll_kp_edit.setValue(self.roll_pid.getKp())
            self.roll_ki_edit.setValue(self.roll_pid.getKi())
            self.roll_kd_edit.setValue(self.roll_pid.getKd())
            self.pitch_kp_edit.setValue(self.pitch_pid.getKp())
            self.pitch_ki_edit.setValue(self.pitch_pid.getKi())
            self.pitch_kd_edit.setValue(self.pitch_pid.getKd())
            self.yaw_kp_edit.setValue(self.yaw_pid.getKp())
            self.yaw_ki_edit.setValue(self.yaw_pid.getKi())
            self.yaw_kd_edit.setValue(self.yaw_pid.getKd())
            message="All PIDs restored from odroid"
            message+="\nRoll PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd())
            message+="\nPitch PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd())
            message+="\nYaw PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd())
            self.status.setText(message)



if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    window=pidSetup()
    window.show()
    app.exec_()
