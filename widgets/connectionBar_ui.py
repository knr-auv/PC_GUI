# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UiFiles\connectionBar.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_connectionBar(object):
    def setupUi(self, connectionBar):
        connectionBar.setObjectName("connectionBar")
        connectionBar.resize(984, 174)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(connectionBar.sizePolicy().hasHeightForWidth())
        connectionBar.setSizePolicy(sizePolicy)
        connectionBar.setMinimumSize(QtCore.QSize(0, 0))
        connectionBar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        connectionBar.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(connectionBar)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l_connection = QtWidgets.QLabel(connectionBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_connection.sizePolicy().hasHeightForWidth())
        self.l_connection.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.l_connection.setFont(font)
        self.l_connection.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.l_connection.setObjectName("l_connection")
        self.horizontalLayout.addWidget(self.l_connection)
        self.l_ip = QtWidgets.QLabel(connectionBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_ip.sizePolicy().hasHeightForWidth())
        self.l_ip.setSizePolicy(sizePolicy)
        self.l_ip.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.l_ip.setFont(font)
        self.l_ip.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_ip.setObjectName("l_ip")
        self.horizontalLayout.addWidget(self.l_ip)
        self.ip_text = QtWidgets.QLineEdit(connectionBar)
        self.ip_text.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ip_text.sizePolicy().hasHeightForWidth())
        self.ip_text.setSizePolicy(sizePolicy)
        self.ip_text.setMinimumSize(QtCore.QSize(100, 20))
        self.ip_text.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ip_text.setFont(font)
        self.ip_text.setInputMask("")
        self.ip_text.setAlignment(QtCore.Qt.AlignCenter)
        self.ip_text.setObjectName("ip_text")
        self.horizontalLayout.addWidget(self.ip_text)
        self.b_connect = QtWidgets.QPushButton(connectionBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_connect.sizePolicy().hasHeightForWidth())
        self.b_connect.setSizePolicy(sizePolicy)
        self.b_connect.setAutoFillBackground(False)
        self.b_connect.setStyleSheet("")
        self.b_connect.setObjectName("b_connect")
        self.horizontalLayout.addWidget(self.b_connect)

        self.retranslateUi(connectionBar)
        QtCore.QMetaObject.connectSlotsByName(connectionBar)

    def retranslateUi(self, connectionBar):
        _translate = QtCore.QCoreApplication.translate
        connectionBar.setWindowTitle(_translate("connectionBar", "connectionBar"))
        self.l_connection.setText(_translate("connectionBar", "Connection info"))
        self.l_ip.setText(_translate("connectionBar", "IP:"))
        self.ip_text.setText(_translate("connectionBar", "localhost:8080"))
        self.b_connect.setText(_translate("connectionBar", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectionBar = QtWidgets.QWidget()
    ui = Ui_connectionBar()
    ui.setupUi(connectionBar)
    connectionBar.show()
    sys.exit(app.exec_())
