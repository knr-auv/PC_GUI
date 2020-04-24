# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cameraContainer.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_cameraContainer(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(658, 531)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.framelabel = QtWidgets.QLabel(Form)
        self.framelabel.setMinimumSize(QtCore.QSize(640, 480))
        self.framelabel.setObjectName("framelabel")
        self.verticalLayout.addWidget(self.framelabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clientData = QtWidgets.QLineEdit(Form)
        self.clientData.setObjectName("clientData")
        self.horizontalLayout.addWidget(self.clientData)
        self.connectButton = QtWidgets.QPushButton(Form)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.framelabel.setText(_translate("Form", "framelabel"))
        self.clientData.setText(_translate("Form", "127.0.0.1:8485"))
        self.connectButton.setText(_translate("Form", "Connect"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     cameraContainer = QtWidgets.QWidget()
#     ui = Ui_cameraContainer()
#     ui.setupUi(cameraContainer)
#     cameraContainer.show()
#     sys.exit(app.exec_())