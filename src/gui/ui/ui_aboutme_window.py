from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutMe(object):
    def setupUi(self, AboutMe):
        AboutMe.setObjectName("AboutMe")
        AboutMe.resize(1250, 980)
        self.label = QtWidgets.QLabel(AboutMe)
        self.label.setGeometry(QtCore.QRect(230, 340, 781, 211))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {\n"
                                 "    qproperty-alignment: AlignCenter;\n"
                                 "    padding-top: 5px; /* 垂直居中对齐时可能需要调整上边距 */\n"
                                 "    padding-bottom: 5px; /* 垂直居中对齐时可能需要调整下边距 */\n"
                                 "}\n"
                                 "")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(AboutMe)
        self.label_3.setGeometry(QtCore.QRect(1000, 940, 241, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(AboutMe)
        QtCore.QMetaObject.connectSlotsByName(AboutMe)

    def retranslateUi(self, AboutMe):
        _translate = QtCore.QCoreApplication.translate
        AboutMe.setWindowTitle(_translate("AboutMe", "Form"))
        self.label.setText(_translate("AboutMe", "电动自行车识别系统"))
        self.label_3.setText(_translate("AboutMe", "GitHubID:WMZZLRei"))
