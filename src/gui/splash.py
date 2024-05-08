from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QSplashScreen, QLabel

from .ui import base64_image


class Splash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 532)

        # 从base64_image中读取图片数据
        icon_data = base64_image()
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)

        self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # 添加正在启动的文字标签
        self.loading_label = QLabel("正在启动...", self)
        font = QFont()
        font.setPointSize(30)  # 调整字体大小为16
        self.loading_label.setFont(font)
        self.loading_label.setAlignment(Qt.AlignCenter)
        label_height = 30
        label_margin = 50  # 调整文字标签与底部的距离
        self.loading_label.setGeometry(0, self.height() - label_height - label_margin, self.width(), label_height)
        self.loading_label.show()

        self.show()
