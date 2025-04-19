import requests
import os
import re
import uuid
import hashlib
import wmi

from stdqt import *

CLIENT_SECRET = ''

def quickmap(**kwargs) -> dict:
    return kwargs

def login(account:str, password:str) -> str:
    data = quickmap(
        clientToken = str(uuid.uuid4()),
        account = account,
        signature = signature(account, password),
        devicedSignature = deviced_signature(account, password)
    )
    try:
        resp = requests.post('http://47.119.20.145:8000/api/v1/auth/login', json=data)
    except Exception:
        return None
    rmap = resp.json()
    if rmap['retcode'] == 10000:
        return rmap['data']['clientSecret']
    elif rmap['retcode'] >= 40000:
        return 'Incorrect'
    else:
        return None
    
def login_via_signatures(account:str, _signature:str, _deviced_signature:str) -> str:
    data = quickmap(
        clientToken = str(uuid.uuid4()),
        account = account,
        signature = _signature,
        devicedSignature = _deviced_signature
    )
    try:
        resp = requests.post('http://47.119.20.145:8000/api/v1/auth/login', json=data)
    except Exception:
        return None
    rmap = resp.json()
    if rmap['retcode'] == 10000:
        return rmap['data']['clientSecret']
    elif rmap['retcode'] >= 40000:
        return 'Incorrect'
    else:
        return None

window = None  # 防止垃圾回收删掉 window

def md5(text:str) -> str:
    md5v = hashlib.md5(text.encode('utf-8')).hexdigest()
    return md5v

def neighexchange(text:str) -> str:
    if len(text) >= 2 and len(text) % 2 == 0:
        result = ''
        for i in range(int(len(text)/2)):
            result += text[ 2 * i + 1] + text[2 * i]
        return result
    else:
        return None

def get_device_uid() -> str:
    pc = wmi.WMI()
    id = ''
    atmp = pc.Win32_Processor()
    for cpu in atmp:
        id += cpu.ProcessorId.strip()
    for board in pc.Win32_BaseBoard():
        id += board.SerialNumber.strip()
    return id

def signature(account:str, password:str) -> str:
    return md5(account + md5(neighexchange(password)))

def deviced_signature(account:str, password:str) -> str:
    return md5(account + md5(neighexchange(password)) + md5(get_device_uid()))

def user_login_flow() -> None:
    global window
    window = QWidget()
    window.setGeometry(500, 500, 500, 500)

    is_account_legal_label = QLabel(window)
    is_account_legal_label.setGeometry(100, 140, 300, 30)
    is_account_legal_label.setText('请在上框输入邮箱账号')
    account_input = QLineEdit(window)
    account_input.setGeometry(100, 100, 300, 30)
    def _check_account(text:str) -> None:
        if not re.search(r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.com$', text):
            is_account_legal_label.setText('账号不符合规范')
        else:
            is_account_legal_label.setText('')
    account_input.textChanged.connect(_check_account)

    is_password_legal_label = QLabel(window)
    is_password_legal_label.setGeometry(100, 240, 300, 30)
    is_password_legal_label.setText('请在上框输入密码')
    password_input = QLineEdit(window)
    password_input.setGeometry(100, 200, 300, 30)
    def _check_password(text:str) -> None:
        if not re.search(r'^[a-zA-Z0-9]{8}[a-zA-Z0-9]*$', text):
            is_password_legal_label.setText('密码不符合规范')
        else:
            is_password_legal_label.setText('')
    password_input.textChanged.connect(_check_password)

    login_button = QPushButton(window)
    login_button.setGeometry(200, 300, 100, 30)
    login_button.setText('登录')
    def _login_action():
        client_secret = login(
            account_input.text(),
            password_input.text()
        )
        print(client_secret)
        CLIENT_SECRET = client_secret
        if client_secret:
            if client_secret == 'Incorrect':
                return
            else:
                if not os.path.exists('./auth/temp'):
                    os.mkdir('./auth/temp')
                with open('./auth/temp/cached', 'w', encoding='utf-8') as f:
                    f.write(f"{account_input.text()}\n{deviced_signature(account_input.text(), password_input.text())}\n{signature(account_input.text(), password_input.text())}")
                window.close()
    login_button.clicked.connect(_login_action)

    window.show()