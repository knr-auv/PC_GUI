# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiFiles/cameraContainer.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_cameraContainer(object):
    def setupUi(self, cameraContainer):
        cameraContainer.setObjectName("cameraContainer")
        cameraContainer.resize(658, 531)
        self.verticalLayout = QtWidgets.QVBoxLayout(cameraContainer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameWidget = QtWidgets.QWidget(cameraContainer)
        self.frameWidget.setObjectName("frameWidget")
        self.verticalLayout.addWidget(self.frameWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clientData = QtWidgets.QLineEdit(cameraContainer)
        self.clientData.setObjectName("clientData")
        self.horizontalLayout.addWidget(self.clientData)
        self.connectButton = QtWidgets.QPushButton(cameraContainer)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(cameraContainer)
        QtCore.QMetaObject.connectSlotsByName(cameraContainer)

    def retranslateUi(self, cameraContainer):
        _translate = QtCore.QCoreApplication.translate
        cameraContainer.setWindowTitle(_translate("cameraContainer", "Form"))
        self.clientData.setText(_translate("cameraContainer", "127.0.0.1:44209"))
        self.connectButton.setText(_translate("cameraContainer", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    cameraContainer = QtWidgets.QWidget()
    ui = Ui_cameraContainer()
    ui.setupUi(cameraContainer)
    cameraContainer.show()
    sys.exit(app.exec_())
