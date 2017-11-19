import requests
import string
import time
import random
import math
import urllib
import base64
import hashlib
import binascii
import rsa

s = requests.session()

# https://login.sina.com.cn/signup/signin.php?entry=sso

weibo = [
        {'no': 'account@sina.com', 'psw': 'password'},
    ]


'''
headers = {
    'Host':'login.sina.com.cn',
    'Origin':'https://login.sina.com.cn',
    'Referer':'https://login.sina.com.cn/signup/signin.php?entry=sso',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'
}
'''


def get_nonce():
    s = ''
    x = string.ascii_uppercase + string.digits
    for i in range(6):
        s += x[math.ceil(random.random() * 1000000) % len(x)]
    return s


def set_name(username):
    b = urllib.parse.quote(username)
    su = base64.b64encode(b.encode('utf-8'))
    return su


# sp: password = sinaSSOEncoder.hex_sha1("" + # sinaSSOEncoder.hex_sha1(sinaSSOEncoder.hex_sha1(password)) + me.servertime + me.nonce)
def set_password(password, timestamp, nonce):
    password_sha1_1 = hashlib.sha1(password.encode('utf-8')).hexdigest()
    password_sha1 = password_sha1_1 + timestamp[:-3] + nonce
    password_sha1_2 = hashlib.sha1(password_sha1.encode('utf-8')).hexdigest()
    password_sha1_3 = hashlib.sha1(password_sha1_2.encode('utf-8')).hexdigest()
    sp = password_sha1_3
    return sp


def get_sp(password, data):
    servertime = str(data.get('servertime'))
    nonce = data.get('nonce')

    key = rsa.PublicKey(int(data.get('pubkey'), 16), int('10001', 16))

    message = servertime + '\t' + nonce + '\n' + password
    passwd = binascii.b2a_hex(rsa.encrypt(message.encode('utf-8'), key))
    return passwd


def pre_login(username, timestamp):
    url = 'https://login.sina.com.cn/sso/prelogin.php'
    params = {
            'entry': 'sso',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': username,
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.15)',
            '_': timestamp
            }
    r = requests.get(url, params=params)
    # content = r.content
    content = eval(r.content.decode('utf-8').split('(')[1].split(')')[0])
    return content


def login(username, password, data):
    login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    form = {
            'entry': 'sso',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'pagerefer': 'https://login.sina.com.cn/sso/login.php',
            'vsnf': '1',
            'su': username,
            'service': 'sso',
            'servertime': data.get('servertime'),
            'nonce': data.get('nonce'),
            'pwencode': 'rsa2',
            'rsakv': data.get('rsakv'),
            'sp': password,
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': '30',
            'returntype': 'TEXT'
            }

    r = s.post(login_url, data=form)
    content = eval(r.content.decode('unicode-escape'))
    # print(content['reason'])
    return content


def login2(content):
    url = content.get('crossDomainUrlList')[0]
    response = s.get(url.replace('\\', ''))
    return response


def login3(content):
    url = content.get('crossDomainUrlList')[1]
    response = s.get(url.replace('\\', ''))
    return response


def get_cookies():
    cookies = []
    for item in weibo:
        # nonce = get_nonce()

        username = set_name(item.get('no'))
        timestamp = str(int(time.time()*1000))

        data = pre_login(username, timestamp)

        # password = set_password(item.get('psw'), timestamp, nonce)
        password = get_sp(item.get('psw'), data)
        response = login(username, password, data)
        print(response.get('retcode'))

        response_2 = login2(response)
        print(response_2.status_code)

        response_3 = login3(response)
        print(response_3.status_code)

        cookies.append(s.cookies.get_dict())

    return cookies
