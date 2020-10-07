from PyQt5 import QtWidgets, QtCore, QtGui
import json
class keyboard_widget(QtWidgets.QWidget):
    getData_callback = QtCore.pyqtSignal(object)
    configChanged =      QtCore.pyqtSignal(object)   
    def __init__(self,parent=None):
       QtWidgets.QWidget.__init__(self,parent)

       #self.setStyleSheet("background-color: green;")
       
       self.key_assignment = {"forward":QtCore.Qt.Key_W,
                        "backward":QtCore.Qt.Key_S,
                        "roll_left":QtCore.Qt.Key_Q,
                        "roll_right":QtCore.Qt.Key_E,
                        "pitch_forward":QtCore.Qt.Key_R,
                        "pitch_backward":QtCore.Qt.Key_F,
                        "yaw_left":QtCore.Qt.Key_A,
                        "yaw_right":QtCore.Qt.Key_D,
                        "emerge":QtCore.Qt.Key_Up,
                        "submerge":QtCore.Qt.Key_Down
                        }

       self.l_forward = QtWidgets.QLabel(self)
       self.l_backward = QtWidgets.QLabel(self)
       self.l_yaw_l = QtWidgets.QLabel(self)
       self.l_yaw_r = QtWidgets.QLabel(self)
       self.l_emerge = QtWidgets.QLabel(self)
       self.l_submerge = QtWidgets.QLabel(self)
       self.l_roll_l = QtWidgets.QLabel(self)
       self.l_roll_r = QtWidgets.QLabel(self)
       self.l_pitch_f = QtWidgets.QLabel(self)
       self.l_pitch_b = QtWidgets.QLabel(self)

       self.l_forward.setAccessibleName("forward")
       self.l_backward.setAccessibleName("backward")
       self.l_yaw_l.setAccessibleName("yaw_left")
       self.l_yaw_r.setAccessibleName("yaw_right")
       self.l_emerge.setAccessibleName("emerge")
       self.l_submerge.setAccessibleName("submerge")
       self.l_roll_l.setAccessibleName("roll_left")
       self.l_roll_r.setAccessibleName("roll_right")
       self.l_pitch_f.setAccessibleName("pitch_forward")
       self.l_pitch_b.setAccessibleName("pitch_backward")

       self.b_forward = QtWidgets.QPushButton(self)
       self.b_backward  = QtWidgets.QPushButton(self)
       self.b_yaw_l = QtWidgets.QPushButton(self)
       self.b_yaw_r = QtWidgets.QPushButton(self)
       self.b_emerge = QtWidgets.QPushButton(self)
       self.b_submerge = QtWidgets.QPushButton(self)
       self.b_roll_l = QtWidgets.QPushButton(self)
       self.b_roll_r = QtWidgets.QPushButton(self)
       self.b_pitch_f = QtWidgets.QPushButton(self)
       self.b_pitch_b = QtWidgets.QPushButton(self)

       self.l_forward.setText("Forward")
       self.l_backward.setText("Backward")
       self.l_yaw_l.setText("Yaw left")
       self.l_yaw_r.setText("Yaw right")
       self.l_emerge.setText("Emerge")
       self.l_submerge.setText("Submerge")
       self.l_roll_l.setText ("Roll left")
       self.l_roll_r.setText ("Roll right")
       self.l_pitch_f.setText("Pitch forward")
       self.l_pitch_b.setText("Pitch backward")

       self.b_forward.setText("W")
       self.b_backward.setText("S")
       self.b_yaw_l.setText("A")
       self.b_yaw_r.setText("D")
       self.b_emerge.setText("Up")
       self.b_submerge.setText("Down")
       self.b_roll_l.setText("Q")
       self.b_roll_r.setText("E")
       self.b_pitch_f.setText("R")
       self.b_pitch_b.setText("F")

       self.b_forward.setAccessibleName("forward")
       self.b_backward.setAccessibleName("backward")
       self.b_yaw_l.setAccessibleName("yaw_left")
       self.b_yaw_r.setAccessibleName("yaw_right")
       self.b_emerge.setAccessibleName("emerge")
       self.b_submerge.setAccessibleName("submerge")
       self.b_roll_l.setAccessibleName("roll_left")
       self.b_roll_r.setAccessibleName("roll_right")
       self.b_pitch_f.setAccessibleName("pitch_forward")
       self.b_pitch_b.setAccessibleName("pitch_backward")

       rate_box = QtWidgets.QGroupBox(self)
       limit_box = QtWidgets.QGroupBox(self)

       limit_box.setTitle("Limits")
       rate_box.setTitle("Rates")

       self.l1_throttle = QtWidgets.QLabel(self)
       self.l1_yaw = QtWidgets.QLabel(self)
       self.l1_roll = QtWidgets.QLabel(self)
       self.l1_pitch = QtWidgets.QLabel(self)
       self.l1_vertical = QtWidgets.QLabel(self)

       self.l1_throttle.setText("Throttle")
       self.l1_yaw.setText("Yaw")
       self.l1_vertical.setText("Vertical")
       self.l1_roll.setText("Roll")
       self.l1_pitch.setText("Pitch")

       self.l2_throttle = QtWidgets.QLabel(self)
       self.l2_yaw = QtWidgets.QLabel(self)
       self.l2_roll = QtWidgets.QLabel(self)
       self.l2_pitch = QtWidgets.QLabel(self)
       self.l2_vertical = QtWidgets.QLabel(self)

       self.l2_throttle.setText("Throttle")
       self.l2_yaw.setText("Yaw")
       self.l2_vertical.setText("Vertical")
       self.l2_roll.setText("Roll")
       self.l2_pitch.setText("Pitch")

       self.s_pitch_rate = QtWidgets.QSpinBox(rate_box)
       self.s_roll_rate = QtWidgets.QSpinBox(rate_box)
       self.s_throttle_rate = QtWidgets.QSpinBox(rate_box)
       self.s_vertical_rate = QtWidgets.QSpinBox(rate_box)
       self.s_yaw_rate = QtWidgets.QSpinBox(rate_box)

       self.s_pitch_limit = QtWidgets.QSpinBox(limit_box)
       self.s_roll_limit = QtWidgets.QSpinBox(limit_box)             
       self.s_throttle_limit = QtWidgets.QSpinBox(limit_box)
       self.s_vertical_limit = QtWidgets.QSpinBox(limit_box)
       self.s_yaw_limit = QtWidgets.QSpinBox(limit_box)

       mainLayout= QtWidgets.QVBoxLayout()
       assignmentLayout = QtWidgets.QGridLayout()
       specLayout = QtWidgets.QHBoxLayout()
       rateLayout = QtWidgets.QGridLayout()
       limitLayout = QtWidgets.QGridLayout()

       limitLayout.addWidget(self.l1_roll,0,0)
       limitLayout.addWidget(self.l1_pitch,1,0)
       limitLayout.addWidget(self.l1_yaw,2,0)
       limitLayout.addWidget(self.l1_vertical,3,0)
       limitLayout.addWidget(self.l1_throttle,4,0)

       limitLayout.addWidget(self.s_roll_limit,0,1)
       limitLayout.addWidget(self.s_pitch_limit,1,1)
       limitLayout.addWidget(self.s_yaw_limit,2,1)
       limitLayout.addWidget(self.s_vertical_limit,3,1)
       limitLayout.addWidget(self.s_throttle_limit,4,1)

       rateLayout.addWidget(self.l2_roll,0,0)
       rateLayout.addWidget(self.l2_pitch,1,0)
       rateLayout.addWidget(self.l2_yaw,2,0)
       rateLayout.addWidget(self.l2_vertical,3,0)
       rateLayout.addWidget(self.l2_throttle,4,0)

       rateLayout.addWidget(self.s_roll_rate,0,1)
       rateLayout.addWidget(self.s_pitch_rate,1,1)
       rateLayout.addWidget(self.s_yaw_rate,2,1)
       rateLayout.addWidget(self.s_vertical_rate,3,1)
       rateLayout.addWidget(self.s_throttle_rate,4,1)

       rate_box.setLayout(rateLayout)
       limit_box.setLayout(limitLayout)
       sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
       rate_box.setSizePolicy(sizePolicy)
       limit_box.setSizePolicy(sizePolicy)
       specLayout.addWidget(rate_box)
       specLayout.addWidget(limit_box)

       mainLayout.addLayout(specLayout)

       assignmentLayout.addWidget(self.l_forward,0,0)
       assignmentLayout.addWidget(self.l_backward,1,0)
       assignmentLayout.addWidget(self.l_yaw_l,2,0)
       assignmentLayout.addWidget(self.l_yaw_r,3,0)
       assignmentLayout.addWidget(self.l_emerge,4,0)
       assignmentLayout.addWidget(self.l_submerge,5,0)
       assignmentLayout.addWidget(self.l_roll_l,6,0)
       assignmentLayout.addWidget(self.l_roll_r,7,0)
       assignmentLayout.addWidget(self.l_pitch_f,8,0)
       assignmentLayout.addWidget(self.l_pitch_b,9,0)

       assignmentLayout.addWidget(self.b_forward,0,1)
       assignmentLayout.addWidget(self.b_backward,1,1)
       assignmentLayout.addWidget(self.b_yaw_l,2,1)
       assignmentLayout.addWidget(self.b_yaw_r,3,1)
       assignmentLayout.addWidget(self.b_emerge,4,1)
       assignmentLayout.addWidget(self.b_submerge,5,1)
       assignmentLayout.addWidget(self.b_roll_l,6,1)
       assignmentLayout.addWidget(self.b_roll_r,7,1)
       assignmentLayout.addWidget(self.b_pitch_f,8,1)
       assignmentLayout.addWidget(self.b_pitch_b,9,1)

       mainLayout.addLayout(assignmentLayout)
       self.b_backward.clicked.connect(lambda: self.dialog(self.l_backward,self.b_backward))
       self.b_forward.clicked.connect(lambda: self.dialog(self.l_forward, self.b_forward))
       self.b_yaw_l.clicked.connect(lambda: self.dialog(self.l_yaw_l, self.b_yaw_l))
       self.b_yaw_r.clicked.connect(lambda: self.dialog(self.l_yaw_r, self.b_yaw_r))
       self.b_emerge.clicked.connect(lambda: self.dialog(self.l_emerge, self.b_emerge))
       self.b_submerge.clicked.connect(lambda: self.dialog(self.l_submerge, self.b_submerge))
       self.b_roll_r.clicked.connect(lambda: self.dialog(self.l_roll_r, self.b_roll_r))
       self.b_roll_l.clicked.connect(lambda: self.dialog(self.l_roll_l, self.b_roll_l))
       self.b_pitch_f.clicked.connect(lambda: self.dialog(self.l_pitch_f, self.b_pitch_f))
       self.b_pitch_b.clicked.connect(lambda: self.dialog(self.l_pitch_b, self.b_pitch_b))
       sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
       self.setSizePolicy(sizePolicy)
       mainLayout.addStretch()
       self.setLayout(mainLayout)
       rateLayout.widget
       for i in rate_box.findChildren(QtWidgets.QSpinBox):
           i.setMaximum(100)
           i.setValue(50)
           i.setSingleStep(5)
           i.setMinimum(0)
       for i in limit_box.findChildren(QtWidgets.QSpinBox):
           i.setMaximum(1000)
           i.setValue(500)
           i.setSingleStep(50)
           i.setMinimum(0)
     
       self.s_roll_rate.setValue(5)
       self.s_roll_rate.setSingleStep(1)
       self.s_roll_limit.setValue(45)
       self.s_roll_limit.setSingleStep(1)
       self.s_roll_limit.setSuffix("�")

       self.s_pitch_rate.setValue(5)
       self.s_pitch_rate.setSingleStep(1)
       self.s_pitch_limit.setValue(45)
       self.s_pitch_limit.setSingleStep(1)
       self.s_pitch_limit.setSuffix("�")
       for i in self.findChildren(QtWidgets.QSpinBox):
            i.valueChanged.connect(lambda: self.configChanged.emit(self.getConfig()))
       mainLayout.setContentsMargins(0,0,0,0)
       self.loadKey()
       self.loadConfig()

    def enableButtons(self):
        for i in self.findChildren(QtWidgets.QPushButton):
            i.setEnabled(True)

    def disableButtons(self):
        for i in self.findChildren(QtWidgets.QPushButton):
            i.setEnabled(False)


    def saveKey(self):
        with open('config/key_assignment.json','w')as fd:
            json.dump(self.key_assignment, fd, indent=1)

    def loadKey(self):
        cfg ={}
        try:
            with open("config/key_assignment.json",'r') as fd:
                cfg = json.load(fd)
        except:
            return
        self.key_assignment = cfg
        for i in self.findChildren(QtWidgets.QPushButton):
            try:
                i.setText(chr(cfg[i.accessibleName()]))
            except ValueError:
                i.setText(self.a2k[cfg[i.accessibleName()]])


    a2k = {
            QtCore.Qt.Key_Up:"Up",
            QtCore.Qt.Key_Down:"Down",
            QtCore.Qt.Key_Right:"Right",
            QtCore.Qt.Key_Left:"Left",
            QtCore.Qt.Key_Space:"Space",
            QtCore.Qt.Key_Home:"Home",
            QtCore.Qt.Key_Tab:"Tab",
            QtCore.Qt.Key_Enter:"Enter",
            QtCore.Qt.Key_Return:"Return",
            QtCore.Qt.Key_Insert:"Insert",
            QtCore.Qt.Key_Delete:"Delete",
            QtCore.Qt.Key_Pause:"Pause",
            QtCore.Qt.Key_Print:"Print"
            }
    def dialog(self,label, button):
        

        def setKeyAss(name, value):
            self.key_assignment[name]=value

        class dialog(QtWidgets.QWidget):
            def __init__(self,parent=None, button = None, label = None):
                QtWidgets.QWidget.__init__(self,parent)
                self.saveKey = None
                self.setAssignment = None
                l = QtWidgets.QVBoxLayout()
                l1 = QtWidgets.QLabel("Assign key to '"+label.text()+"'")
                l2 = QtWidgets.QLabel("Press 'Esc' to cancel")
                l1.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                l2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                l.addWidget(l1)
                l.addWidget(l2)
                self.setMinimumSize(QtCore.QSize(200, 200))
                self.setWindowModality(QtCore.Qt.ApplicationModal)
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.Dialog)
                self.setLayout(l)
                self.show()

            def keyPressEvent(self,event):
                if event.isAutoRepeat():
                    return
                if event.key()==QtCore.Qt.Key_Escape:
                    self.close()
                    return
                self.setAssignment(label.accessibleName(),event.key())
                tb = event.text().capitalize()
                if tb == "" or tb == " " or tb == chr(13) or tb == chr(9):
                    try:
                        tb = self.a2k[event.key()]
                    except KeyError:
                        tb = str(event.key())   
                self.saveKey()
                button.setText(tb)
                self.close()

        d = dialog(self, button, label)
        d.setAssignment = setKeyAss
        d.saveKey = self.saveKey




    def getConfig(self):
        control_spec = {     "throttle_rate":int(self.s_throttle_rate.text()),
                             "throttle_stop":0.7,
                             "vertical_rate":int(self.s_vertical_rate.text()),
                             "vertical_stop":0.7,
                             "yaw_rate":int(self.s_yaw_rate.text()),
                             "yaw_stop":0.0,
                             "roll_stop":0,
                             "pitch_stop":0,
                             "throttle_limit":int(self.s_throttle_limit.text()),
                             "yaw_limit":int(self.s_yaw_limit.text()),
                             "vertical_limit":int(self.s_vertical_limit.text()),
                             "roll_rate":int(self.s_roll_rate.text()),
                             "roll_limit":int(self.s_roll_limit.text().replace('�','')),
                             "pitch_rate":int(self.s_pitch_rate.text()),
                             "pitch_limit":int(self.s_pitch_limit.text().replace('�',''))
                             }
        return control_spec

    def saveConfig(self):
        with open('config/keyboard_config.json','w')as fd:
            json.dump(self.getConfig(), fd, indent=1)
    
    def loadConfig(self):
        cfg ={}
        try:
            with open("confgig/keyboard_config.json",'r') as fd:
                cfg = json.load(fd)
        except:
            return
        self.s_throttle_rate.setValue(cfg["throttle_rate"])
        self.s_vertical_rate.setValue(cfg["vertical_rate"])
        self.s_yaw_rate.setValue(cfg["yaw_rate"])
        self.s_roll_rate.setValue(cfg["roll_rate"])
        self.s_pitch_rate.setValue(cfg["pitch_rate"])
        self.s_throttle_limit.setValue(cfg["throttle_limit"])
        self.s_vertical_limit.setValue(cfg["vertical_limit"])
        self.s_yaw_limit.setValue(cfg["yaw_limit"])
        self.s_roll_limit.setValue(cfg["roll_limit"])
        self.s_pitch_limit.setValue(cfg["pitch_limit"])


