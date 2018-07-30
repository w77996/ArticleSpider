import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.text")

try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    'User-agent': agent
}

def is_login():
    #用户是否为登录
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header,allow_redirect=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print ("ok")

def get_xsrf():
    reponses = session.get("https://www.zhihu.com",headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', reponses.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

def zhihu_login(account,password):
#     知乎登录
    if re.match("^1\d{10}",account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "xsrf": get_xsrf(),
            "phone_num":account,
            "password":password
        }

    else:
        if "@" in account:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "xsrf": get_xsrf(),
                "email": account,
                "password": password
            }
    session.post(post_url, data=post_data, headers=header)
    session.cookies.save()

# get_xsrf()
zhihu_login("18520540560","")
