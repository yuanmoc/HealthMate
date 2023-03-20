import io
import json
import os

from utils import config_util, cookie_util
from app import client_util

user_config_file = '.user_config.ini'

cities_file = '.cities'

config_section = 'default'

conf = {
    'username': '',
    'password': '',
    # 城市
    'city_id': int(),
    'city_name': '',
    # 医院编号
    'unit_id': int(),
    'unit_name': '',
    # 科室编号
    'dept_id': int(),
    'dept_name': '',
    # 挂号医生编号，可多选
    'doctor_ids': list([]),
    'doctor_names': list([]),
    # 挂号就诊人编号
    'member_id': int(),
    'member_name': '',
    # 挂号时间 具体日期
    'registration_days': list([]),
    # 挂号时间 上午=am，下午=pm 上下午am,pm
    'registration_am_pm': list(['am', 'pm']),
    # 定时抢号
    'fixed_time': 0,
    # 定时抢号时间段
    'time_range': list([]),
    # 抢号频率，单位：毫秒
    'time_rate': 1000
}

config = config_util.Config(user_config_file)
conf = config.getConfigToDict(config_section, conf)


def get_config():
    return conf


def get_user_config(key):
    return conf.get(key)


def save_user_config(key, value):
    conf[key] = value
    config.set('default', key, value)


def clear_user_config():
    if os.path.exists(user_config_file):
        os.remove(user_config_file)
    if os.path.exists(cookie_util.cookie_file):
        os.remove(cookie_util.cookie_file)
    # if os.path.exists(cities_file):
    #     os.remove(cities_file)


def has_user_config():
    if os.path.exists(user_config_file):
        return True
    return False


def get_cities():
    cities = {}
    if os.path.exists(cities_file):
        f = io.open(cities_file, 'r')
        text = f.read()
        f.close()
        cities = json.loads(text)
    if cities is not None and len(cities) > 0:
        return cities
    cities = client_util.get_all_cities()
    f = io.open(cities_file, 'w', encoding='utf-8')
    f.write(json.dumps(cities, ensure_ascii=False))
    f.close()
    return cities


