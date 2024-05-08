from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication

from .aboutme_window import AboutMeWindow
from .camera_window import CameraDetectionWindow
from .image_window import ImageDetectionWindow
from .ui import Ui_MainWindow
from .video_window import VideoDetectionWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 实例化Ui_MainWindow类
        self.ui = Ui_MainWindow()

        try:
            # 调用setupUi方法将UI布局应用到当前窗口
            self.ui.setupUi(self)
        except Exception as e:
            print(f"UI布局应用出错: {e}")
            # 这里可以添加一些错误处理的逻辑，比如显示错误信息，或者退出程序

        # 通过一个封装的方法添加UI到stackedWidget，减少代码重复
        self._add_subwindows()

        # 为switchButton绑定槽函数
        self.ui.switchImageDetection.clicked.connect(self.show_image_detection_page)
        self.ui.switchVideoDetection.clicked.connect(self.show_video_detection_page)
        self.ui.switchCameraDetection.clicked.connect(self.show_camera_detection_page)
        self.ui.switchAboutMe.clicked.connect(self.show_about_me_page)

        # 禁止窗口自由形变
        self.setFixedSize(self.size())

        # 调用move()方法将窗口移动到屏幕中央
        self.move_to_center()

    def move_to_center(self):
        # 获取屏幕的中心点
        screen_center = QApplication.desktop().screen().rect().center()
        # 获取窗口的中心点
        window_center = self.rect().center()
        # 计算窗口左上角在屏幕中央的位置
        move_to = screen_center - window_center
        # 将窗口左上角坐标调整为屏幕中央
        self.move(self.pos() + move_to)

    def _add_subwindows(self):
        """
        向堆叠小部件中添加子窗口的方法。
        此方法遍历一个包含窗口类和页面名称的列表，尝试为每个项创建一个子窗口，并将相应的UI实例化后添加到堆叠小部件中。

        参数:
        self: 对象自身的引用。

        返回值:
        无
        """
        # 准备子窗口信息的列表，每项包含一个窗口类和一个页面名称
        pages = [
            (ImageDetectionWindow, "imageDetectionPage"),
            (VideoDetectionWindow, "videoDetectionPage"),
            (CameraDetectionWindow, "cameraDetectionPage"),
            (AboutMeWindow, "aboutMePage")
        ]
        # 遍历页面列表，为每个页面创建子窗口并添加UI
        for WindowClass, page_name in pages:
            try:
                page = WindowClass()
                if isinstance(page, QWidget):  # 确保page是QWidget或其子类，以便添加到stackedWidget
                    self.ui.stackedWidget.addWidget(page)
                else:
                    print(f"创建{page_name}时返回的页面对象不是QWidget或其子类")
            except Exception as e:
                # 如果在设置UI过程中发生错误，则打印错误信息
                print(f"设置{page_name}出错: {e}")

    def _create_subwindow(self, page_name):
        """
        创建并配置一个子窗口。

        参数:
        - page_name: 子窗口的名称，用于设置对象名。

        返回值:
        - page: 创建的QtWidgets.QWidget对象实例。
        """
        # 创建一个新的QtWidgets.QWidget对象作为子窗口
        page = QtWidgets.QWidget()
        # 设置子窗口的对象名为page_name
        page.setObjectName(page_name)
        # 将子窗口添加到堆叠式小部件中
        self.ui.stackedWidget.addWidget(page)
        return page

    def show_image_detection_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_video_detection_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_camera_detection_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def show_about_me_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)
