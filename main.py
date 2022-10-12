import sys
from PySide6.QtCore import QSize, Qt, QPoint, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QStackedWidget
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen
from game_page import Game
from choose_level import Level
from index import Index
import functools

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle("kami2")
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        self.index = Index()
        self.index.redirect_travel.connect(self.show_travel)
        self.index.redirect_hidden.connect(self.show_hidden)
        self.show_index()

    def show_index(self):
        if hasattr(self, "travel"):
            self.stackedWidget.removeWidget(self.travel)
            self.travel.close()
            delattr(self, "travel")
        self.stackedWidget.addWidget(self.index)
        self.stackedWidget.setCurrentWidget(self.index)
    
    def show_travel(self):
        if hasattr(self, "game"):
            self.stackedWidget.removeWidget(self.game)
            self.game.close()
            delattr(self, "game")
            
        if not hasattr(self, "travel"):
            self.travel = Level()
            self.stackedWidget.addWidget(self.travel)
            self.travel.redirect_home.connect(self.show_index)
            self.travel.redirect_game.connect(self.show_game)
        self.stackedWidget.setCurrentWidget(self.travel)
        print(self.stackedWidget.count(), "travel")

    def show_hidden(self):
        pass

    def show_game(self, lv):
        if not hasattr(self, "game"):
            self.game = Game(lv)
        else:
            self.stackedWidget.removeWidget(self.game)
            self.game.close()
            delattr(self, "game")
            self.game = Game(lv)
        self.stackedWidget.addWidget(self.game)
        self.game.redirect_travel.connect(self.show_travel)
        self.stackedWidget.setCurrentWidget(self.game)
        print(self.stackedWidget.count(), "game")
    
if __name__ == "__main__":
    app = QApplication([])
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    # controller = Controller()
    # controller.show_index()
    # index = Index()
    # index.show()
    # travel = Level()
    # index.travel_button.clicked.connect(travel.show)
    
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
        

    # app.exec_()