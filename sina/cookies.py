import requests

weibo = [
        {'no': 'account@sina.com', 'psw': 'password'},
    ]

headers = {
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http://weibo.cn/&backTitle=%CE%A2%B2%A9&vt=',
    }

s = requests.session()
s.headers = headers


def login(username, password):
    url = 'https://passport.weibo.cn/sso/login'
    data = {
            'username': username,
            'password': password,
            'savestate': '1',
            'r': 'http://weibo.cn/',
            'ec': '0',
            'pagerefer': '',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
            }
    response = s.post(url, data=data)
    return response


def login_after(response):
    url = response.get('data').get('crossdomainlist').get('weibo.com').replace('\\', '')
    content = s.get(url)
    print(content.status_code)

    url = response.get('data').get('crossdomainlist').get('sina.com.cn').replace('\\', '')
    content = s.get(url)
    print(content.status_code)

    url = response.get('data').get('crossdomainlist').get('weibo.cn').replace('\\', '')
    content = s.get(url)
    print(content.status_code)


def get_cookies():
    cookies = []
    for item in weibo:
        response = login(item.get('no'), item.get('psw'))
        print(response.status_code)

        login_after(eval(response.text))
        cookies.append(s.cookies.get_dict())

    return cookies
