from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoDetectionUI(object):
    def setupUi(self, VideoDetectionUI):
        # 设置主窗口的名称和大小
        VideoDetectionUI.setObjectName("VideoDetectionUI")
        VideoDetectionUI.resize(1250, 980)

        # 设置输入部件
        self.widgetInput = QtWidgets.QWidget(VideoDetectionUI)
        self.widgetInput.setGeometry(QtCore.QRect(9, 9, 891, 210))
        self.widgetInput.setObjectName("widgetInput")

        # 设置按钮部件
        self.widgetButton = QtWidgets.QWidget(self.widgetInput)
        self.widgetButton.setGeometry(QtCore.QRect(0, 0, 151, 211))
        self.widgetButton.setObjectName("widgetButton")

        # 设置开始按钮
        self.buttonStart = QtWidgets.QPushButton(self.widgetButton)
        self.buttonStart.setGeometry(QtCore.QRect(0, 0, 150, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.buttonStart.setFont(font)
        self.buttonStart.setObjectName("buttonStart")

        # 设置重置按钮
        self.buttonReset = QtWidgets.QPushButton(self.widgetButton)
        self.buttonReset.setGeometry(QtCore.QRect(0, 110, 150, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.buttonReset.setFont(font)
        self.buttonReset.setObjectName("buttonReset")

        # 设置参数部件
        self.widgetParameter = QtWidgets.QWidget(self.widgetInput)
        self.widgetParameter.setGeometry(QtCore.QRect(150, 0, 741, 210))
        self.widgetParameter.setObjectName("widgetParameter")

        # 设置文件路径编辑框
        self.editFilePath = QtWidgets.QLineEdit(self.widgetParameter)
        self.editFilePath.setGeometry(QtCore.QRect(130, 10, 511, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editFilePath.setFont(font)
        self.editFilePath.setObjectName("editFilePath")

        # 设置文件路径标签
        self.labelFilePath = QtWidgets.QLabel(self.widgetParameter)
        self.labelFilePath.setGeometry(QtCore.QRect(0, 0, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelFilePath.setFont(font)
        self.labelFilePath.setObjectName("labelFilePath")

        # 设置打开文件按钮
        self.buttonFilePath = QtWidgets.QPushButton(self.widgetParameter)
        self.buttonFilePath.setGeometry(QtCore.QRect(650, 10, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonFilePath.setFont(font)
        self.buttonFilePath.setObjectName("buttonFilePath")

        # 设置置信度标签
        self.labelConfidence = QtWidgets.QLabel(self.widgetParameter)
        self.labelConfidence.setGeometry(QtCore.QRect(0, 70, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelConfidence.setFont(font)
        self.labelConfidence.setObjectName("labelConfidence")

        # 设置保存路径标签
        self.labelSavePath = QtWidgets.QLabel(self.widgetParameter)
        self.labelSavePath.setGeometry(QtCore.QRect(0, 150, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelSavePath.setFont(font)
        self.labelSavePath.setObjectName("labelSavePath")

        # 设置置信度滑块
        self.confidenceSlider = QtWidgets.QSlider(self.widgetParameter)
        self.confidenceSlider.setGeometry(QtCore.QRect(129, 90, 511, 22))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.confidenceSlider.setFont(font)
        self.confidenceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.confidenceSlider.setObjectName("confidenceSlider")
        self.confidenceSlider.setValue(60)

        # 设置置信度编辑框
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

        # 设置保存路径编辑框
        self.editSavePath = QtWidgets.QLineEdit(self.widgetParameter)
        self.editSavePath.setGeometry(QtCore.QRect(130, 160, 511, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editSavePath.setFont(font)
        self.editSavePath.setObjectName("editSavePath")

        # 设置打开保存路径按钮
        self.buttonSavePath = QtWidgets.QPushButton(self.widgetParameter)
        self.buttonSavePath.setGeometry(QtCore.QRect(650, 160, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonSavePath.setFont(font)
        self.buttonSavePath.setObjectName("buttonSavePath")

        # 设置输出标签
        self.labelOutput = QtWidgets.QLabel(VideoDetectionUI)
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

        # 视频播放标签


        # 设置预览标签
        self.labelPreview = QtWidgets.QLabel(VideoDetectionUI)
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

        self.retranslateUi(VideoDetectionUI)
        QtCore.QMetaObject.connectSlotsByName(VideoDetectionUI)

    def retranslateUi(self, VideoDetectionUI):
        _translate = QtCore.QCoreApplication.translate
        VideoDetectionUI.setWindowTitle(_translate("VideoDetectionUI", "Form"))
        self.buttonStart.setText(_translate("VideoDetectionUI", "检测"))
        self.buttonReset.setText(_translate("VideoDetectionUI", "重置"))
        self.labelFilePath.setText(_translate("VideoDetectionUI", "  文件路径："))
        self.buttonFilePath.setText(_translate("VideoDetectionUI", "打开"))
        self.labelConfidence.setText(_translate("VideoDetectionUI", "  置信度："))
        self.labelSavePath.setText(_translate("VideoDetectionUI", "  保存路径："))
        self.editConfidenceValue.setText(_translate("VideoDetectionUI", "0.60"))
        self.buttonSavePath.setText(_translate("VideoDetectionUI", "打开"))
        self.labelOutput.setText(_translate("VideoDetectionUI", "请选择视频"))
        self.labelPreview.setText(_translate("VideoDetectionUI", "视频检测"))
