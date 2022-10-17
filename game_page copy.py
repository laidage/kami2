import random
import sys, os
from utils import get_triangles, whichTriangle

from PySide6.QtCore import QSize, Qt, QPoint, QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen, QPalette
from game_logic2 import Env
import functools 
import torch
from net import Net


basedir = os.getcwd()
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'kami2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

colors = [Qt.red, Qt.blue, Qt.green]
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

def bind(objectName, propertyName):
    def getter(self):
        return self.findChild(QObject, objectName).property(propertyName)

    def setter(self, value):
        self.findChild(QObject, objectName).setProperty(propertyName, value)

    return property(getter, setter)

class Game(QLabel):
    # current_step = bind("step_button", "text")
    redirect_travel = Signal(int)
    def __init__(self, lv=1, model=None):
        super().__init__()
        self.lv = lv
        self.setWindowTitle("kami2")
        # canvas = QPixmap(400, 300)
        canvas = QPixmap(SCREEN_WIDTH,SCREEN_HEIGHT)
        # canvas.fill(Qt.green)
        self.setPixmap(canvas)
        self.env = Env()
        # self.step_button = QPushButton("", self)
        
        self.triangle_colors, self.min_steps, self.colors, self.color_rgbs = self.env.init_game(self.lv)
        self.current_step = self.min_steps
        self.qcolors = [QColor(*rgb) for rgb in self.color_rgbs]
        self.current_color_index = 0
        self.triangles = get_triangles()
        self.draw_triangles(self.triangles)
        self.draw_handle_buttons()
        self.draw_color_buttons()
        self.mousePressEvent = self.pressEvent
        self.model = model
        # self.setMenuWidget(button2)

        # Set the central widget of the Window.
    def pressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() != Qt.LeftButton:   ##判断是否鼠标左键点击
            return
        pos = QMouseEvent.pos()
        x, y = whichTriangle(pos.x(), pos.y(), self.triangles)
        color_index = self.current_color_index
        self.triangle_colors, reward, done = self.env.change_color(x, y, color_index)
        if reward == 0:
            return 
        self.current_step -= 1
        self.step_button.setText(str(self.current_step))
        self.draw_triangles(self.triangles)
        if done:
            self.back()
        
        
    def draw_one_color(self, triangles_index, color):
        canvas = self.pixmap()
        painter = QPainter(canvas)
        for xy_index in triangles_index:
            x, y = xy_index
            triangle = self.triangles[x][y]
            points = QPolygon([
                    QPoint(*triangle[0]),
                    QPoint(*triangle[1]),
                    QPoint(*triangle[2])
                ])
            brush = QBrush()
            # color = random.choice(colors)
            brush.setColor(color)
            # brush.setStyle(Qt.SolidPattern)
            brush.setStyle(Qt.Dense7Pattern)
            painter.setBrush(brush)
            pen = QPen()
            pen.setWidth(0)
            pen.setStyle(Qt.PenStyle.SolidLine)
            pen.setColor(color)
            painter.setPen(pen)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.drawPolygon(points,Qt.WindingFill)
        painter.end()
        self.setPixmap(canvas)

    def draw_triangles(self, triangles):
        canvas = self.pixmap()
        painter = QPainter(canvas)
        # painter.setRenderHint(QPainter.LosslessImageRendering, True)
        for i, column in enumerate(triangles):
            for j, triangle in enumerate(column):
                points = QPolygon([
                    QPoint(*triangle[0]),
                    QPoint(*triangle[1]),
                    QPoint(*triangle[2])
                ])
                brush = QBrush()
                # color = random.choice(colors)
                color = self.qcolors[self.triangle_colors[i][j]]
                brush.setColor(color)
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                pen = QPen()
                pen.setStyle(Qt.PenStyle.SolidLine)
                pen.setWidth(0)
                pen.setColor(color)
                painter.setPen(pen)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.drawPolygon(points,Qt.WindingFill)
        painter.end()
        self.setPixmap(canvas)

    def selectColor(self, index):
        self.current_color_index = index

    def draw_handle_buttons(self):
        width = 144 // 4
        height = SCREEN_HEIGHT - 82 * 14 // 2
        icons = ["./assets/back.png", "", "./assets/refresh.png", "./assets/tip.png"]
        funcs = [self.back, None, self.refresh, self.tip]
        for i in range(4):
            x = i * width
            y = 82 * 14 // 2
            button = QPushButton("", self)
            button.setStyleSheet("border: 0; background-color: #241b0d;")
            button.setIcon(QIcon(icons[i]))
            button.setIconSize(QSize(60, 60))
            button.setGeometry(x, y, width, height)
            if i < 3:
                button.setStyleSheet("border: 0; background-color: #241b0d; border-right: 1px solid white; color: white; font-size: 22px;")
            if i == 1:
                button.setText(str(self.current_step))
                self.step_button = button
            button.clicked.connect(funcs[i])
    
    def draw_color_buttons(self):
        # 画颜色按钮，并添加监听器
        # canvas = self.pixmap()
        width = (SCREEN_WIDTH - 144) // self.colors
        height = SCREEN_HEIGHT - 82 * 14 // 2
        for i in range(self.colors):
            x = 144 + i * width
            y = 82 * 14 // 2
            button = QPushButton("", self)
            # print(str(self.color_rgbs[i]))
            # print("background-color: " + str(self.color_rgbs[i])+";")
            button.setStyleSheet("border: 0; background-color: rgb" + str(self.color_rgbs[i])+"; border-top: 1px dotted #241b0d;")
            button.setGeometry(x, y, width, height)
            button.clicked.connect(functools.partial(self.selectColor, i))

    def back(self):
        self.redirect_travel.emit(1)

    def refresh(self):
        self.triangle_colors, self.min_steps, self.colors, self.color_rgbs = self.env.init_game(self.lv)
        self.current_step = self.min_steps
        self.current_color_index = 0
        self.step_button.setText(str(self.current_step))
        self.draw_triangles(self.triangles)
        

    def tip(self):
        if self.model:
            state = tran_state(self.triangle_colors, self.colors)
            state = torch.tensor(state, dtype=torch.half).unsqueeze(0)
            state = state.float()
            with torch.no_grad():
                action =  self.model(state).max(1)[1].view(1, 1)
                print(action)


    def clickTriangles(self):
        x, y, color = 0, 0, 0
        xy_indexs, _, _ = self.env.change_color(x, y, color)
        if not xy_indexs:
            return
        canvas = self.pixmap()
        painter = QPainter(canvas)
        for xy_index in xy_indexs:
            x, y = xy_index
            triangle = self.triangles[x][y]
            points = QPolygon([
                    QPoint(*triangle[0]),
                    QPoint(*triangle[1]),
                    QPoint(*triangle[2])
                ])
            brush = QBrush()
            # color = random.choice(colors)
            brush.setColor(color)
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            pen = QPen()
            pen.setWidthF(0)
            pen.setColor(color)
            painter.setPen(pen)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.drawPolygon(points,Qt.WindingFill)
        painter.end()
        self.setPixmap(canvas)

def tran_state(state, color_nums):
        trans_state = []
        for color_index in range(5):
            if color_index >= color_nums:
                trans_state.append([[-1 for _ in range(15)] for _ in range(20)])
                continue
            types = []
            for column_index in range(20):
                column = [0 for _ in range(15)]
                if column_index % 4 == 1 or column_index % 4 == 2: 
                    column[14] = -1
                types.append(column)
            trans_state.append(types)
        for i in range(20):
            for j in range(len(state[i])):
                color = state[i][j]
                trans_state[color][i][j] = 1
        return trans_state

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy_net = Net().float().to(device)
    if os.path.exists("model/half_net.pth"):
        policy_net.load_state_dict(torch.load("model/half_net.pth", map_location=torch.device('cpu')))
    policy_net = policy_net
    gameLabel = Game(36, policy_net)
    mainWindow = QMainWindow()
    mainWindow.setCentralWidget(gameLabel)
    mainWindow.show()

    app.exec_()
