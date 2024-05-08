import os

# OpenCV is used for video and image processing.
import cv2
# PyQt5 is used for building the GUI.
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import (
    QWidget, QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QDialog, QProgressBar
)

from src.utils import ObjectDetector
from .ui import Ui_VideoDetectionUI


class VideoDetectionWindow(QWidget):
    """
        视频检测窗口类
    """
    def __init__(self):
        super().__init__()
        self.reset_signal = None
        self.save_path = None
        self.ui = Ui_VideoDetectionUI()
        self.ui.setupUi(self)

        # 初始化子线程
        self.worker_thread = None  # 初始化工作线程为None

        # 初始化进度条
        self.progress_dialog = None

        self.allowed_extensions = ['mp4', 'mkv', 'wmv']  # 定义允许的文件扩展名
        self.running = None
        self.count = None

        # 文件路径按钮点击事件
        self.ui.buttonFilePath.clicked.connect(self.open_file_dialog)
        self.ui.buttonSavePath.clicked.connect(self.select_save_folder)

        # 滑块绑定
        self.ui.confidenceSlider.setMinimum(0)
        self.ui.confidenceSlider.setMaximum(100)
        self.ui.confidenceSlider.setSingleStep(1)
        self.ui.confidenceSlider.valueChanged.connect(self.update_confidence_value_text)
        self.ui.editConfidenceValue.returnPressed.connect(self.update_confidence_slider_position_from_textbox)
        self.ui.editConfidenceValue.editingFinished.connect(self.update_confidence_slider_position_from_textbox)

        # 检测按钮点击事件
        self.ui.buttonStart.clicked.connect(self.start_detection)

        # 重置按钮点击事件
        self.ui.buttonReset.clicked.connect(self.reset_values)

    def open_file_dialog(self):
        """
            打开文件对话框，限制选择文件类型为 .mp4, .mkv, .wmv。
            选中后，将文件路径更新到 `editFilePath` 控件中。
        """
        dialog = QFileDialog(self)
        dialog.setNameFilter(f"Image Files ({' '.join(['*.' + ext for ext in self.allowed_extensions])})")

        if dialog.exec_():
            selected_file = dialog.selectedFiles()[0]  # 获取第一个（也是唯一一个）选择的文件路径
            self.update_file_path(selected_file)  # 直接更新文件路径
            self.display_video_first_frame(selected_file)  # 更新预览图片

    def is_valid_video_file(self, file_path: str) -> bool:
        """
            通过拓展名判断是否是合法的视频文件
        参数:
        - file_path (str): 要检查的文件路径。

        返回:
        - bool: 如果文件类型有效，则返回True；否则返回False。
        """
        if not file_path:  # 检查输入是否为空字符串
            return False

        file_extension = os.path.splitext(file_path)[1].lower()  # 将扩展名转换为小写
        allowed_extensions_lower = ['.' + ext.lower() for ext in self.allowed_extensions]  # 在每个元素前添加点号，并将列表中的每个元素转换为小写
        return file_extension in allowed_extensions_lower

    def update_file_path(self, file_path: str):
        """
            更新 `editFilePath` 控件显示的文件路径。
        参数:
            - file_path (str): 要显示的文件路径。
        """
        if self.is_valid_video_file(file_path):
            self.ui.editFilePath.setText(file_path)  # 更新文件路径
        else:
            print(f"选择的文件'{file_path}' 不是视频类型。请选择.mp4, .mkv, .wmv ")
            QMessageBox.warning(
                self,
                "视频类型错误",
                f"选择的文件'{file_path}' 不是视频类型。请选择.mp4, .mkv, .wmv "
            )

    def select_save_folder(self):
        """
            打开保存文件夹的选择对话框，选中后将文件夹路径更新到 `editSavePath` 控件中。
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
        尝试将滑块位置更新为对应数值，如果无法更新，调用show_warning_message()方法进行弹窗警告。
        """
        text = self.ui.editConfidenceValue.text().strip()  # 去除首尾空格
        if text:
            if not text.replace('.', '').isdigit():  # 检查是否为数字（包括小数点）
                self.show_warning_message("无效数值输入", "请输入一个有效的数值。")
            else:
                value = float(text)
                if not 0.0 <= value <= 1.0:
                    self.show_warning_message("输入值超出范围", "请输入介于 0.0 和 1.0 之间的数值。")
                else:
                    self.ui.confidenceSlider.setValue(int(value * 100))  # 将浮点数转换为整数（范围 0 到 100）

    def reset_values(self):
        """
            重置窗口控件至初始化状态。
        """
        try:
            self.running = False
            self.reset_signal = True
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
            self.ui.labelPreview.setText("视频检测")
            self.ui.labelOutput.setText("请选择视频文件")
            print("重置完成")
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

    # 输入合法性验证
    def validate_input(self):
        """
            输入合法性验证，判断保存文件路径是否合法。判断保存路径是否合法，判断置信度值是否合法。
        """
        if not self.is_valid_video_file(self.ui.editFilePath.text()):
            # 判断视频文件是否合法
            self.show_warning_message(
                title="视频路径错误",
                message="选择的有效的视频文件。"
            )
            return False
        if not self.ui.editSavePath.text() or not os.path.isdir(self.ui.editSavePath.text()):
            # 判断保存路径是否为空或者不是一个文件夹
            self.show_warning_message(
                title="保存路径错误",
                message="请选择有效的保存路径。"
            )
            return False

        if not self.ui.editConfidenceValue.text():
            self.show_warning_message(
                title="置信度值错误",
                message="请输入置信度值。"
            )
            return False
        try:
            confidence_value = float(self.ui.editConfidenceValue.text())
            if not 0.0 <= confidence_value <= 1.0:
                self.show_warning_message(
                    title="置信度值错误",
                    message="置信度值必须在0.0到1.0之间。"
                )
                return False
        except ValueError:
            self.show_warning_message(
                title="置信度值错误",
                message="置信度值必须是一个数字。"
            )
            return False

        # 如果所有验证都通过，则返回 True
        return True

    def start_detection(self):
        """
            开始视频检测。
        """
        # 首先进行输入合法性验证
        if not self.validate_input():
            # 输入不合法，不执行检测操作
            return

        print("开始检测")
        # 传递参数
        video_path, self.save_path, confidence_value = self.passing_parameters()
        total_frames, width, height = self.get_video_properties(video_path)

        # 创建进度条类
        self.progress_dialog = ProgressDialog(int(total_frames))

        # 连接终止信号
        self.progress_dialog.stop_signal.connect(self.stop_detection)

        # 创建子线程
        self.worker_thread = DetectionThread(video_path, self.save_path, confidence_value, width, height)
        self.worker_thread.update_signal.connect(self.update_progress)  # 连接信号
        self.worker_thread.finished_signal.connect(self.on_finished)  # 连接完成信号
        self.worker_thread.running = True  # 修改标识符

        self.progress_dialog.show()  # 显示进度条
        self.worker_thread.start()  # 启动线程

    def stop_detection(self):
        """
            停止视频检测
        """
        print("test")
        if self.worker_thread is not None:
            self.worker_thread.stop()  # 发出停止信号
            self.worker_thread.wait()  # 等待线程结束
            self.worker_thread = None  # 清理线程实例
            self.progress_dialog.close()  # 关闭进度条窗口

    def update_progress(self, count):
        """
            更新进度条值
        Args:
            count:进度值

        Returns:

        """
        self.progress_dialog.update_progress(count)

    def on_finished(self):
        """
            推理完成后的处理：关闭进度条窗口，弹窗提示，播放推理结果，
        """
        print("推理完成")
        self.progress_dialog.close()
        self.running = False
        self.show_warning_message("注意", "检测完成，文件保存在{0}/output_video.mp4".format(self.save_path))
        self.display_video(self.save_path + '/output_video.mp4')

    def passing_parameters(self):
        """
            传递检测参数。
        Returns:
            video_path (str): 视频文件路径。
            save_path (str): 保存路径。
            confidence_value (float): 置信度阈值。
        """
        return self.ui.editFilePath.text(), self.ui.editSavePath.text(), float(self.ui.editConfidenceValue.text())

    def display_video_first_frame(self, video_path: str):
        """
        显示指定路径的图片到指定的 `QLabel` 控件上。

        参数:
        - video_path (str): 图片文件的路径。
        - target_label (QLabel): 要显示图片的目标 QLabel 控件。
        """
        if not os.path.isfile(video_path):
            print(f"视频文件 '{video_path}' 不存在，请检查路径是否正确。")
            return

        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()  # 读取第一帧

        if not ret:
            print(f"无法从视频文件 '{video_path}' 读取第一帧，请检查文件是否有效。")
            return

        # 将 OpenCV BGR 图像转换为 RGB，并创建 QPixmap
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pixmap = QPixmap.fromImage(QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888))

        # 检查加载是否成功
        if pixmap.isNull():
            print(f"无法将视频第一帧转换为 QPixmap，请检查图像数据是否有效。")
            return

        scaled_pixmap = pixmap.scaled(self.ui.labelPreview.size(), Qt.KeepAspectRatio)
        self.ui.labelPreview.setPixmap(scaled_pixmap)
        self.ui.labelPreview.setAlignment(Qt.AlignCenter)  # 可选：居中显示图片

        # 释放资源
        cap.release()

    def display_video(self, display_video_path):
        """
        在指定的 QLabel 上播放指定路径的视频。

        Args:
            display_video_path (str): 视频文件路径。

        Returns:
            bool: 如果视频成功打开并开始播放，返回 True；否则返回 False。
        """

        # 尝试打开视频文件
        if not os.path.isfile(display_video_path):
            print(f"视频文件 '{display_video_path}' 不存在，请检查路径是否正确。")
            return False

        video = cv2.VideoCapture(display_video_path)

        if not video.isOpened():
            print(f"无法打开视频文件: {display_video_path}")
            return False

        # 获取视频的原始宽高、总帧数和帧率
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        # frame_rate = int(video.get(cv2.CAP_PROP_FPS))

        # 获取 label 输出的实际宽高
        label_output_width = self.ui.labelOutput.width()
        label_output_height = self.ui.labelOutput.height()

        # 计算目标播放尺寸，保持宽高比不变
        target_width = label_output_width
        target_height = label_output_height

        if width > height:
            long_side = width
            scale_ratio = target_width / long_side
        else:
            long_side = height
            scale_ratio = target_height / long_side

        # 循环读取视频帧并显示
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            # 将帧缩放到目标尺寸
            scaled_frame = cv2.resize(frame, None, fx=scale_ratio, fy=scale_ratio, interpolation=cv2.INTER_AREA)
            # 将 OpenCV 的帧转换为 QtGui 的图像
            pixmap = self.convert_cv_to_pixmap(scaled_frame)

            self.ui.labelOutput.setPixmap(pixmap)
            self.ui.labelOutput.show()
            cv2.waitKey(10)  # 每帧等待10毫秒
            if self.reset_signal:
                self.ui.labelOutput.setText("请选择视频文件")
                self.reset_signal = False
                break

        video.release()  # 播放完毕后释放视频资源

        return True

    def convert_cv_to_pixmap(self, cv_image):
        """
            将 OpenCV 的 BGR 格式的图像转换为 QPixmap
        Args:
            cv_image: OpenCV 的 BGR 格式的图像
        Return:
            pixmap: QPixmap 格式的图片
        """
        height, width, channels = cv_image.shape
        bytes_per_line = channels * width
        q_img = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_img)
        return pixmap

    def get_video_properties(self, video_path):
        """
            计算视频总帧率，宽度，高度
        Args:
            video_path: 视频文件路径
        Returns:
            total_frames: 视频总帧数
            width: 视频宽度
            height: 视频高度
        """
        # 打开视频文件
        video_data = cv2.VideoCapture(video_path)

        # 检查视频是否成功打开
        if not video_data.isOpened():
            raise ValueError("Error: Unable to open video file")

        # 获取视频的帧率
        total_frames = int(video_data.get(cv2.CAP_PROP_FRAME_COUNT))

        # 获取视频的宽度和高度
        width = int(video_data.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_data.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_data.release()

        return total_frames, width, height


class ProgressDialog(QDialog):
    """
        进度条类，用于显示检测进度。
    """
    stop_signal = pyqtSignal()  # 终止信号，用于终止检测子线程

    def __init__(self, total_frames):
        super().__init__()

        # 设置对话框的标题、图标和大小，并设置为模态对话框
        self.setWindowTitle("正在检测，请稍等")
        self.setWindowIcon(QIcon("./icons/icon.ico"))
        self.setFixedSize(300, 150)
        self.setModal(True)
        # 设置窗口标志，只保留最小化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        # 创建控件：进度条和取消按钮
        self.progress_bar = QProgressBar()  # 进度条
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(total_frames)
        self.progress_bar.setMinimum(0)

        self.cancel_button = QPushButton("停止检测")
        # 连接取消按钮的点击事件
        self.cancel_button.clicked.connect(self.stop_signal.emit)

        # 将控件添加到布局管理器中
        layout = QVBoxLayout()
        # 删除对label的添加语句
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def set_progress(self, value: int):
        """
            设置进度条最大值
        args:
            value: 进度条最大值
        """
        self.progress_bar.setMaximum(value)

    def update_progress(self, count):
        """
            更新进度条的进度值
        Args:
            count: 进度值
        """
        self.progress_bar.setValue(count)


class DetectionThread(QThread):
    """
        检测子线程类
    """
    update_signal = pyqtSignal(int)  # 发出整数信号，用于更新UI
    finished_signal = pyqtSignal()  # 发出计数完成信号

    running = None  # 控制线程运行的标志位

    def __init__(self, video_path, save_path, confidence_value, width, height):
        """
        初始化工作线程。
        """
        super().__init__()
        self.count = 0
        self.video_path = video_path
        self.save_path = save_path
        self.confidence_value = confidence_value
        self.width = width
        self.height = height

        # 初始化检测器
        self.predictor = ObjectDetector(
            confidence_threshold=confidence_value,
            iou_threshold=0.4,
            draw_text=False,
            save=True,
            save_path=save_path,
            use_gpu=True)

    def run(self):
        """
            线程主体运行函数，从read_video_frames()中读取视频帧，调用predictor类的检测方法进行检测，把输出结果组合成视频。
            中途传递进度值，检测完毕后，发送完成信号调用on_finished()。
        """

        # 输出视频存储配置
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编解码器
        out = cv2.VideoWriter(self.save_path + '/output_video.mp4', fourcc, 30, (self.width, self.height))

        frames_generator = self.read_video_frames(video_path=self.video_path)
        count = 0  # 进度条数值
        while self.running:
            try:
                # 从生成器中获取下一帧
                frame = next(frames_generator)
            except StopIteration:
                # 如果生成器耗尽（即视频的所有帧都被读取完毕），则传递完成信号并退出循环
                self.finished_signal.emit()
                break
            out_frame = self.predictor.run_video(frame=frame)  # 对每一帧进行推理
            out.write(out_frame)  # 保存输出的每一帧
            count += 1  # 更新进度条数值
            self.update_signal.emit(count)  # 发出更新信号
            print("正在检测第{0}帧".format(str(count)))

    def stop(self):
        """
            停止线程运行。
        """
        self.running = False

    def read_video_frames(self, video_path):
        """
            打开视频文件，创建生成器读取视频的每一帧
        Args:
            video_path: 文件路径

        Returns:
            frame: 生成器读取后的帧

        """
        video = cv2.VideoCapture(video_path)

        # 检查视频是否成功打开
        if not video.isOpened():
            raise ValueError("Error: Unable to open video file")

        try:
            # 逐帧读取视频
            while True:
                # 读取一帧
                ret, frame = video.read()

                # 检查是否成功读取帧
                if not ret:
                    break

                # 返回当前帧
                yield frame
        finally:
            # 关闭视频文件
            video.release()
