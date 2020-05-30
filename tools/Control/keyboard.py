from PyQt5 import QtWidgets, QtCore, QtGui
class Keyboard(QtWidgets.QWidget):
    escapeClicked = QtCore.pyqtSignal()
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.getData_callback = None
        self.mode = "keyboard"
        self.key_mem={}
        self.output = {"vertical": 0, 'roll':0, 'pitch':0, "yaw":0, "throttle":0}
        self.key_assignment = {"forward":0,
                            "backward":0,
                            "roll_left":0,
                            "roll_right":0,
                            "pitch_forward":0,
                            "pitch_backward":0,
                            "yaw_left":0,
                            "yaw_right":0,
                            "emerge":0,
                            "submerge":0
                            }

        self.control_spec = {"throttle_rate":50,
                             "throttle_stop":0.7,
                             "vertical_rate":20,
                             "vertical_stop":0.7,
                             "yaw_rate":20,
                             "yaw_stop":0.0,
                             "throttle_limit":500,
                             "yaw_limit":500,
                             "vertical_limit":500,
                             "roll_limit":45,
                             "pitch_limit":45,
                             "roll_rate":1,
                             "yaw_rate":1,
                             "roll_stop":0,
                             "pitch_stop":0
                             }
    def setKeyAssignment(self,arg):
        self.key_assignment = arg
        for i in self.key_assignment.values():
            self.key_mem[i] = False
        

    def setConfig(self,arg):
        self.control_spec = arg

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            if event.key()==QtCore.Qt.Key_Escape:
                self.escapeClicked.emit()
            self.key_mem[event.key()] = True
            
    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.key_mem[event.key()] = False

    def start_control(self):
        self.grabKeyboard()
    def stop_control(self):
        self.releaseKeyboard()
    def get_data(self):
        #print(self.key_mem)
        #horizontal forward/backward
        if self.key_mem[self.key_assignment["forward"]] and not self.key_mem[self.key_assignment["backward"]]:
            self.output["throttle"] +=self.control_spec["throttle_rate"]
        elif not self.key_mem[self.key_assignment["forward"]] and self.key_mem[self.key_assignment["backward"]]:
            self.output["throttle"] -=self.control_spec["throttle_rate"]
        #both pressed or none is breaking
        elif self.key_mem[self.key_assignment["forward"]] and self.key_mem[self.key_assignment["backward"]]:
            self.output["throttle"] *= self.control_spec["throttle_stop"]
        elif not self.key_mem[self.key_assignment["forward"]] and not self.key_mem[self.key_assignment["backward"]]:
            self.output["throttle"] *= self.control_spec["throttle_stop"]

        #yaw 
        if self.key_mem[self.key_assignment["yaw_left"]] and not self.key_mem[self.key_assignment["yaw_right"]]:
            self.output["yaw"] -=self.control_spec["yaw_rate"]
        elif not self.key_mem[self.key_assignment["yaw_left"]] and self.key_mem[self.key_assignment["yaw_right"]]:
            self.output["yaw"] +=self.control_spec["yaw_rate"]
        elif self.key_mem[self.key_assignment["yaw_left"]] and self.key_mem[self.key_assignment["yaw_right"]]:
            self.output["yaw"] *= self.control_spec["yaw_stop"]
        elif not self.key_mem[self.key_assignment["yaw_left"]] and not self.key_mem[self.key_assignment["yaw_right"]]:
            self.output["yaw"] *= self.control_spec["yaw_stop"]

        #vertical 
        if self.key_mem[self.key_assignment["emerge"]] and not self.key_mem[self.key_assignment["submerge"]]:
            self.output["vertical"] +=self.control_spec["vertical_rate"]
        elif not self.key_mem[self.key_assignment["emerge"]] and self.key_mem[self.key_assignment["submerge"]]:
           self.output["vertical"] -=self.control_spec["vertical_rate"]
        elif self.key_mem[self.key_assignment["emerge"]] and self.key_mem[self.key_assignment["submerge"]]:
            self.output["vertical"] *= self.control_spec["vertical_stop"]
        elif not self.key_mem[self.key_assignment["emerge"]] and not self.key_mem[self.key_assignment["submerge"]]:
            self.output["vertical"] *= self.control_spec["vertical_stop"]
        #roll
        if self.key_mem[self.key_assignment["roll_left"]] and not self.key_mem[self.key_assignment["roll_right"]]:
            self.output["roll"] +=self.control_spec["roll_rate"]
        elif not self.key_mem[self.key_assignment["roll_left"]] and self.key_mem[self.key_assignment["roll_right"]]:
            self.output["roll"] -=self.control_spec["roll_rate"]
        elif self.key_mem[self.key_assignment["roll_left"]] and self.key_mem[self.key_assignment["roll_right"]]:
            self.output["roll"] *= self.control_spec["roll_stop"]
        elif not self.key_mem[self.key_assignment["roll_left"]] and not self.key_mem[self.key_assignment["roll_right"]]:
            self.output["roll"] *= self.control_spec["roll_stop"] 
        #pitch
        if self.key_mem[self.key_assignment["pitch_backward"]] and not self.key_mem[self.key_assignment["pitch_forward"]]:
            self.output["pitch"] +=self.control_spec["pitch_rate"]
        elif not self.key_mem[self.key_assignment["pitch_backward"]] and self.key_mem[self.key_assignment["pitch_forward"]]:
            self.output["pitch"] -=self.control_spec["pitch_rate"]
        elif self.key_mem[self.key_assignment["pitch_backward"]] and self.key_mem[self.key_assignment["pitch_forward"]]:
            self.output["pitch"] *= self.control_spec["pitch_stop"]
        elif not self.key_mem[self.key_assignment["pitch_backward"]] and not self.key_mem[self.key_assignment["pitch_forward"]]:
            self.output["pitch"] *= self.control_spec["pitch_stop"] 
        for i in self.output:
            if self.output[i]>self.control_spec[i+"_limit"]:
                self.output[i] = self.control_spec[i+"_limit"]
            elif self.output[i]<-self.control_spec[i+"_limit"]:
                self.output[i] = -self.control_spec[i+"_limit"]
        self.getData_callback.emit([self.output["roll"],self.output["pitch"],int(self.output["yaw"]),int(self.output["vertical"]),int(self.output["throttle"])])
    
    def run(self):
        pass