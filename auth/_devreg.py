import hashlib
import wmi

def quickmap(**kwargs) -> dict:
    return kwargs

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

if __name__ == '__main__':
    pw = input('请输入你的密码')
    _cf = input('上面的输入是否正确? 如果不正确，请在此修改，否则留空')
    if _cf: pa = _cf
    sig = signature('2892439741@qq.com', pw)
    dsig = deviced_signature('2892439741@qq.com', pw)
    with open('./sig.txt', 'w', encoding='utf-8') as f:
        f.write(f"sig:{sig}\ndsig:{dsig}")