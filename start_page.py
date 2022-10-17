import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QImage

from choose_level import Level

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
        background = QPixmap().fromImage(QImage("./assets/background.png")).scaled(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.setPixmap(background)
        self.setBaseSize(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.welcome_text = QPushButton("", self)
        self.welcome_girl = QPushButton("", self)
        self.styled_buttons()

    def styled_buttons(self):
        x1, y1, width1, height1 = 55, 50 + 20, 250, 100
        x2, y2, width2, height2 = 30, 50 + 160, 300, 300
        self.welcome_text.setGeometry(x1, y1, width1, height1)
        self.welcome_girl.setGeometry(x2, y2, width2, height2)
        self.welcome_text.setIcon(QIcon('./assets/welcome_text.png'))
        self.welcome_girl.setIcon(QIcon('./assets/welcome_girl.png'))
        self.welcome_text.setIconSize(QSize(width1, height1))
        self.welcome_girl.setIconSize(QSize(width2, height2))
        self.welcome_text.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.welcome_girl.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = StartLabel()
    window.show()

    app.exec_()