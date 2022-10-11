import sys
from PySide6.QtCore import QSize, Qt, QPoint, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen
from game_page import Game
from choose_level import Level
from index import Index

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

def open_travel():
        window = Level()
        window.show()


class Controller:
    def __init__(self):
        self.index = Index()
        self.travel = Level()
        self.game = Game()

    def show_index(self):
        pass

    def show_travel(self):
        pass

    def show_game(self):
        pass

    def show_hidden(self):
        pass


if __name__ == "__main__":
    app = QApplication([])
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    index = Index()
    index.show()
    # level = Level()
    # index.travel_button.clicked.connect(level.show)
    # window = Level()
    # window.show()
    # window = Game()
    # window.show()
        

    app.exec_()