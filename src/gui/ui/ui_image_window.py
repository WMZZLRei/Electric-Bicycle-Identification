from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImageDetectionUI(object):
    def __init__(self):
        """
        类的初始化方法。
        该方法初始化了与用户界面相关的多个属性，包括标签、按钮、编辑框等UI元素。
        属性列表：
        - labelPreview: 预览标签，用于显示预览内容。
        - buttonSavePath: 保存路径按钮，用于选择文件保存路径。
        - editSavePath: 保存路径编辑框，用于显示和修改文件的保存路径。
        - editConfidenceValue:置信度值编辑框，用于显示和修改置信度阈值。
        - confidenceSlider: 置信度滑块，用于通过可视化方式调整置信度阈值。
        - labelSavePath: 保存路径标签，用于显示保存路径的相关提示信息。
        - labelConfidence: 置信度标签，用于显示置信度的相关提示信息。
        - buttonFilePath: 文件路径按钮，用于选择文件路径。
        - labelFilePath: 文件路径标签，用于显示文件路径的相关提示信息。
        - editFilePath: 文件路径编辑框，用于显示和修改文件的路径。
        - widgetParameter: 参数 widget，用于显示和交互的参数设置界面。
        - buttonReset: 重置按钮，用于恢复到初始状态。
        - buttonStart: 启动按钮，用于开始相关进程。
        - widgetButton: 按钮 widget，包含了一系列操作按钮。
        - widgetInput: 输入 widget，用于处理用户输入。
        """
        self.labelPreview = None
        self.buttonSavePath = None
        self.editSavePath = None
        self.editConfidenceValue = None
        self.confidenceSlider = None
        self.labelSavePath = None
        self.labelConfidence = None
        self.buttonFilePath = None
        self.labelFilePath = None
        self.editFilePath = None
        self.widgetParameter = None
        self.buttonReset = None
        self.buttonStart = None
        self.widgetButton = None
        self.widgetInput = None


    def setupUi(self, ImageDetectionUI):
        ImageDetectionUI.setObjectName("ImageDetectionUI")
        ImageDetectionUI.resize(1250, 980)

        # 输入框区域
        self.widgetInput = QtWidgets.QWidget(ImageDetectionUI)
        self.widgetInput.setGeometry(QtCore.QRect(9, 9, 891, 210))
        self.widgetInput.setObjectName("widgetInput")

        # 按钮区域
        self.widgetButton = QtWidgets.QWidget(self.widgetInput)
        self.widgetButton.setGeometry(QtCore.QRect(0, 0, 151, 211))
        self.widgetButton.setObjectName("widgetButton")

        # 检测按钮
        self.buttonStart = QtWidgets.QPushButton(self.widgetButton)
        self.buttonStart.setGeometry(QtCore.QRect(0, 0, 150, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.buttonStart.setFont(font)
        self.buttonStart.setObjectName("buttonStart")

        # 重置按钮
        self.buttonReset = QtWidgets.QPushButton(self.widgetButton)
        self.buttonReset.setGeometry(QtCore.QRect(0, 110, 150, 100))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        self.buttonReset.setFont(font)
        self.buttonReset.setObjectName("buttonReset")

        # 参数区域
        self.widgetParameter = QtWidgets.QWidget(self.widgetInput)
        self.widgetParameter.setGeometry(QtCore.QRect(150, 0, 741, 210))
        self.widgetParameter.setObjectName("widgetParameter")

        # 文件路径输入框
        self.editFilePath = QtWidgets.QLineEdit(self.widgetParameter)
        self.editFilePath.setGeometry(QtCore.QRect(130, 10, 511, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editFilePath.setFont(font)
        self.editFilePath.setObjectName("editFilePath")

        # 文件路径文本框
        self.labelFilePath = QtWidgets.QLabel(self.widgetParameter)
        self.labelFilePath.setGeometry(QtCore.QRect(0, 0, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelFilePath.setFont(font)
        self.labelFilePath.setObjectName("labelFilePath")

        # 文件路径打开按钮
        self.buttonFilePath = QtWidgets.QPushButton(self.widgetParameter)
        self.buttonFilePath.setGeometry(QtCore.QRect(650, 10, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonFilePath.setFont(font)
        self.buttonFilePath.setObjectName("buttonFilePath")

        # 置信度文本框
        self.labelConfidence = QtWidgets.QLabel(self.widgetParameter)
        self.labelConfidence.setGeometry(QtCore.QRect(0, 70, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelConfidence.setFont(font)
        self.labelConfidence.setObjectName("labelConfidence")

        # 保存路径文本框
        self.labelSavePath = QtWidgets.QLabel(self.widgetParameter)
        self.labelSavePath.setGeometry(QtCore.QRect(0, 150, 121, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.labelSavePath.setFont(font)
        self.labelSavePath.setObjectName("labelSavePath")

        # 置信度滑动条
        self.confidenceSlider = QtWidgets.QSlider(self.widgetParameter)
        self.confidenceSlider.setGeometry(QtCore.QRect(129, 90, 511, 22))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.confidenceSlider.setFont(font)
        self.confidenceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.confidenceSlider.setObjectName("confidenceSlider")
        self.confidenceSlider.setValue(60)

        # 置信度输入框
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

        # 保存路径输入框
        self.editSavePath = QtWidgets.QLineEdit(self.widgetParameter)
        self.editSavePath.setGeometry(QtCore.QRect(130, 160, 511, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editSavePath.setFont(font)
        self.editSavePath.setObjectName("editSavePath")

        # 保存路径打开按钮
        self.buttonSavePath = QtWidgets.QPushButton(self.widgetParameter)
        self.buttonSavePath.setGeometry(QtCore.QRect(650, 160, 81, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.buttonSavePath.setFont(font)
        self.buttonSavePath.setObjectName("buttonSavePath")

        # 输出区域
        self.labelOutput = QtWidgets.QLabel(ImageDetectionUI)
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

        # 预览区域
        self.labelPreview = QtWidgets.QLabel(ImageDetectionUI)
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

        self.retranslateUi(ImageDetectionUI)
        QtCore.QMetaObject.connectSlotsByName(ImageDetectionUI)

    def retranslateUi(self, ImageDetectionUI):
        _translate = QtCore.QCoreApplication.translate
        ImageDetectionUI.setWindowTitle(_translate("ImageDetectionUI", "图片检测窗口"))
        self.buttonStart.setText(_translate("ImageDetectionUI", "检测"))
        self.buttonReset.setText(_translate("ImageDetectionUI", "重置"))
        self.labelFilePath.setText(_translate("ImageDetectionUI", "  文件路径："))
        self.buttonFilePath.setText(_translate("ImageDetectionUI", "打开"))
        self.labelConfidence.setText(_translate("ImageDetectionUI", "  置信度："))
        self.labelSavePath.setText(_translate("ImageDetectionUI", "  保存路径："))
        self.editConfidenceValue.setText(_translate("ImageDetectionUI", "0.60"))
        self.buttonSavePath.setText(_translate("ImageDetectionUI", "打开"))
        self.labelOutput.setText(_translate("ImageDetectionUI", "请选择图片"))
        self.labelPreview.setText(_translate("ImageDetectionUI", "图片检测"))
