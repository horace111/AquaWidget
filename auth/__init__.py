import os
import threading

import auth.avatar
import auth.login

from stdqt import *

CLIENT_SECRET = ''

def user_login_flow() -> str:
    return auth.login.user_login_flow()

class MainWindowHeader(QPushButton):
    static_unique_main_window_header_instance = None  # 这类的实例全局且唯一
    client_secret = ''

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.clicked.connect(auth.login.user_login_flow)
        self.headerImage = ''  # 和 Qt 命名格式一样
        self.setObjectName('MainWindowHeader')
        self.setMouseTracking(True)  # 否则 Qt 为了节省资源, 会仅在鼠标按下的时候跟踪
        self.setStyleSheet(
            f"""QPushButton#MainWindowHeader {'{'}
                border-image: url({self.headerImage});
                border: 1px solid black;
                border-radius: 30px
                {'}'}"""
        )  # 在 self.headerImage 有值前, 显示默认样式
        MainWindowHeader.static_unique_main_window_header_instance = self
        self._thread_onstart_auto_login()
    def setHeaderImageUrl(self, url:str) -> None:
        self.headerImage = url
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
    def onstart_auto_login(self):
        if os.path.exists('./auth/temp/cached'):
            with open('./auth/temp/cached', 'r', encoding='utf-8') as f:
                account, dsign, sign = f.read().split('\n')
            _cs = auth.login.login_via_signatures(account, dsign, sign)
            if _cs:
                CLIENT_SECRET = _cs
                MainWindowHeader.client_secret = _cs
                self.setHeaderImageUrl(auth.avatar.query(account))
    def _thread_onstart_auto_login(self):
        threading.Thread(target=self.onstart_auto_login).start()