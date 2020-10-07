# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiFiles/controlSettings.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_controlSettings(object):
    def setupUi(self, controlSettings):
        controlSettings.setObjectName("controlSettings")
        controlSettings.resize(365, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(controlSettings.sizePolicy().hasHeightForWidth())
        controlSettings.setSizePolicy(sizePolicy)
        controlSettings.setMinimumSize(QtCore.QSize(0, 600))
        controlSettings.setMaximumSize(QtCore.QSize(500, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(controlSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(controlSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_14 = QtWidgets.QLabel(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_4.addWidget(self.label_14)
        self.l_PIDInterval = QtWidgets.QLineEdit(self.widget_2)
        self.l_PIDInterval.setMaximumSize(QtCore.QSize(70, 16777215))
        self.l_PIDInterval.setAlignment(QtCore.Qt.AlignCenter)
        self.l_PIDInterval.setObjectName("l_PIDInterval")
        self.horizontalLayout_4.addWidget(self.l_PIDInterval)
        self.b_arm = QtWidgets.QPushButton(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_arm.sizePolicy().hasHeightForWidth())
        self.b_arm.setSizePolicy(sizePolicy)
        self.b_arm.setObjectName("b_arm")
        self.horizontalLayout_4.addWidget(self.b_arm)
        self.verticalLayout_3.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.s_control = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.s_control.sizePolicy().hasHeightForWidth())
        self.s_control.setSizePolicy(sizePolicy)
        self.s_control.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.s_control.setObjectName("s_control")
        self.s_control.addItem("")
        self.s_control.addItem("")
        self.s_control.addItem("")
        self.horizontalLayout_6.addWidget(self.s_control)
        self.label_13 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_6.addWidget(self.label_13)
        self.l_interval = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_interval.sizePolicy().hasHeightForWidth())
        self.l_interval.setSizePolicy(sizePolicy)
        self.l_interval.setMaximumSize(QtCore.QSize(50, 16777215))
        self.l_interval.setAlignment(QtCore.Qt.AlignCenter)
        self.l_interval.setObjectName("l_interval")
        self.horizontalLayout_6.addWidget(self.l_interval)
        self.b_start = QtWidgets.QPushButton(self.widget)
        self.b_start.setObjectName("b_start")
        self.horizontalLayout_6.addWidget(self.b_start)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_15 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_2.addWidget(self.label_15)
        self.mode_box = QtWidgets.QComboBox(self.widget)
        self.mode_box.setObjectName("mode_box")
        self.mode_box.addItem("")
        self.mode_box.addItem("")
        self.horizontalLayout_2.addWidget(self.mode_box)
        self.mode_btn = QtWidgets.QPushButton(self.widget)
        self.mode_btn.setObjectName("mode_btn")
        self.horizontalLayout_2.addWidget(self.mode_btn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.widget)
        self.verticalLayout.addWidget(self.widget_3)
        self.padSpec = QtWidgets.QWidget(controlSettings)
        self.padSpec.setObjectName("padSpec")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.padSpec)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.padSpec)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 69))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_4 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.e_deadzone = QtWidgets.QLineEdit(self.widget_4)
        self.e_deadzone.setObjectName("e_deadzone")
        self.horizontalLayout_5.addWidget(self.e_deadzone)
        self.verticalLayout_4.addWidget(self.widget_4)
        self.w_pad_select = QtWidgets.QWidget(self.groupBox_3)
        self.w_pad_select.setObjectName("w_pad_select")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_pad_select)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l_padStatus = QtWidgets.QLabel(self.w_pad_select)
        self.l_padStatus.setObjectName("l_padStatus")
        self.horizontalLayout.addWidget(self.l_padStatus)
        self.b_refresh = QtWidgets.QPushButton(self.w_pad_select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_refresh.sizePolicy().hasHeightForWidth())
        self.b_refresh.setSizePolicy(sizePolicy)
        self.b_refresh.setObjectName("b_refresh")
        self.horizontalLayout.addWidget(self.b_refresh)
        self.verticalLayout_4.addWidget(self.w_pad_select)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.padSpec)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 157))
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.e_roll = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.e_roll.setMinimum(0.0)
        self.e_roll.setMaximum(5.0)
        self.e_roll.setSingleStep(0.01)
        self.e_roll.setProperty("value", 2.0)
        self.e_roll.setObjectName("e_roll")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.e_roll)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.e_pitch = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.e_pitch.setWrapping(False)
        self.e_pitch.setFrame(True)
        self.e_pitch.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.e_pitch.setSpecialValueText("")
        self.e_pitch.setProperty("showGroupSeparator", False)
        self.e_pitch.setPrefix("")
        self.e_pitch.setSuffix("")
        self.e_pitch.setMinimum(0.0)
        self.e_pitch.setMaximum(5.0)
        self.e_pitch.setSingleStep(0.01)
        self.e_pitch.setProperty("value", 2.0)
        self.e_pitch.setObjectName("e_pitch")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.e_pitch)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.e_yaw = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.e_yaw.setMinimum(0.0)
        self.e_yaw.setMaximum(5.0)
        self.e_yaw.setSingleStep(0.01)
        self.e_yaw.setProperty("value", 2.0)
        self.e_yaw.setObjectName("e_yaw")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.e_yaw)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.e_throttle = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.e_throttle.setMinimum(0.0)
        self.e_throttle.setMaximum(5.0)
        self.e_throttle.setSingleStep(0.01)
        self.e_throttle.setProperty("value", 2.0)
        self.e_throttle.setObjectName("e_throttle")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.e_throttle)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label)
        self.e_vertical = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.e_vertical.setMinimum(0.0)
        self.e_vertical.setMaximum(5.0)
        self.e_vertical.setSingleStep(0.01)
        self.e_vertical.setProperty("value", 2.0)
        self.e_vertical.setObjectName("e_vertical")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.e_vertical)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.padSpec)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 157))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.l_roll = QtWidgets.QSpinBox(self.groupBox_2)
        self.l_roll.setPrefix("")
        self.l_roll.setProperty("value", 30)
        self.l_roll.setObjectName("l_roll")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.l_roll)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.l_pitch = QtWidgets.QSpinBox(self.groupBox_2)
        self.l_pitch.setProperty("value", 30)
        self.l_pitch.setObjectName("l_pitch")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.l_pitch)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.l_yaw = QtWidgets.QSpinBox(self.groupBox_2)
        self.l_yaw.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.l_yaw.setMaximum(1000)
        self.l_yaw.setProperty("value", 300)
        self.l_yaw.setObjectName("l_yaw")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.l_yaw)
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.l_vertical = QtWidgets.QSpinBox(self.groupBox_2)
        self.l_vertical.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.l_vertical.setMaximum(1000)
        self.l_vertical.setProperty("value", 500)
        self.l_vertical.setObjectName("l_vertical")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.l_vertical)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.l_throttle = QtWidgets.QSpinBox(self.groupBox_2)
        self.l_throttle.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.l_throttle.setAccelerated(False)
        self.l_throttle.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.l_throttle.setMaximum(1000)
        self.l_throttle.setSingleStep(10)
        self.l_throttle.setProperty("value", 600)
        self.l_throttle.setObjectName("l_throttle")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.l_throttle)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.padSpec)
        self.osdSettings = osdSettings(controlSettings)
        self.osdSettings.setObjectName("osdSettings")
        self.verticalLayout.addWidget(self.osdSettings)

        self.retranslateUi(controlSettings)
        QtCore.QMetaObject.connectSlotsByName(controlSettings)

    def retranslateUi(self, controlSettings):
        _translate = QtCore.QCoreApplication.translate
        controlSettings.setWindowTitle(_translate("controlSettings", "Form"))
        self.label_14.setText(_translate("controlSettings", "PID interval (ms):"))
        self.l_PIDInterval.setText(_translate("controlSettings", "20"))
        self.b_arm.setText(_translate("controlSettings", "Arm"))
        self.label_6.setText(_translate("controlSettings", "Control:"))
        self.s_control.setItemText(0, _translate("controlSettings", "Pad"))
        self.s_control.setItemText(1, _translate("controlSettings", "Keyboard"))
        self.s_control.setItemText(2, _translate("controlSettings", "Autonomy"))
        self.label_13.setText(_translate("controlSettings", "Interval (ms):"))
        self.l_interval.setText(_translate("controlSettings", "40"))
        self.b_start.setText(_translate("controlSettings", "Start"))
        self.label_15.setText(_translate("controlSettings", "Mode:"))
        self.mode_box.setItemText(0, _translate("controlSettings", "Stable"))
        self.mode_box.setItemText(1, _translate("controlSettings", "Acro"))
        self.mode_btn.setText(_translate("controlSettings", "SET"))
        self.label_7.setText(_translate("controlSettings", "Pad deadzone"))
        self.e_deadzone.setText(_translate("controlSettings", "2000"))
        self.l_padStatus.setText(_translate("controlSettings", "TextLabel"))
        self.b_refresh.setText(_translate("controlSettings", "Refresh"))
        self.groupBox.setTitle(_translate("controlSettings", "Expo"))
        self.label_2.setText(_translate("controlSettings", "Roll"))
        self.label_4.setText(_translate("controlSettings", "Pitch"))
        self.label_3.setText(_translate("controlSettings", "Yaw"))
        self.label_5.setText(_translate("controlSettings", "Throttle"))
        self.label.setText(_translate("controlSettings", "Vertical"))
        self.groupBox_2.setTitle(_translate("controlSettings", "Limits"))
        self.label_8.setText(_translate("controlSettings", "Roll angle"))
        self.l_roll.setSuffix(_translate("controlSettings", "°"))
        self.label_9.setText(_translate("controlSettings", "Pitch angle"))
        self.l_pitch.setSuffix(_translate("controlSettings", "°"))
        self.label_10.setText(_translate("controlSettings", "Yaw"))
        self.label_11.setText(_translate("controlSettings", "Vertical"))
        self.label_12.setText(_translate("controlSettings", "Throttle"))
from widgets.osdSettings import osdSettings


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    controlSettings = QtWidgets.QWidget()
    ui = Ui_controlSettings()
    ui.setupUi(controlSettings)
    controlSettings.show()
    sys.exit(app.exec_())
