import io
import json
import os.path
import threading
import time

cookie_file = '.cookie.txt'

cookie_json = {}


def save_cookie():
    """
    保存cookie到文件
    :param cookie: cookie {key: value}
    :return:
    """
    if cookie_json is None or len(cookie_json) <= 0:
        return
    f = io.open(cookie_file, 'w', encoding='Utf-8')
    f.write(json.dumps(cookie_json, ensure_ascii=False))
    f.close()


def save_thread():
    while True:
        save_cookie()
        time.sleep(20)


save_thread = threading.Thread(target=save_thread)
save_thread.daemon = True
save_thread.start()


def save_session_cookie(cookies):
    """
    保存session cookie
    :param cookies: request.session.cookies
    :return:
    """
    if cookies is None:
        return
    cookie = get_cookie_json_from_file()
    if cookie is None or len(cookie) <= 0:
        cookie = {}
    for c in cookies:
        cookie[c.name] = c.value
    global cookie_json
    cookie_json = cookie


def get_cookie_json_from_file():
    """
    从文件中获取cookie
    :return:
    """
    global cookie_json
    if cookie_json is not None and len(cookie_json) > 0:
        return cookie_json

    exists_file = os.path.exists(cookie_file)
    if not exists_file:
        return None
    file = io.open(cookie_file, 'r', encoding='Utf-8')
    re = file.read()
    file.close()
    if re is None or re == '':
        return None
    cookie_json = json.loads(re)
    return cookie_json


def get_cookie_string_from_file():
    """
    获取拼接好的cookie字符串
    :return:
    """
    json_cookie = get_cookie_json_from_file()
    if json_cookie is None:
        return None
    cookie = ''
    for key in json_cookie.keys():
        cookie = cookie + key + '=' + json_cookie.get(key) + '; '
    return cookie


def get_cookie_value(name):
    """
    获取cookie值
    :param name: cookie键
    :return:
    """
    json_cookie = get_cookie_json_from_file()
    return json_cookie.get(name)
