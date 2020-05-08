# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiFiles/connectionManager.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_connectionManager(object):
    def setupUi(self, connectionManager):
        connectionManager.setObjectName("connectionManager")
        connectionManager.resize(765, 250)
        connectionManager.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(connectionManager)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(connectionManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(557, 0))
        self.widget.setMaximumSize(QtCore.QSize(557, 16777215))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l_interval = QtWidgets.QLabel(self.widget)
        self.l_interval.setMinimumSize(QtCore.QSize(70, 23))
        self.l_interval.setMaximumSize(QtCore.QSize(70, 23))
        self.l_interval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_interval.setObjectName("l_interval")
        self.horizontalLayout.addWidget(self.l_interval)
        self.t_interval = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.t_interval.sizePolicy().hasHeightForWidth())
        self.t_interval.setSizePolicy(sizePolicy)
        self.t_interval.setMinimumSize(QtCore.QSize(0, 20))
        self.t_interval.setMaximumSize(QtCore.QSize(133, 20))
        self.t_interval.setAlignment(QtCore.Qt.AlignCenter)
        self.t_interval.setObjectName("t_interval")
        self.horizontalLayout.addWidget(self.t_interval)
        self.b_start_sending = QtWidgets.QPushButton(self.widget)
        self.b_start_sending.setMinimumSize(QtCore.QSize(130, 23))
        self.b_start_sending.setMaximumSize(QtCore.QSize(130, 23))
        self.b_start_sending.setObjectName("b_start_sending")
        self.horizontalLayout.addWidget(self.b_start_sending)
        self.b_stop_sending = QtWidgets.QPushButton(self.widget)
        self.b_stop_sending.setMinimumSize(QtCore.QSize(129, 23))
        self.b_stop_sending.setMaximumSize(QtCore.QSize(129, 23))
        self.b_stop_sending.setObjectName("b_stop_sending")
        self.horizontalLayout.addWidget(self.b_stop_sending)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(connectionManager)
        QtCore.QMetaObject.connectSlotsByName(connectionManager)

    def retranslateUi(self, connectionManager):
        _translate = QtCore.QCoreApplication.translate
        connectionManager.setWindowTitle(_translate("connectionManager", "Form"))
        self.l_interval.setText(_translate("connectionManager", "Interval (ms):"))
        self.t_interval.setText(_translate("connectionManager", "30"))
        self.b_start_sending.setText(_translate("connectionManager", "Start telemetry"))
        self.b_stop_sending.setText(_translate("connectionManager", "Stop telemetry"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectionManager = QtWidgets.QWidget()
    ui = Ui_connectionManager()
    ui.setupUi(connectionManager)
    connectionManager.show()
    sys.exit(app.exec_())
