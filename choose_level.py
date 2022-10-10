import sys
from PySide6.QtCore import QSize, Qt, QPoint, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'kami2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class Level(QMainWindow):
    # current_step = bind("step_button", "text")

    def __init__(self, type="旅程"):
        super().__init__()

        self.setWindowTitle("kami2")
        self.label = QLabel()
        background = QPixmap().fromImage("./assets/background.png").scaled(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.label.setPixmap(background)
        self.label.setBaseSize(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.setCentralWidget(self.label)

        self.home_button = QPushButton("", self.label)
        self.left_button = QPushButton("", self.label)
        self.right_button = QPushButton("", self.label)
        self.styled_button()

    def styled_button(self):
        x, y, width, height = 20, 20, 50, 50
        self.home_button.setGeometry(x, y, width, height)
        self.home_button.setIcon(QIcon("./assets/home.png"))
        self.home_button.setIconSize(QSize(35, 35))
        self.home_button.setStyleSheet("background-color: #9cb8b5; border-radius: 25;")

        left_x, right_x, y, width, height = 30, SCREEN_WIDTH - 60, SCREEN_HEIGHT - 50, 30, 30
        self.left_button.setGeometry(left_x, y, width, height)
        self.right_button.setGeometry(right_x, y, width, height)
        self.left_button.setIcon(QIcon("./assets/left.png"))
        self.right_button.setIcon(QIcon("./assets/right.png"))
        self.left_button.setIconSize(QSize(30, 30))
        self.right_button.setIconSize(QSize(30, 30))
        self.left_button.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.right_button.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = Level()
    window.show()

    app.exec_()