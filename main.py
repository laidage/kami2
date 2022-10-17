from hidden_level import HLevel
from hidden_game_page import HGame
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QIcon
from game_page import Game
from choose_level import Level
from index import Index

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
        if hasattr(self, "hidden"):
            self.stackedWidget.removeWidget(self.hidden)
            self.hidden.close()
            delattr(self, "hidden")
        self.stackedWidget.addWidget(self.index)
        self.stackedWidget.setCurrentWidget(self.index)
    
    def show_travel(self, reload_config=-1):
        if hasattr(self, "game"):
            self.stackedWidget.removeWidget(self.game)
            self.game.close()
            delattr(self, "game")
            if reload_config != -1:
                self.travel.reload_config(reload_config)
            
        if not hasattr(self, "travel"):
            self.travel = Level()
            self.stackedWidget.addWidget(self.travel)
            self.travel.redirect_home.connect(self.show_index)
            self.travel.redirect_game.connect(self.show_game)
        self.stackedWidget.setCurrentWidget(self.travel)

    def show_hidden(self, reload_config=-1):
        if hasattr(self, "hidden_game"):
            self.stackedWidget.removeWidget(self.hidden_game)
            self.hidden_game.close()
            delattr(self, "hidden_game")
            if reload_config != -1:
                self.hidden.reload_config(reload_config)
            
        if not hasattr(self, "hidden"):
            self.hidden = HLevel()
            self.stackedWidget.addWidget(self.hidden)
            self.hidden.redirect_home.connect(self.show_index)
            self.hidden.redirect_hidden_game.connect(self.show_hidden_game)
        self.stackedWidget.setCurrentWidget(self.hidden)

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

    def show_hidden_game(self, lv):
        if not hasattr(self, "hidden_game"):
            self.hidden_game = HGame(lv)
        else:
            self.stackedWidget.removeWidget(self.hidden_game)
            self.hidden_game.close()
            delattr(self, "hidden_game")
            self.hidden_game = HGame(lv)
        self.stackedWidget.addWidget(self.hidden_game)
        self.hidden_game.redirect_hidden.connect(self.show_hidden)
        self.stackedWidget.setCurrentWidget(self.hidden_game)
    
if __name__ == "__main__":
    app = QApplication([])
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())