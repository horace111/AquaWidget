import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

class AquaWidget(QWidget):
    def __init__(self, parent = ..., flags = ..., scale:tuple=(200, 200)):
        super().__init__(parent, flags)
        self.dx , self.dy = scale
    
NOPARENT = QWidget()

def noqapp():
    QtWidgets.QApplication(sys.argv)