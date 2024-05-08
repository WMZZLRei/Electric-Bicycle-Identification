from PyQt5.QtWidgets import QWidget

from .ui import Ui_AboutMe


class AboutMeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AboutMe()
        self.ui.setupUi(self)