import sys
from PySide6.QtCore import QSize, QPropertyAnimation, QPoint, Signal, QThread
from PySide6.QtWidgets import QApplication, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QImage

import time

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'kami2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class StartLabel(QLabel):
    # current_step = bind("step_button", "text")
    def __init__(self):
        super().__init__()

        self.setWindowTitle("kami2")
        background = QPixmap().fromImage(QImage("./assets/welcome.png")).scaled(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.setPixmap(background)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = StartLabel()
    window.show()

    app.exec_()