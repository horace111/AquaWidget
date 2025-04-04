from stdqt import *

class MainWindowHeader(QPushButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headerImage = ''
        self.setObjectName('MainWindowHeader')
        self.setMouseTracking(True)  # 否则 Qt 为了节省资源, 会仅在鼠标按下的时候跟踪
        self.hide()  # 在 .headerImage 属性有值前, 都不显示出来
    def setHeaderImageUrl(self, url:str) -> None:
        self.headerImage = url
        if not self.isVisible():
            self.setStyleSheet(
                f"""QPushButton#MainWindowHeader {'{'}
                border-image: url({self.headerImage});
                border: 1px solid black;
                border-radius: 30px
                {'}'}"""
            )
            self.show()
    # 重写 mouseMoveEvent
    def mouseMoveEvent(self, e):
        if ((e.pos().x() - 30) ** 2 + (e.pos().y() - 30) ** 2) ** 0.5 <= 30:  # 注意减 30 是因为相对坐标
            self.setStyleSheet(
                """QPushButton#MainWindowHeader {
                background-color: green;
                border: 1px solid black;
                border-radius: 30px
                }"""
            )
        else:
            self.setStyleSheet(
                """QPushButton#MainWindowHeader {
                background-color: black;
                border: 1px solid black;
                border-radius: 30px
                }"""
            )
        return super().mouseMoveEvent(e)
    
    # 暂时不启用鼠标悬浮交互
    def mouseMoveEvent(self, e):
        return super().mouseMoveEvent(e)  
    
    # 重写 mousePressEvent
    # 或者通过一个半透明颜色直接覆盖在上面  .show()  .hide()  可能性能更佳
    # 4.4 补注: 现在认为上一行注释所述确为更佳实践. 我不想让 requests.get() 卡住主线程, 而在下完
    #           头像之后新线程应用下好的头像, 会干扰这些交互逻辑
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
        self.setStyleSheet(
            f"""QPushButton#MainWindowHeader {'{'}
            border-image: url({self.headerImage});
            border: 1px solid black;
            border-radius: 30px
            {'}'}"""
        )
        return super().mouseReleaseEvent(e)