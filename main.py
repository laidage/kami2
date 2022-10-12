import sys
from PySide6.QtCore import QSize, Qt, QPoint, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen
from game_page import Game
from choose_level import Level
from index import Index
import functools

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640


class Controller:
    def __init__(self):
        self.index = Index()
        self.index.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.index.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.index.redirect_travel.connect(self.show_travel)
        self.index.redirect_hidden.connect(self.show_hidden)

    def show_index(self):
        if hasattr(self, "travel"):
            self.travel.close()
        self.index.show()

    def show_travel(self):
        if hasattr(self, "game"):
            self.game.close()
        if hasattr(self, "index"):
            self.index.setHidden(True)
        
        if hasattr(self, "travel"):
            self.travel.show()
        else:
            self.travel = Level()
        self.travel.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.travel.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.travel.show()
        self.travel.redirect_home.connect(self.show_index)
        self.travel.redirect_game.connect(self.show_game)

    def show_game(self, lv):
        if hasattr(self, "travel"):
            self.travel.setHidden(True)
        if hasattr(self, "game"):
            self.game.close()
        self.game = Game(lv)
        self.game.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.game.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game.show()
        self.game.redirect_travel.connect(self.show_travel)

    def show_hidden(self):
        print("hidden")
        pass


if __name__ == "__main__":
    app = QApplication([])
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    controller = Controller()
    controller.show_index()
    # index = Index()
    # index.show()
    # travel = Level()
    # index.travel_button.clicked.connect(travel.show)
    
    sys.exit(app.exec_())
        

    # app.exec_()