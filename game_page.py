import json
import random
import sys, os
from utils import get_triangles, whichTriangle

from PySide6.QtCore import QSize, Qt, QPoint, QObject, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPolygon, QColor, QBrush, QPen
from game_logic2 import Env
import functools
from utils import tran_state
from net import Net
import torch


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
    def __init__(self, lv):
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
        with open('kami_state.json', 'r') as f:
            self.global_state = json.load(f)
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
            reload_config = -1
            if self.current_step >= 0:
                if self.global_state["travel_level"][self.lv - 1] < 2:
                    self.global_state["travel_level"][self.lv - 1] = 2
                    with open('kami_state.json', 'w') as f:
                        json.dump(self.global_state, f)
                    reload_config = self.lv
            else:
                if self.global_state["travel_level"][self.lv - 1] == 0:
                    self.global_state["travel_level"][self.lv - 1] = 1
                    with open('kami_state.json', 'w') as f:
                        json.dump(self.global_state, f)
                    reload_config = self.lv
            self.back(reload_config)
        
        
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
        width = (SCREEN_WIDTH - 144) // self.colors
        x, y = 144 + width * (index + 1) - 20,  82 * 14 // 2
        if index == self.colors - 1:
            x = SCREEN_WIDTH - 20
        self.selected_color_button.setGeometry(x, y, 20, 20)


    def draw_handle_buttons(self):
        width = 144 // 4
        height = SCREEN_HEIGHT - 82 * 14 // 2
        icons = ["./assets/back.png", "", "./assets/refresh.png", "./assets/tip.png"]
        funcs = [functools.partial(self.back, -1), None, self.refresh, self.tip]
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
            button.setStyleSheet("border: 0; background-color: rgb" + str(self.color_rgbs[i])+"; border-top: 1px dotted #241b0d;")
            button.setGeometry(x, y, width, height)
            button.clicked.connect(functools.partial(self.selectColor, i))
        self.selected_color_button = QPushButton("", self)
        self.selected_color_button.setIcon(QIcon('./assets/selected.png'))
        self.selected_color_button.setIconSize(QSize(30, 30))
        self.selectColor(0)

    def back(self, reload_config):
        self.redirect_travel.emit(reload_config)

    def refresh(self):
        self.triangle_colors, self.min_steps, self.colors, self.color_rgbs = self.env.init_game(self.lv)
        self.current_step = self.min_steps
        self.current_color_index = 0
        self.step_button.setText(str(self.current_step))
        self.draw_triangles(self.triangles)
        

    def tip(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch.set_default_dtype(torch.float16)
        # , map_location='cpu'
        self.net = Net().float().to(device)
        if os.path.exists("model/half_net.pth"):
            self.net.load_state_dict(torch.load("model/half_net.pth"))
        if self.net:
            state = tran_state(self.triangle_colors, self.colors)
            state = torch.tensor(state, dtype=torch.half).unsqueeze(0)
            state = state.float()
            with torch.no_grad():
                action =  self.net(state).max(1)[1].view(1, 1)
                x, y, color = self.env.tran_action(action.item())
                print(x, y, color)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(basedir, "assets", "app_icon.ico")))
    app.setWindowIcon(QIcon("./assets/app_icon.ico"))
    window = Game(3)
    window.show()

    app.exec_()
