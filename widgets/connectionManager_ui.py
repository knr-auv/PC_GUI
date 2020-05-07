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
        connectionManager.resize(640, 480)
        self.horizontalLayout = QtWidgets.QHBoxLayout(connectionManager)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.b_start_sending = QtWidgets.QPushButton(connectionManager)
        self.b_start_sending.setObjectName("b_start_sending")
        self.horizontalLayout.addWidget(self.b_start_sending)

        self.retranslateUi(connectionManager)
        QtCore.QMetaObject.connectSlotsByName(connectionManager)

    def retranslateUi(self, connectionManager):
        _translate = QtCore.QCoreApplication.translate
        connectionManager.setWindowTitle(_translate("connectionManager", "Form"))
        self.b_start_sending.setText(_translate("connectionManager", "Start telemetry"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectionManager = QtWidgets.QWidget()
    ui = Ui_connectionManager()
    ui.setupUi(connectionManager)
    connectionManager.show()
    sys.exit(app.exec_())
