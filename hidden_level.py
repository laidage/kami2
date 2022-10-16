import sys
from PySide6.QtCore import QSize, Qt, QPoint, QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QImage
import functools

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'kami2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class HLevel(QLabel):
    # current_step = bind("step_button", "text")
    
    redirect_home = Signal(int)
    redirect_hidden_game = Signal(int)
    def __init__(self, type="旅程"):
        super().__init__()

        self.setWindowTitle("kami2")
        background = QPixmap().fromImage(QImage("./assets/background.png")).scaled(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.setPixmap(background)
        self.setBaseSize(SCREEN_WIDTH,SCREEN_HEIGHT)

        self.home_button = QPushButton("", self)
        self.styled_button()
        self.count_level = 42
        self.current_level_imgs = [QPushButton("", self) for _ in range(5)]
        self.current_levels = [QPushButton("", self) for _ in range(5)]
        self.current_level_nums = [QLabel("", self.current_levels[i]) for i in range(5)]
        self.styled_level()
        self.bind_level()


    def styled_button(self):
        self.home_button.clicked.connect(self.return_home)
        x, y, width, height = 20, 20, 40, 40
        self.home_button.setGeometry(x, y, width, height)
        self.home_button.setIcon(QIcon("./assets/home.png"))
        self.home_button.setIconSize(QSize(27, 27))
        self.home_button.setStyleSheet("background-color: #9cb8b5; border-radius: 20;")



    def styled_level(self):
        for i in range(5):
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
        for i in range(5):
            lv = i + 1
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
        self.redirect_hidden_game.emit(lv)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = HLevel()
    window.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
    window.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.show()

    app.exec_()