# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiFiles/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 843)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connectionBar = connectionBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectionBar.sizePolicy().hasHeightForWidth())
        self.connectionBar.setSizePolicy(sizePolicy)
        self.connectionBar.setMinimumSize(QtCore.QSize(0, 0))
        self.connectionBar.setObjectName("connectionBar")
        self.verticalLayout.addWidget(self.connectionBar)
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setAutoFillBackground(False)
        self.tabs.setStyleSheet("")
        self.tabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabs.setObjectName("tabs")
        self.test = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.test.sizePolicy().hasHeightForWidth())
        self.test.setSizePolicy(sizePolicy)
        self.test.setObjectName("test")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.test)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dataBox = QtWidgets.QFrame(self.test)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataBox.sizePolicy().hasHeightForWidth())
        self.dataBox.setSizePolicy(sizePolicy)
        self.dataBox.setMinimumSize(QtCore.QSize(500, 700))
        self.dataBox.setMaximumSize(QtCore.QSize(500, 16777215))
        self.dataBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dataBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dataBox.setObjectName("dataBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dataBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.engineData = engineData(self.dataBox)
        self.engineData.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.engineData.sizePolicy().hasHeightForWidth())
        self.engineData.setSizePolicy(sizePolicy)
        self.engineData.setMinimumSize(QtCore.QSize(419, 465))
        self.engineData.setMaximumSize(QtCore.QSize(419, 465))
        self.engineData.setBaseSize(QtCore.QSize(400, 400))
        self.engineData.setObjectName("engineData")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.engineData)
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2.addWidget(self.engineData)
        self.boatData = boatData(self.dataBox)
        self.boatData.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boatData.sizePolicy().hasHeightForWidth())
        self.boatData.setSizePolicy(sizePolicy)
        self.boatData.setMinimumSize(QtCore.QSize(419, 200))
        self.boatData.setMaximumSize(QtCore.QSize(419, 16777215))
        self.boatData.setBaseSize(QtCore.QSize(419, 400))
        self.boatData.setObjectName("boatData")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.boatData)
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2.addWidget(self.boatData)
        self.horizontalLayout.addWidget(self.dataBox)
        self.cameraContainer = QtWidgets.QWidget(self.test)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cameraContainer.sizePolicy().hasHeightForWidth())
        self.cameraContainer.setSizePolicy(sizePolicy)
        self.cameraContainer.setMinimumSize(QtCore.QSize(416, 534))
        self.cameraContainer.setObjectName("cameraContainer")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.cameraContainer)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout.addWidget(self.cameraContainer)
        self.tabs.addTab(self.test, "")
        self.PID = QtWidgets.QWidget()
        self.PID.setObjectName("PID")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.PID)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pidDataBox = QtWidgets.QFrame(self.PID)
        self.pidDataBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pidDataBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pidDataBox.setObjectName("pidDataBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pidDataBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pidSetup = QtWidgets.QWidget(self.pidDataBox)
        self.pidSetup.setObjectName("pidSetup")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pidSetup)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.pidSetup)
        self.pidBoatData = QtWidgets.QWidget(self.pidDataBox)
        self.pidBoatData.setObjectName("pidBoatData")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.pidBoatData)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_3.addWidget(self.pidBoatData)
        self.horizontalLayout_5.addWidget(self.pidDataBox)
        self.plots = QtWidgets.QWidget(self.PID)
        self.plots.setObjectName("plots")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.plots)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5.addWidget(self.plots)
        self.tabs.addTab(self.PID, "")
        self.control = QtWidgets.QWidget()
        self.control.setObjectName("control")
        self.tabs.addTab(self.control, "")
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Okoń"))
        self.tabs.setTabText(self.tabs.indexOf(self.test), _translate("MainWindow", "Test"))
        self.tabs.setTabText(self.tabs.indexOf(self.PID), _translate("MainWindow", "PID"))
        self.tabs.setTabText(self.tabs.indexOf(self.control), _translate("MainWindow", "Control"))
from widgets.boatData import boatData
from widgets.connectionBar import connectionBar
from widgets.engineData import engineData


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
