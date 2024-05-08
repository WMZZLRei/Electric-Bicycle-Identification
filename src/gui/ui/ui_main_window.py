from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap

from .icon_base64_data import base64_image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)
        MainWindow.setWindowTitle("电动自行车识别系统")
        icon_data = base64_image()
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        MainWindow.setWindowIcon(QIcon(pixmap))
        # 创建stackedWidget
        self.stackedWidget = QtWidgets.QStackedWidget(MainWindow)
        self.stackedWidget.setGeometry(QtCore.QRect(340, 9, 1250, 980))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.stackedWidget.setFont(font)
        self.stackedWidget.setObjectName("stackedWidget")
        # 创建switchWidget
        self.switchWidget = QtWidgets.QWidget(MainWindow)
        self.switchWidget.setGeometry(QtCore.QRect(10, 10, 320, 991))
        self.switchWidget.setObjectName("switchWidget")
        # 创建switchButton
        self.switchImageDetection = QtWidgets.QPushButton(self.switchWidget)
        self.switchImageDetection.setGeometry(QtCore.QRect(0, 0, 320, 280))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(30)
        self.switchImageDetection.setFont(font)
        self.switchImageDetection.setObjectName("switchImageDetection")
        # 创建switchButton
        self.switchVideoDetection = QtWidgets.QPushButton(self.switchWidget)
        self.switchVideoDetection.setGeometry(QtCore.QRect(0, 320, 320, 280))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.switchVideoDetection.setFont(font)
        self.switchVideoDetection.setObjectName("switchVideoDetection")
        # 创建switchButton
        self.switchCameraDetection = QtWidgets.QPushButton(self.switchWidget)
        self.switchCameraDetection.setGeometry(QtCore.QRect(0, 640, 320, 280))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(30)
        self.switchCameraDetection.setFont(font)
        self.switchCameraDetection.setObjectName("switchCameraDetection")
        # 创建switchButton
        self.switchAboutMe = QtWidgets.QPushButton(self.switchWidget)
        self.switchAboutMe.setGeometry(QtCore.QRect(0, 952, 320, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.switchAboutMe.setFont(font)
        self.switchAboutMe.setObjectName("switchAboutMe")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "电动自行车识别系统"))
        self.switchImageDetection.setText(_translate("MainWindow", "图片检测"))
        self.switchVideoDetection.setText(_translate("MainWindow", "视频检测"))
        self.switchCameraDetection.setText(_translate("MainWindow", "摄像头检测"))
        self.switchAboutMe.setText(_translate("MainWindow", "关于我"))
