import threading

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from src.gui.ui import Ui_CameraDetectionUI
from src.utils import ObjectDetector


def convert_cv_to_pixmap(cv_image):
    height, width, channels = cv_image.shape
    bytes_per_line = channels * width
    q_img = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
    pixmap = QPixmap.fromImage(q_img)
    return pixmap


def resize_image_with_aspect_ratio(image, target_width, target_height):
    # 获取原始图像的宽高
    original_height, original_width = image.shape[:2]

    # 计算原始图像的宽高比
    aspect_ratio = original_width / original_height

    # 计算目标图像的宽高比
    target_aspect_ratio = target_width / target_height

    # 根据目标宽高比和原始宽高比确定缩放比例
    if aspect_ratio > target_aspect_ratio:
        # 如果原始图像的宽高比更大，则以目标高度为基准进行缩放
        scale = target_height / original_height
    else:
        # 如果原始图像的宽高比更小，则以目标宽度为基准进行缩放
        scale = target_width / original_width

    # 缩放图像
    resized_image = cv2.resize(image, None, fx=scale, fy=scale)

    return resized_image


class CameraDetectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_CameraDetectionUI()
        self.ui.setupUi(self)
        self.running = True
        # 初始化摄像头列表
        self.ui.comboboxCamera.clear()
        self.ui.comboboxCamera.addItems(list_camera_devices())

        # 初始化检测器
        self.predictor = ObjectDetector(
            iou_threshold=0.4,
            draw_text=False,
            save=False,
            use_gpu=True)

        # 预热模型
        frame = np.zeros((1, 1, 3), dtype=np.uint8)
        self.predictor.run_camera(frame)

        # 滑块绑定
        self.ui.confidenceSlider.setMinimum(0)
        self.ui.confidenceSlider.setMaximum(100)
        self.ui.confidenceSlider.setSingleStep(1)
        self.ui.confidenceSlider.valueChanged.connect(self.update_confidence_value_text)
        self.ui.editConfidenceValue.returnPressed.connect(self.update_confidence_slider_position_from_textbox)
        self.ui.editConfidenceValue.editingFinished.connect(self.update_confidence_slider_position_from_textbox)

        # 按钮绑定
        self.ui.buttonCamera.clicked.connect(self.update_camera)
        self.ui.buttonSavePath.clicked.connect(self.select_save_folder)

        # 检测按钮点击事件
        self.ui.buttonStart.clicked.connect(self.start_detection)

        # 停止按钮点击事件
        self.ui.buttonStop.clicked.connect(self.stop_values)

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
            except ValueError:
                self.show_warning_message("无效数值输入", "请输入一个有效的数值。")

    def update_camera(self):
        """
        获取摄像头设备，更新摄像头设备栏
        """
        # 禁用按钮防止重复点击
        self.ui.buttonCamera.setEnabled(False)

        # 在单独的线程中执行耗时任务
        threading.Thread(target=self.update_camera_task).start()

    def update_camera_task(self):
        # 清空摄像头设备下拉列表框
        self.ui.comboboxCamera.clear()

        # 获取摄像头设备列表
        camera_devices = list_camera_devices()

        # 添加摄像头设备到下拉列表框
        self.ui.comboboxCamera.addItems(camera_devices)

        # 在主线程中重新启用按钮
        self.ui.buttonCamera.setEnabled(True)

    def select_save_folder(self):
        """
        打开文件夹选择对话框，选中后将文件夹路径更新到 `editSavePath` 控件中。
        """
        folder_dialog = QFileDialog(self)
        folder_dialog.setFileMode(QFileDialog.DirectoryOnly)  # 只允许选择目录
        if folder_dialog.exec_():
            selected_folder = folder_dialog.selectedFiles()[0]
            self.ui.editSavePath.setText(selected_folder)  # 更新编辑框文本

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
        开始检测。
        """
        self.running = True
        # 获取摄像头设备、保存路径和置信度值
        camera = self.ui.comboboxCamera.currentText()
        if camera == "未检测到摄像头，请检查是否有摄像头设备":
            self.show_warning_message("警告", "未检测到摄像头，请检查是否有摄像头设备。")
            return  # 退出函数
        save_path = self.ui.editSavePath.text()
        confidence_value = float(self.ui.editConfidenceValue.text())
        print("使用编号为{0}的摄像头，保存地址为{1}，置信度为{2}".format(camera, save_path, confidence_value))
        output_camera = None
        if self.ui.labelSavePath.text():
            save = True
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_camera = cv2.VideoWriter(save_path + '/output_camera.mp4', fourcc, 30, (640, 480))
        else:
            save = False
        # 裁切视频帧，推理，label持续显示
        frame_generator = self.get_video_frame(int(camera))
        try:
            first_displayed = False
            while self.running:
                try:
                    frame = next(frame_generator)

                    # 推理
                    self.predictor.save_path = save_path
                    self.predictor.confidence_threshold = confidence_value
                    out_image, result = self.predictor.run_camera(frame)
                    # label显示
                    self.display_output_image(out_image)
                    if len(result) > 0:
                        self.ui.labelPreview.setText("请注意！")
                    else:
                        self.ui.labelPreview.setText("未检测到！")
                    if save:
                        output_camera.write(out_image)  # 保存输出的每一帧

                except StopIteration:
                    if not self.running:
                        break  # 如果 self.running 变为假，则退出循环
        finally:
            if save:
                output_camera.release()

    def get_video_frame(self, camera_index: int):
        cap = cv2.VideoCapture(camera_index)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("无法从摄像头获取视频帧")
                break
            yield frame
            cv2.waitKey(10)
            if not self.running:
                break
        cap.release()

    def display_output_image(self, cv_image):
        # 图片缩放适应窗口
        resize_image = resize_image_with_aspect_ratio(cv_image, 1230, 750)
        # 将 OpenCV 图像转换为 PyQt5 可用的图像格式
        pixmap = convert_cv_to_pixmap(resize_image)
        # 显示
        self.ui.labelOutput.setPixmap(pixmap)

    def stop_values(self):
        """
            停止检测
        """
        self.running = False
        self.ui.labelOutput.clear()
        self.ui.labelOutput.setText("检测已停止")


def list_camera_devices():
    """
        获取摄像头设备，返回摄像头设备列表
    """
    num_devices = 0
    camera_devices = []
    while True:
        cap = cv2.VideoCapture(num_devices)
        if not cap.isOpened():
            break
        else:
            camera_devices.append(str(num_devices))  # 将序列号转换为字符串并添加到列表中
            num_devices += 1
        cap.release()

    if num_devices == 0:
        camera_devices = ["未检测到摄像头，请检查是否有摄像头设备"]

    return camera_devices
