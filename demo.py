import sys
import uuid
import widgets

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

app = QtWidgets.QApplication(sys.argv)



def main():
    window = QWidget()
    
    def _acquire_qw() -> QWidget:
        qw = QWidget(parent=window)
        qwon = str(uuid.uuid4())
        qw.setObjectName(qwon)
        qw.setStyleSheet(f"QWidget#{qwon}{'{'}border: 1px solid black;border-radius: 30px{'}'}")
        return qw

    window.setGeometry(760, 120, 300, 600)

    widgets.set_acquire_func(_acquire_qw)
    widgets.reg_all()

    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()