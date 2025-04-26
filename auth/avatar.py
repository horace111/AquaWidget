import requests
import os
from winenvvars import TEMP

def query(em:str) -> str:
    """
    Return value is the avatar path.
    """
    r = requests.get('http://47.119.20.145:8000/api/v1/auth/avatar', params={"account": em}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'})
    try:
        with open(f"{TEMP}/AquaWidget/user_avatar.png", 'wb') as f:
            f.write(r.content)
    except FileNotFoundError:
        os.mkdir(f"{TEMP}/AquaWidget")
        with open(f"{TEMP}/AquaWidget/user_avatar.png", 'wb') as f:
            f.write(r.content)
    # return f"{TEMP}/AquaWidget/{em}.png"
    return f"{TEMP}/AquaWidget/user_avatar.png"

# https://q.qlogo.cn/headimg_dl?dst_uin=986561577&spec=100&img_type=png