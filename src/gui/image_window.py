import os

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QDialog

from .ui import Ui_ImageDetectionUI
from src.utils import ObjectDetector


class ImageDetectionWindow(QWidget):
    """
    图片检测窗口类
    """
    progress_message_box = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_ImageDetectionUI()
        self.ui.setupUi(self)

        # 文件路径按钮点击事件
        self.ui.buttonFilePath.clicked.connect(self.open_file_dialog)  # 选择图片文件路径
        self.ui.editFilePath.returnPressed.connect(self.is_valid_image_file)  # 图片文件合法性验证(回车)
        self.ui.editFilePath.editingFinished.connect(self.is_valid_image_file)  # 图片文件合法性验证(失去焦点)

        self.ui.buttonSavePath.clicked.connect(self.select_save_folder)  # 选择保存路径
        self.ui.editSavePath.returnPressed.connect(self.is_valid_save_file)  # 保存文件夹路径合法性验证(回车)
        self.ui.editSavePath.editingFinished.connect(self.is_valid_save_file)  # 输入合法性验证(失去焦点)

        # 滑块绑定
        self.ui.confidenceSlider.setMinimum(0)
        self.ui.confidenceSlider.setMaximum(100)
        self.ui.confidenceSlider.setSingleStep(1)
        self.ui.confidenceSlider.valueChanged.connect(self.update_confidence_value_text)
        # 滑块输入验证
        self.ui.editConfidenceValue.returnPressed.connect(self.update_confidence_slider_position_from_textbox)
        self.ui.editConfidenceValue.editingFinished.connect(self.update_confidence_slider_position_from_textbox)

        # 检测按钮点击事件
        self.ui.buttonStart.clicked.connect(self.start_detection)

        # 重置按钮点击事件
        self.ui.buttonReset.clicked.connect(self.reset_values)

        # 允许的文件扩展名
        self.allowed_extensions = ['jpg', 'jpeg', 'png']

        # 初始化检测器
        self.predictor = None

        # 初始化进度框
        self.progress_dialog = ProgressDialog()

    def open_file_dialog(self):
        """
        打开文件对话框，限制选择文件类型为 .jpg, .jpeg, .png。
        选中后，将文件路径更新到 `editFilePath` 控件中。
        """
        dialog = QFileDialog(self)
        dialog.setNameFilter(f"Image Files ({' '.join(['*.' + ext for ext in self.allowed_extensions])})")

        if dialog.exec_():
            selected_file = dialog.selectedFiles()[0]  # 获取第一个（也是唯一一个）选择的文件路径
            self.update_file_path(selected_file)  # 直接更新文件路径

            self.display_image(selected_file, self.ui.labelPreview)  # 更新预览图片

    def is_valid_save_file(self):
        if not self.ui.editSavePath.text() or not os.path.isdir(self.ui.editSavePath.text()):
            # 判断保存路径是否为空或者不是一个文件夹
            self.show_warning_message(
                title="保存路径错误",
                message="请选择有效的保存路径。"
            )
            return False

        return True

    def is_valid_image_file(self, file_path: str) -> bool:
        """
        检查文件路径是否指向一个允许的图像文件类型。
        参数:
        - file_path (str): 要检查的文件路径。

        返回:
        - bool: 如果文件类型有效，则返回True；否则返回False。
        """
        file_extension = os.path.splitext(file_path)[1].lower()  # 将扩展名转换为小写
        allowed_extensions_lower = ['.' + ext.lower() for ext in self.allowed_extensions]  # 在每个元素前添加点号，并将列表中的每个元素转换为小写

        if file_extension not in allowed_extensions_lower:
            self.show_warning_message(
                title="图片路径错误",
                message="选择的有效的图片文件。"
            )
            return False

        return True

    def update_file_path(self, file_path: str):
        """
        更新 `editFilePath` 控件显示的文件路径。
        参数:
        - file_path (str): 要显示的文件路径。
        """
        file_extension = os.path.splitext(file_path)[1].lower()  # 将扩展名转换为小写
        allowed_extensions_lower = ['.' + ext.lower() for ext in self.allowed_extensions]  # 在每个元素前添加点号，并将列表中的每个元素转换为小写

        if file_extension in allowed_extensions_lower:
            self.ui.editFilePath.setText(file_path)  # 更新文件路径
        else:
            QMessageBox.warning(
                self,
                "图片类型错误",
                f"选择的文件'{file_path}' 不是图片类型。请选择.jpg, .jpeg, .png "
            )

    def display_image(self, image_path: str, target_label: QLabel):
        """
        显示指定路径的图片到指定的 `QLabel` 控件上。

        参数:
        - image_path (str): 图片文件的路径。
        - target_label (QLabel): 要显示图片的目标 QLabel 控件。
        """
        try:
            # 加载图片到 QPixmap
            pixmap = QPixmap(image_path)
        except Exception as e:
            QMessageBox.warning(
                self,
                "显示推理结果失败",
                f"加载图片时发生错误: {str(e)}"
            )
            return

        # 按照原图比例缩放图片
        scaled_pixmap = pixmap.scaled(target_label.size(), Qt.KeepAspectRatio)

        # 设置 QLabel 的 pixmap 属性以显示图片
        target_label.setPixmap(scaled_pixmap)
        target_label.setAlignment(Qt.AlignCenter)  # 可选：居中显示图片

    def select_save_folder(self):
        """
        打开文件夹选择对话框，选中后将文件夹路径更新到 `editSavePath` 控件中。
        """
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)  # 只允许选择目录
        if folder_dialog.exec_():
            selected_folder = folder_dialog.selectedFiles()[0]
            self.ui.editSavePath.setText(selected_folder)  # 更新编辑框文本

    def update_confidence_value_text(self, value: int):
        """
        当滑块值改变时，更新 `editConfidenceValue` 文本框的内容。
        参数:
        - value (int): 滑块当前的值（范围 0 到 100）。
        """
        formatted_value = "{:.2f}".format(value / 100.0)  # 将整数值转换为 0 到 1 之间的浮点数
        self.ui.editConfidenceValue.setText(formatted_value)

    def update_confidence_slider_position_from_textbox(self):
        """
        当用户在 `editConfidenceValue` 文本框中输入一个数值并按下回车键时，
        尝试将滑块位置更新为对应数值。
        """
        text = self.ui.editConfidenceValue.text().strip()  # 去除首尾空格
        if text:
            try:
                value = float(text)
                if 0.0 <= value <= 1.0:
                    self.ui.confidenceSlider.setValue(int(value * 100))  # 将浮点数转换为整数（范围 0 到 100）
                else:
                    self.show_warning_message("输入值超出范围", "请输入介于 0.0 和 1.0 之间的数值。")
                    self.ui.editConfidenceValue.setText("0.60")
                    self.ui.confidenceSlider.setValue(60)
            except ValueError:
                self.show_warning_message("无效数值输入", "请输入介于 0.0 和 1.0 之间的数值。")
                self.ui.editConfidenceValue.setText("0.60")
                self.ui.confidenceSlider.setValue(60)
        else:
            self.show_warning_message("置信度为空", "请输入介于 0.0 和 1.0 之间的数值。")
            self.ui.editConfidenceValue.setText("0.60")
            self.ui.confidenceSlider.setValue(60)

    def reset_values(self):
        """
        重置窗口控件至初始化状态。
        """
        try:
            self.ui.editFilePath.clear()  # 清空文件路径文本框
            self.ui.editSavePath.clear()  # 清空保存路径文本框

            # 将滑块重置
            self.ui.confidenceSlider.setValue(60)

            # 更新滑块数值框，显示滑块最小值对应的浮点数（转换为百分比后保留两位小数）
            formatted_value = "{:.2f}".format(self.ui.confidenceSlider.value() / 100.0)
            self.ui.editConfidenceValue.setText(formatted_value)

            # 清除图片预览 label 上的图片
            self.ui.labelPreview.clear()
            # 恢复 labelPreview 初始文字内容
            self.ui.labelPreview.setText("图片检测")
            # 清除输出框的图片
            self.ui.labelOutput.clear()
            # 恢复输出框的文字
            self.ui.labelOutput.setText("请选择图片")
        except Exception as e:
            self.show_warning_message(
                title="重置控件时发生错误",
                message=f"错误详情：{str(e)}"
            )

    def show_warning_message(self, title: str, message: str):
        """
        显示警告消息框。
        参数:
        - title (str): 消息框标题。
        - message (str): 消息框内容。
        """
        QMessageBox.warning(self, title, message)

    def start_detection(self):
        """
        开始图像检测。
        """
        # 读取图片数据

        # 如果任意一个为空则退出
        if not self.ui.editFilePath.text() or not self.ui.editSavePath.text():
            self.show_warning_message("未选择图片或保存路径", "请选择图片和保存路径。")
            return
        try:
            image_data = cv2.imread(self.ui.editFilePath.text())
        except Exception as e:
            self.show_warning_message("读取图像异常", f"读取图像时发生异常：{str(e)}")
            return

        # 获取当前输入图像路径、保存路径和置信度值（从 editConfidenceValue 文本框获取）
        save_path = self.ui.editSavePath.text()
        confidence_value = float(self.ui.editConfidenceValue.text())

        self.predictor = ObjectDetector(
            save=True,
            confidence_threshold=confidence_value,
            save_path=save_path,
            use_gpu=False
        )
        # 创建进度对话框
        self.progress_dialog.show()
        self.predictor.run_image(image_data=image_data)  # 进行推理
        self.progress_dialog.close()
        self.display_image(self.ui.editSavePath.text() + "/result.jpg", self.ui.labelOutput)
        self.predictor = None


class ProgressDialog(QDialog):
    """
    提示框，用于提示检测进度。
    """

    def __init__(self):
        super().__init__()
        # 设置提示框的标题、图标和大小，并设置为模态对话框
        self.setWindowTitle("正在进行检测")
        self.setWindowIcon(QIcon("./icons/icon.ico"))
        self.setFixedSize(300, 100)
        # 设置窗口标志，只保留最小化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        # 创建垂直布局管理器
        layout = QVBoxLayout()

        # 添加居中显示的 QLabel
        label = QLabel("请稍等！")
        font = QFont()
        font.setPointSize(1)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # 将布局设置到对话框上
        self.setLayout(layout)
