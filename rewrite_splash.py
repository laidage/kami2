from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import time

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640

class Splash(QSplashScreen):
    def __init__(self):
        super(Splash, self).__init__()
        self.setPixmap(QPixmap('./assets/welcome.png').scaled(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.show()
        time.sleep(3)

    def mousePressEvent(self, evt):
        pass
        # 重写鼠标点击事件，阻止点击后消失
    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象
    def enterEvent(self, *args, **kwargs):
        pass
        # 重写鼠标移动事件，阻止出现卡顿现象
    def mouseMoveEvent(self, *args, **kwargs):
        pass