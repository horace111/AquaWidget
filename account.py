from stdqt import *

class MainWindowHeader(QPushButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.image = QImage('https://q.qlogo.cn/headimg_dl?dst_uin=986561577&spec=100&img_type=jpg')
        self.setObjectName('MainWindowHeader')
        self.setStyleSheet(
            """QPushButton#MainWindowHeader {
            border-image: url(./resources/986561577.jpg);
            border: 1px solid black;
            border-radius: 30px
            }"""
        )
    def setImage(self, url:str) -> None:
        self.image
        pass
    def mousePressEvent(self, e):
        self.setStyleSheet(
            """QPushButton#MainWindowHeader {
            background-color: black;
            border: 1px solid black;
            border-radius: 30px
            }"""
        )
        return super().mousePressEvent(e)
    def mouseReleaseEvent(self, e):
        # 或者通过一个半透明颜色直接覆盖在上面  .show()  .hide()
        self.setStyleSheet(
            """QPushButton#MainWindowHeader {
            border-image: url(./resources/986561577.jpg);
            border: 1px solid black;
            border-radius: 30px
            }"""
        )
        return super().mouseReleaseEvent(e)