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

class Index(QMainWindow):
    # current_step = bind("step_button", "text")

    def __init__(self):
        super().__init__()

        self.setWindowTitle("kami2")
        self.label = QLabel()
        background = QPixmap().fromImage("./assets/background.png").scaled(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.label.setPixmap(background)
        self.label.setBaseSize(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.setCentralWidget(self.label)
        # self.label.setStyleSheet("background: url(./assets/background.png);")
        self.travel_button = QPushButton("", self.label)
        self.hidden_button = QPushButton("", self.label)
        self.styled_buttons()

    def styled_buttons(self):
        width = 200
        height = 200
        x = 80
        y1 = 50 + 20
        y2 = y1 + height + 40
        self.travel_button.setGeometry(x, y1, width, height)
        self.hidden_button.setGeometry(x, y2, width, height)
        self.travel_button.setIcon(QIcon('./assets/travel.png'))
        self.hidden_button.setIcon(QIcon('./assets/hidden.png'))
        self.travel_button.setIconSize(QSize(200, 200))
        self.hidden_button.setIconSize(QSize(200, 200))
        self.travel_button.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.hidden_button.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = Index()
    window.show()

    app.exec_()