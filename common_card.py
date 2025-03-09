from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsBlurEffect
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QPainter
from PyQt5.QtCore import Qt
from gui import Fonts

class BackGround(QGraphicsRectItem):
    def __init__(self, x, y, r = 30, w = 370, h = 370):
        super().__init__(x, y, w, h)
        self.radius = r
        self.setBrush(QBrush(QColor(204, 204, 204)))
        self.setPen(Qt.NoPen)

    def paint(self, painter):
        path = QPainterPath()
        path.addRoundedRect(self.rect(), self.radius, self.radius)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(path, self.brush())
        painter.drawPath(path)

