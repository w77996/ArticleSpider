import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

def get_xsrf():
    reponses = requests.get("https://www.zhihu.com")
    print(reponses.text)
    return ""

def zhihu_login(account,password):
#     知乎登录
    if re.match("^1\d{10}",account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "xsrf":""
            ""
        }

