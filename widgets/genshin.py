import sys

from PyQt5 import QtWidgets

class AquaWidget():
    def __init__(self, scale:tuple=(200, 200)):
        self.dx , self.dy = scale

def reg(parent:QtWidgets.QWidget) -> AquaWidget:
    widget = AquaWidget(scale=(200, 200))
    text1 = QtWidgets.QLabel('我要玩原神！', parent=parent)
    return widget