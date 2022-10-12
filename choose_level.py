import sys
from PySide6.QtCore import QSize, Qt, QPoint, QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen
import functools

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'kami2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class Level(QLabel):
    # current_step = bind("step_button", "text")
    
    redirect_home = Signal(int)
    redirect_game = Signal(int)
    def __init__(self, type="旅程"):
        super().__init__()

        self.setWindowTitle("kami2")
        background = QPixmap().fromImage("./assets/background.png").scaled(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.setPixmap(background)
        self.setBaseSize(SCREEN_WIDTH,SCREEN_HEIGHT)

        self.home_button = QPushButton("", self)
        self.left_button = QPushButton("", self)
        self.right_button = QPushButton("", self)
        self.current_page_button = QPushButton("", self)
        self.styled_button()
        self.count_level = 42
        self.current_page = 1
        self.current_level_imgs = [QPushButton("", self) for _ in range(6)]
        self.current_levels = [QPushButton("", self) for _ in range(6)]
        self.current_level_nums = [QLabel("", self.current_levels[i]) for i in range(6)]
        self.styled_level()
        self.bind_level()


    def styled_button(self):
        x, y, width, height = 20, 20, 40, 40
        self.home_button.setGeometry(x, y, width, height)
        self.home_button.setIcon(QIcon("./assets/home.png"))
        self.home_button.setIconSize(QSize(27, 27))
        self.home_button.setStyleSheet("background-color: #9cb8b5; border-radius: 20;")

        x, y, width, height = SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - 50, 30, 30
        self.current_page_button.setGeometry(x, y, width, height)
        self.current_page_button.setStyleSheet("background-color: #9cb8b5; border-radius: 15; color: white;")

        left_x, right_x, y, width, height = 30, SCREEN_WIDTH - 60, SCREEN_HEIGHT - 50, 30, 30
        self.left_button.setGeometry(left_x, y, width, height)
        self.right_button.setGeometry(right_x, y, width, height)
        self.left_button.setIcon(QIcon("./assets/left.png"))
        self.right_button.setIcon(QIcon("./assets/right.png"))
        self.left_button.setIconSize(QSize(30, 30))
        self.right_button.setIconSize(QSize(30, 30))
        self.left_button.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.right_button.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.home_button.clicked.connect(self.return_home)
        self.left_button.clicked.connect(self.left)
        self.right_button.clicked.connect(self.right)

    def styled_level(self):
        for i in range(6):
            x, y, width, height = (i % 3) * 115 + 16, (i // 3) * (160 + 100) + 80, 99, 160
            self.current_level_imgs[i].setGeometry(x, y, width, height)
            self.current_level_imgs[i].setIconSize(QSize(99, 160))
            x, y, width, height = (i % 3) * 115 + 16 + 20, (i // 3) * (160 + 100) + 80 + 170, 60, 60
            self.current_levels[i].setGeometry(x, y, width, height)
            self.current_levels[i].setIconSize(QSize(60, 60))
            self.current_levels[i].setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
            x, y ,width, height = 0, 0, 60, 60
            
            self.current_level_nums[i].setGeometry(x, y, width, height)
            self.current_level_nums[i].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.current_level_nums[i].setStyleSheet("font-size: 18px; color: #475c53;")

    def bind_level(self):
        self.current_page_button.setText(str(self.current_page))
        for i in range(6):
            lv = (self.current_page - 1) * 6 + (i + 1)
            self.current_level_imgs[i].setIcon(QIcon("./level_img/" + str(lv) + ".png"))
            # self.current_level[i].setText(str(lv))
            # if i % 2 == 0:
            #     self.current_level[i].setIcon(QIcon("./assets/perfect.png"))
            # else:
            #     self.current_level[i].setIcon(QIcon("./assets/ok.png"))
            self.current_levels[i].setIcon(QIcon("./assets/level.png"))
            self.current_level_nums[i].setText(str(lv))
            self.current_level_imgs[i].clicked.connect(functools.partial(self.open_game, lv))
            self.current_levels[i].clicked.connect(functools.partial(self.open_game, lv))

            # self.current_level[i].setStyleSheet("background: url('./assets/level.png'); background-position: center; "
            # + "background-size: 100 100;")

    def return_home(self):
        self.redirect_home.emit(1)

    def open_game(self, lv=1):
        self.redirect_game.emit(lv)

    def left(self):
        if self.current_page <= 1:
            return
        self.current_page -= 1
        self.current_page_button.setText(str(self.current_page))
        self.bind_level()

    def right(self):
        if self.current_page >= 7:
            return
        self.current_page += 1
        self.current_page_button.setText(str(self.current_page))
        self.bind_level()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = Level()
    window.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    window.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.show()

    app.exec_()