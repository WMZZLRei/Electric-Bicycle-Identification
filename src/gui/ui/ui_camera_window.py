from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CameraDetectionUI(object):
    def setupUi(self, CameraDetectionUI):
        """
        初始化摄像头检测用户界面的布局和组件。

        参数:
        - CameraDetectionUI: 窗口对象，是用户界面的容器。
        """
        CameraDetectionUI.setObjectName("CameraDetectionUI")
        CameraDetectionUI.resize(1250, 980)
        # 输入区域布局
        self.widgetInput = QtWidgets.QWidget(CameraDetectionUI)
        self.widgetInput.setGeometry(QtCore.QRect(9, 9, 891, 210))
        self.widgetInput.setObjectName("widgetInput")

        # 按钮区域布局
        self.widgetButton = QtWidgets.QWidget(self.widgetInput)
        self.widgetButton.setGeometry(QtCore.QRect(0, 0, 151, 211))
        self.widgetButton.setObjectName("widgetButton")

        # 启动按钮
        self.buttonStart = QtWidgets.QPushButton(self.widgetButton)
        self.buttonStart.setGeometry(QtCore.QRect(0, 0, 150, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.buttonStart.setFont(font)
        self.buttonStart.setObjectName("buttonStart")

        # 停止按钮
        self.buttonStop = QtWidgets.QPushButton(self.widgetButton)
        self.buttonStop.setGeometry(QtCore.QRect(0, 110, 150, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.buttonStop.setFont(font)
        self.buttonStop.setObjectName("buttonStop")

        # 参数区域布局
        self.widgetParameter = QtWidgets.QWidget(self.widgetInput)
        self.widgetParameter.setGeometry(QtCore.QRect(150, 0, 741, 210))
        self.widgetParameter.setObjectName("widgetParameter")

        # 摄像头设备下拉菜单栏
        self.comboboxCamera = QtWidgets.QComboBox(self.widgetParameter)
        self.comboboxCamera.setGeometry(QtCore.QRect(130, 10, 511, 31))
        self.comboboxList = ["未检测到摄像头，请检查是否有摄像头设备"]
        self.comboboxCamera.addItems(self.comboboxList)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.comboboxCamera.setFont(font)
        self.comboboxCamera.setObjectName("comboboxCamera")

        # 摄像头设备标签
        self.labelCamera = QtWidgets.QLabel(self.widgetParameter)
        self.labelCamera.setGeometry(QtCore.QRect(0, 0, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelCamera.setFont(font)
        self.labelCamera.setObjectName("labelCamera")

        # 摄像头设备按钮
        self.buttonCamera = QtWidgets.QPushButton(self.widgetParameter)
        self.buttonCamera.setGeometry(QtCore.QRect(650, 10, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonCamera.setFont(font)
        self.buttonCamera.setObjectName("buttonCamera")

        # 置信度标签
        self.labelConfidence = QtWidgets.QLabel(self.widgetParameter)
        self.labelConfidence.setGeometry(QtCore.QRect(0, 70, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelConfidence.setFont(font)
        self.labelConfidence.setObjectName("labelConfidence")

        # 保存路径标签
        self.labelSavePath = QtWidgets.QLabel(self.widgetParameter)
        self.labelSavePath.setGeometry(QtCore.QRect(0, 150, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelSavePath.setFont(font)
        self.labelSavePath.setObjectName("labelSavePath")

        # 置信度滑块
        self.confidenceSlider = QtWidgets.QSlider(self.widgetParameter)
        self.confidenceSlider.setGeometry(QtCore.QRect(129, 90, 511, 22))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.confidenceSlider.setFont(font)
        self.confidenceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.confidenceSlider.setObjectName("confidenceSlider")
        self.confidenceSlider.setValue(60)

        # 置信度值编辑框
        self.editConfidenceValue = QtWidgets.QLineEdit(self.widgetParameter)
        self.editConfidenceValue.setGeometry(QtCore.QRect(650, 79, 81, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editConfidenceValue.setFont(font)
        self.editConfidenceValue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.editConfidenceValue.setStyleSheet("QLineEdit {\n"
                                               "    qproperty-alignment: AlignCenter;\n"
                                               "    padding-top: 5px; /* 垂直居中对齐时可能需要调整上边距 */\n"
                                               "    padding-bottom: 5px; /* 垂直居中对齐时可能需要调整下边距 */\n"
                                               "}\n"
                                               "")
        self.editConfidenceValue.setObjectName("editConfidenceValue")

        # 保存路径编辑框
        self.editSavePath = QtWidgets.QLineEdit(self.widgetParameter)
        self.editSavePath.setGeometry(QtCore.QRect(130, 160, 511, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editSavePath.setFont(font)
        self.editSavePath.setObjectName("editSavePath")

        # 保存路径按钮
        self.buttonSavePath = QtWidgets.QPushButton(self.widgetParameter)
        self.buttonSavePath.setGeometry(QtCore.QRect(650, 160, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonSavePath.setFont(font)
        self.buttonSavePath.setObjectName("buttonSavePath")

        # 输出标签
        self.labelOutput = QtWidgets.QLabel(CameraDetectionUI)
        self.labelOutput.setGeometry(QtCore.QRect(13, 221, 1231, 751))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(48)
        self.labelOutput.setFont(font)
        self.labelOutput.setStyleSheet("QLabel {\n"
                                       "    qproperty-alignment: AlignCenter;\n"
                                       "    padding-top: 5px; /* 垂直居中对齐时可能需要调整上边距 */\n"
                                       "    padding-bottom: 5px; /* 垂直居中对齐时可能需要调整下边距 */\n"
                                       "}\n"
                                       "")
        self.labelOutput.setObjectName("labelOutput")

        # 预览标签
        self.labelPreview = QtWidgets.QLabel(CameraDetectionUI)
        self.labelPreview.setGeometry(QtCore.QRect(900, 10, 345, 210))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(30)
        self.labelPreview.setFont(font)
        self.labelPreview.setStyleSheet("QLabel {\n"
                                        "    qproperty-alignment: AlignCenter;\n"
                                        "    padding-top: 5px; /* 垂直居中对齐时可能需要调整上边距 */\n"
                                        "    padding-bottom: 5px; /* 垂直居中对齐时可能需要调整下边距 */\n"
                                        "}\n"
                                        "")
        self.labelPreview.setObjectName("labelPreview")

        self.retranslateUi(CameraDetectionUI)
        QtCore.QMetaObject.connectSlotsByName(CameraDetectionUI)

    def retranslateUi(self, CameraDetectionUI):
        """
        翻译用户界面的文本。

        参数:
        - CameraDetectionUI: 窗口对象，需要对其组件进行文本翻译。
        """
        _translate = QtCore.QCoreApplication.translate
        CameraDetectionUI.setWindowTitle(_translate("CameraDetectionUI", "Form"))
        self.buttonStart.setText(_translate("CameraDetectionUI", "检测"))
        self.buttonStop.setText(_translate("CameraDetectionUI", "停止"))
        self.labelCamera.setText(_translate("CameraDetectionUI", "  摄像头："))
        self.buttonCamera.setText(_translate("CameraDetectionUI", "刷新"))
        self.labelConfidence.setText(_translate("CameraDetectionUI", "  置信度："))
        self.labelSavePath.setText(_translate("CameraDetectionUI", "  保存路径："))
        self.editConfidenceValue.setText(_translate("CameraDetectionUI", "0.60"))
        self.buttonSavePath.setText(_translate("CameraDetectionUI", "打开"))
        self.labelOutput.setText(_translate("CameraDetectionUI", "请开启检测"))
        self.labelPreview.setText(_translate("CameraDetectionUI", "摄像头检测"))
