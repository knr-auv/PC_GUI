# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from .pidSetup_ui import Ui_pidSetup
import logging


class PID:
    def __init__(self,P=0.,I=0.,D=0.):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Kl = 0
        
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

    def setKl(self, L):
        self.Kl = L
    
    def getKl(self):
        return self.Kl

    def setAll(self,P=0.,I=0.,D=0., L = 0.):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Kl = L

    def setAllFromList(self, params):
        self.Kp=params[0]
        self.Ki=params[1]
        self.Kd=params[2]
        self.Kl = params[3]

    def getAll(self):
        return [self.Kp, self.Ki,self.Kd, self.Kl]
        

class pidSetup(QtWidgets.QWidget, Ui_pidSetup):
    send_pid=QtCore.pyqtSignal(object)
    request_pid=QtCore.pyqtSignal(str)
    send_msg = QtCore.pyqtSignal(str)
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
        self.l_roll_pid = PID()
        self.l_pitch_pid = PID()
        self.depth_pid = PID()

    def connect_buttons(self):
        self.roll_set_btn.clicked.connect(lambda x: self.pidSend('roll'))
        self.roll_restore_btn.clicked.connect(lambda x: self.pidRequest('roll'))
        self.pitch_set_btn.clicked.connect(lambda x: self.pidSend('pitch'))
        self.pitch_restore_btn.clicked.connect(lambda x: self.pidRequest('pitch'))
        self.yaw_set_btn.clicked.connect(lambda x: self.pidSend('yaw'))
        self.yaw_restore_btn.clicked.connect(lambda x: self.pidRequest('yaw'))
        self.depth_set_btn.clicked.connect(lambda x: self.pidSend('depth'))
        self.depth_restore_btn.clicked.connect(lambda x: self.pidRequest('depth'))
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
            self.roll_pid.setKl(float(self.roll_rate_edit.value()))
            self.send_pid.emit(['roll',self.roll_pid.getKp(),self.roll_pid.getKi(),self.roll_pid.getKd(), self.roll_pid.getKl()])
            message="Roll PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f}, Kl: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd(), self.roll_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Roll PID set")
        if data=='pitch':
            self.pitch_pid.setKp(float(self.pitch_kp_edit.value()))
            self.pitch_pid.setKi(float(self.pitch_ki_edit.value()))
            self.pitch_pid.setKd(float(self.pitch_kd_edit.value()))
            self.pitch_pid.setKl(float(self.pitch_rate_edit.value()))
            self.send_pid.emit(['pitch',self.pitch_pid.getKp(),self.pitch_pid.getKi(),self.pitch_pid.getKd(), self.pitch_pid.getKl()])
            message="Pitch PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd(), self.pitch_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Pitch PID set")
        if data=='yaw':
            self.yaw_pid.setKp(float(self.yaw_kp_edit.value()))
            self.yaw_pid.setKi(float(self.yaw_ki_edit.value()))
            self.yaw_pid.setKd(float(self.yaw_kd_edit.value()))
            self.yaw_pid.setKl(float(self.yaw_rate_edit.value()))
            self.send_pid.emit(['yaw',self.yaw_pid.getKp(),self.yaw_pid.getKi(),self.yaw_pid.getKd(), self.yaw_pid.getKl()])
            message="Yaw PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd(), self.yaw_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Yaw PID set")

        if data=='depth':
            self.depth_pid.setKp(float(self.depth_kp_edit.value()))
            self.depth_pid.setKi(float(self.depth_ki_edit.value()))
            self.depth_pid.setKd(float(self.depth_kd_edit.value()))
            self.depth_pid.setKl(float(self.depth_rate_edit.value()))
            self.send_pid.emit(['depth',self.depth_pid.getKp(),self.depth_pid.getKi(),self.depth_pid.getKd(), self.depth_pid.getKl()])
            message="depth PID set\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.depth_pid.getKp(), self.depth_pid.getKi(), self.depth_pid.getKd(), self.depth_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Depth PID set")

        if data=='all':
            self.roll_pid.setKp(float(self.roll_kp_edit.value()))
            self.roll_pid.setKi(float(self.roll_ki_edit.value()))
            self.roll_pid.setKd(float(self.roll_kd_edit.value()))
            self.roll_pid.setKl(float(self.roll_rate_edit.value()))

            self.pitch_pid.setKp(float(self.pitch_kp_edit.value()))
            self.pitch_pid.setKi(float(self.pitch_ki_edit.value()))
            self.pitch_pid.setKd(float(self.pitch_kd_edit.value()))
            self.pitch_pid.setKl(float(self.pitch_rate_edit.value()))

            self.yaw_pid.setKp(float(self.yaw_kp_edit.value()))
            self.yaw_pid.setKi(float(self.yaw_ki_edit.value()))
            self.yaw_pid.setKd(float(self.yaw_kd_edit.value()))
            self.yaw_pid.setKl(float(self.yaw_rate_edit.value()))

            self.depth_pid.setKp(float(self.depth_kp_edit.value()))
            self.depth_pid.setKi(float(self.depth_ki_edit.value()))
            self.depth_pid.setKd(float(self.depth_kd_edit.value()))
            self.depth_pid.setKl(float(self.depth_rate_edit.value()))

            self.send_pid.emit([
                'all',self.roll_pid.getKp(),self.roll_pid.getKi(),self.roll_pid.getKd(), self.roll_pid.getKl(),
                self.pitch_pid.getKp(),self.pitch_pid.getKi(),self.pitch_pid.getKd(),self.pitch_pid.getKl(),
                self.yaw_pid.getKp(),self.yaw_pid.getKi(),self.yaw_pid.getKd(),self.yaw_pid.getKl(),
                self.depth_pid.getKp(), self.depth_pid.getKi(),self.depth_pid.getKd(), self.depth_pid.getKl()
                ])
            message="All PIDs set"
            message+="\nRoll PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd(), self.roll_pid.getKl())
            message+="\nPitch PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd(), self.pitch_pid.getKl())
            message+="\nYaw PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd(), self.yaw_pid.getKl())
            message+="\ndepth PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.depth_pid.getKp(), self.depth_pid.getKi(),self.depth_pid.getKd(), self.depth_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("All PIDs set")

    def update(self, data):
        if data[0]=='roll':
            self.roll_pid.setKp(float(data[1]))
            self.roll_pid.setKi(float(data[2]))
            self.roll_pid.setKd(float(data[3]))
            self.roll_pid.setKl(float(data[4]))
            self.roll_kp_edit.setValue(self.roll_pid.getKp())
            self.roll_ki_edit.setValue(self.roll_pid.getKi())
            self.roll_kd_edit.setValue(self.roll_pid.getKd())
            self.roll_rate_edit.setValue(self.roll_pid.getKl())
            message="Roll PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd(),self.roll_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Roll pid restored")

        if data[0]=='pitch':
            self.pitch_pid.setKp(float(data[1]))
            self.pitch_pid.setKi(float(data[2]))
            self.pitch_pid.setKd(float(data[3]))
            self.pitch_pid.setKl(float(data[4]))
            self.pitch_kp_edit.setValue(self.pitch_pid.getKp())
            self.pitch_ki_edit.setValue(self.pitch_pid.getKi())
            self.pitch_kd_edit.setValue(self.pitch_pid.getKd())
            self.pitch_rate_edit.setValue(self.pitch_pid.getKl())
            message="Pitch PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd(),self.pitch_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Pitch pid restored")

        if data[0]=='yaw':
            self.yaw_pid.setKp(float(data[1]))
            self.yaw_pid.setKi(float(data[2]))
            self.yaw_pid.setKd(float(data[3]))
            self.yaw_pid.setKl(float(data[4]))
            self.yaw_kp_edit.setValue(self.yaw_pid.getKp())
            self.yaw_ki_edit.setValue(self.yaw_pid.getKi())
            self.yaw_kd_edit.setValue(self.yaw_pid.getKd())
            self.yaw_rate_edit.setValue(self.yaw_pid.getKl())
            message="Yaw PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd(), self.yaw_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Yaw pid restored")

        if data[0]=='depth':
            self.depth_pid.setKp(float(data[1]))
            self.depth_pid.setKi(float(data[2]))
            self.depth_pid.setKd(float(data[3]))
            self.depth_pid.setKl(float(data[4]))
            self.depth_kp_edit.setValue(self.depth_pid.getKp())
            self.depth_ki_edit.setValue(self.depth_pid.getKi())
            self.depth_kd_edit.setValue(self.depth_pid.getKd())
            self.depth_rate_edit.setValue(self.depth_pid.getKl())
            message="depth PID restored from odroid\nKp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.depth_pid.getKp(), self.depth_pid.getKi(), self.depth_pid.getKd(), self.depth_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("Depth PID restored")

        if data[0]=='all':
            self.roll_pid.setKp(float(data[1]))
            self.roll_pid.setKi(float(data[2]))
            self.roll_pid.setKd(float(data[3]))
            self.roll_pid.setKl(float(data[4]))

            self.pitch_pid.setKp(float(data[5]))
            self.pitch_pid.setKi(float(data[6]))
            self.pitch_pid.setKd(float(data[7]))
            self.pitch_pid.setKl(float(data[8]))

            self.yaw_pid.setKp(float(data[9]))
            self.yaw_pid.setKi(float(data[10]))
            self.yaw_pid.setKd(float(data[11]))
            self.yaw_pid.setKl(float(data[12]))

            self.depth_pid.setKp(float(data[13]))
            self.depth_pid.setKi(float(data[14]))
            self.depth_pid.setKd(float(data[15]))
            self.depth_pid.setKl(float(data[16]))
            
            self.roll_kp_edit.setValue(self.roll_pid.getKp())
            self.roll_ki_edit.setValue(self.roll_pid.getKi())
            self.roll_kd_edit.setValue(self.roll_pid.getKd())
            self.roll_rate_edit.setValue(self.roll_pid.getKl())

            self.pitch_kp_edit.setValue(self.pitch_pid.getKp())
            self.pitch_ki_edit.setValue(self.pitch_pid.getKi())
            self.pitch_kd_edit.setValue(self.pitch_pid.getKd())
            self.pitch_rate_edit.setValue(self.pitch_pid.getKl())

            self.yaw_kp_edit.setValue(self.yaw_pid.getKp())
            self.yaw_ki_edit.setValue(self.yaw_pid.getKi())
            self.yaw_kd_edit.setValue(self.yaw_pid.getKd())
            self.yaw_rate_edit.setValue(self.yaw_pid.getKl())

            self.depth_kp_edit.setValue(self.depth_pid.getKp())
            self.depth_ki_edit.setValue(self.depth_pid.getKi())
            self.depth_kd_edit.setValue(self.depth_pid.getKd())
            self.depth_rate_edit.setValue(self.depth_pid.getKl())

            message="All PIDs restored from odroid"
            message+="\nRoll PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.roll_pid.getKp(), self.roll_pid.getKi(), self.roll_pid.getKd(), self.roll_pid.getKl())
            message+="\nPitch PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.pitch_pid.getKp(), self.pitch_pid.getKi(), self.pitch_pid.getKd(), self.pitch_pid.getKl())
            message+="\nYaw PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.yaw_pid.getKp(), self.yaw_pid.getKi(), self.yaw_pid.getKd(), self.yaw_pid.getKl())
            message+="\ndepth PID Kp: {:.2f} Ki: {:.2f} Kd: {:.2f} Kl: {:.2f}".format(self.depth_pid.getKp(), self.depth_pid.getKi(),self.depth_pid.getKd(), self.depth_pid.getKl())
            logging.debug(message)
            self.send_msg.emit("All PIDs restored")



if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    window=pidSetup()
    window.show()
    app.exec_()
