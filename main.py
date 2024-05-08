import sys

from PyQt5.QtWidgets import QApplication

from src.gui import MainWindow, Splash

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = Splash()
    splash.show()

    # 创建主窗口
    main_window = MainWindow()
    splash.close()
    main_window.show()

    sys.exit(app.exec_())
