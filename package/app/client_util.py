import random
import re
import json
import time

from utils import rsa_util, date_util, cookie_util, http_util
from app import user_log_util
from app import constants, client_config
import datetime

session = http_util.Session()

datetime_format = '%Y-%m-%d %H:%M:%S'

def requestBefore(**kwargs):
    """
    请求前处理
    :param kwargs: 头信息
    :return:
    """
    # 处理头信息
    headers = kwargs.get('headers')
    if headers is None:
        headers = {}
    # 设置cookie
    cookie = cookie_util.get_cookie_string_from_file()
    if cookie:
        headers['Cookie'] = cookie
    headers['User-Agent'] = random.choice(constants.ua)
    headers['Referer'] = constants.domain
    headers['origin'] = constants.domain
    kwargs['headers'] = headers

    proxies = {
        'http': 'http://113.124.86.24:9999'
    }
    kwargs['proxies'] = proxies
    return kwargs


def requestAfter(res):
    """
    请求后处理
    :return:
    """
    user_log_util.getLogger().info('请求: %s', res.url)
    # 保存cookie
    cookie_util.save_session_cookie(session.getCookies())

    if res.status_code != 200:
        user_log_util.getLogger().info('响应非200: %s-%s-%s', res.url, res.status_code, res.text)
        exit(1)
    content_type = res.headers.get('Content-Type')
    if content_type is None or 'json' not in content_type:
        return
    json_text = json.loads(res.text)
    error_code = json_text.get('error_code')
    error_msg = json_text.get('error_msg')
    result_code = json_text.get('result_code')
    if result_code is not None and int(result_code) != 1:
        user_log_util.getLogger().info("请求失败: %s-%s-%s", res.url, error_code, error_msg)
    if error_code is not None and int(error_code) == 10021:
        user_log_util.getLogger().info('用户需要重新登录')


session.before(requestBefore)
session.after(requestAfter)


def get_token():
    """
    获取登录页面token
    :return:
    """
    res = session.get(constants.login_url)
    token = re.search(r'id="tokens".*?value="(.*?)"', res.text, re.M | re.S | re.I).group(1)
    user_log_util.getLogger().info('token: %s', token)
    return token


def check_user(username, password, token):
    """
    检验用户
    :param username: 用户名
    :param password: 密码
    :param token: 登录页面token
    :return:
    """
    encrypt_username = rsa_util.encrypt_rsa(constants.public_key, username)
    encrypt_password = rsa_util.encrypt_rsa(constants.public_key, password)
    form_data = {
        'username': encrypt_username,
        'password': encrypt_password,
        'type': 'm',
        'token': token
    }
    res = session.formPost(constants.check_user_url, data=form_data)
    return True


def login(username, password, token):
    """
    登录
    :param username: 用户名
    :param password: 密码
    :param token: 登录页面token
    :return:
    """
    encrypt_username = rsa_util.encrypt_rsa(constants.public_key, username)
    encrypt_password = rsa_util.encrypt_rsa(constants.public_key, password)
    form_data = {
        'username': encrypt_username,
        'password': encrypt_password,
        'target': constants.domain,
        'error_num': '0',
        'token': token
    }
    res = session.formPost(constants.login_url, data=form_data)
    if res.history is None or len(res.history) <= 0:
        user_log_util.getLogger().info('登录失败，请检查用户名: %s和密码: %s', username, password)
        return False
    res = res.history.pop()
    if not res.is_redirect:
        user_log_util.getLogger().info('没有重定向，登录失败，请检查用户名和密码')
        return False
    location = res.url
    redirect1 = session.get(location)
    redirect1 = redirect1.history.pop()
    if redirect1.is_redirect:
        user_log_util.getLogger().info('登录成功')
        return True
    else:
        user_log_util.getLogger().info('登录失败')
        return False


def check_login_status():
    """
    检测cookie是否有效
    :return:
    """
    res = session.get(constants.account)
    if res.history:
        local = res.history.pop()
        if local.is_redirect:
            return False
    return True


def init_login_cookie(username, password):
    """
    初始化登录，并设置cookie信息
    :param username: 用户名
    :param password: 密码
    :return:
    """
    cookie = cookie_util.get_cookie_json_from_file()
    if cookie is not None and cookie != '':
        flag = check_login_status()
        if flag:
            return True
    token = get_token()
    check_user(username, password, token)
    return login(username, password, token)


def get_all_cities():
    res = session.get(constants.domain)
    data = re.search(r'var\s+cities\s+=(.*?);', res.text, re.M | re.S | re.I).group(1)
    return json.loads(data)

def search_city(cities, city_name):
    search_value = []
    for city in cities:
        if city_name in city.get('match'):
            search_value.append(city)
    return search_value


def get_all_unit_by_city(city_id):
    data = {
        'c': city_id
    }
    res = session.formPost(constants.get_unit_by_city, data=data)
    return json.loads(res.text)


def search_unit_by_city(city_id, unit_name):
    search_value = []
    units = get_all_unit_by_city(city_id)
    for unit in units:
        if unit_name in unit.get('unit_name'):
            search_value.append(unit)
    return search_value

def get_all_dept_by_unit(unit_id):
    data = {
        'keyValue': unit_id
    }
    res = session.formPost(constants.get_dept_by_unit, data=data)
    pubcats = json.loads(res.text)
    depts = []
    for pubcat in pubcats:
        pubcat_name = pubcat.get('pubcat')
        childs = pubcat.get('childs')
        if childs is None:
            continue
        for dept in childs:
            dept['dep_name'] = dept.get('dep_name') + "(" + pubcat_name +")"
            depts.append(dept)
    return depts


def search_dept_by_unit(unit_id, dept_name):
    search_value = []
    depts = get_all_dept_by_unit(unit_id)
    for dept in depts:
        if dept_name in dept.get('dep_name'):
            search_value.append(dept)
    return search_value


def get_sch_edp(unit_id, dept_id):
    """
    获取部门的挂号信息
    :param unit_id: 医院ID
    :param dept_id: 部门ID
    :return:
    """
    param_data = {
        'unit_id': unit_id,
        'dep_id': dept_id,
        'date': date_util.get_date_str(),
        'p': 0,
        'user_key': cookie_util.get_cookie_value('access_hash')
    }
    res = session.get(constants.sch_dep, params=param_data)
    data = json.loads(res.text)
    return data


def get_member() -> list:
    member_value = []
    res = session.get(constants.get_member)
    body = re.search(r'<tbody\s+id="mem_list">(.*?)</tbody>', res.text, re.M | re.S | re.I).group(1)

    all_member = re.findall(r'<tr(.*?)</tr>', body, re.M | re.S | re.I)
    for member in all_member:
        id = re.search(r'id="mem(.*?)"', member, re.M | re.S | re.I).group(1)
        infos = re.findall('<td>(.*?)<', member, re.M | re.S | re.I)
        name = infos[0]
        sex = infos[1]
        birth = infos[2]
        id_card = infos[3]
        cellphone = infos[4]
        member_value.append({
            'id': id,
            'name': name,
            'sex': sex,
            'birth': birth,
            'id_card': id_card,
            'cellphone': cellphone
        })
    return member_value


def do_submit(sch_data, unit_id, dept_id, doctor_id, schedule_id, mid, time_type, detlid, detlid_realtime, level_code):
    """
    提交预约订单
    :param sch_data: 提交订单页面里的 sch_data
    :param unit_id: 医院ID
    :param dept_id: 科室ID
    :param doctor_id: 医生ID
    :param schedule_id: 当天（上午/下午）预约 sch_id
    :param mid: 就诊人ID
    :param time_type: 时间类型am/pm
    :param detlid: 上午，下午（如时间段:9-10,11-12）预约 ID
    :param detlid_realtime: 提交订单页面里的 detlid_realtime
    :param level_code: 专家类型码，是普通号还是专家号等
    :return:
    """
    form_data = {
        "sch_data": sch_data,
        "unit_id": unit_id,
        "dep_id": dept_id,
        "doctor_id": doctor_id,
        "schedule_id": schedule_id,
        "mid": mid,
        "accept": "1",
        "time_type": time_type,
        "detlid": detlid,
        "detlid_realtime": detlid_realtime,
        "level_code": level_code,
        "addressId": '3317',
        "address": 'Civic Center'
    }
    res = session.formPost(constants.y_submit, data=form_data)
    if not res.history or len(res.history) == 0:
        user_log_util.getLogger().info('预约失败')
        return False
    local = res.history.pop()
    res = session.get(local.url)
    if '预约成功' in res.text:
        user_log_util.getLogger().info('预约成功')
        return True
    else:
        user_log_util.getLogger().info('预约失败')
        return False


def registration_task():
    conf = client_config.get_config()
    time_range = conf.get('time_range')
    fixed_time = conf.get('fixed_time')
    time_rate = conf.get('time_rate')
    member_id = conf.get('member_id')
    unit_id = conf.get('unit_id')
    dept_id = conf.get('dept_id')
    doctor_ids = conf.get('doctor_ids')
    registration_days = conf.get('registration_days')
    registration_am_pm = conf.get('registration_am_pm')
    if unit_id is None or unit_id <= 0:
        user_log_util.getLogger().info('医院不能为空，请选择后，再操作')
        time.sleep(2)
        return False
    if dept_id is None or dept_id <= 0:
        user_log_util.getLogger().info('科室不能为空，请选择后，再操作')
        time.sleep(2)
        return False
    if doctor_ids is None or len(doctor_ids) <= 0:
        user_log_util.getLogger().info('医生不能为空，请选择后，再操作')
        time.sleep(2)
        return False
    if member_id is None or member_id <= 0:
        user_log_util.getLogger().info('就诊人不能为空，请选择后，再操作')
        time.sleep(2)
        return False

    # 定时任务
    if fixed_time == 1 and time_range is not None and len(time_range) == 2:
        now = datetime.datetime.now()
        from_time = datetime.datetime.strptime(time_range[0], datetime_format)
        to_time = datetime.datetime.strptime(time_range[1], datetime_format)
        if from_time > now or to_time < now:
            user_log_util.getLogger().info('不在挂号时间内')
            time.sleep(0.5)
            return False
    sch_list = get_sch_list(unit_id, dept_id, doctor_ids, registration_days, registration_am_pm)
    for sch in sch_list:
        unit_id = sch.get('unit_id')
        dept_id = sch.get('dep_id')
        doctor_id = sch.get('doctor_id')
        schedule_id = sch.get('schedule_id')
        time_type = sch.get('time_type')
        mid = member_id
        level_code = sch.get('level_code')

        res = get_order(unit_id, dept_id, schedule_id)
        detlid_realtime = res.get('detlid_realtime')
        sch_data = res.get('sch_data')
        delts_value = res.get('delts_value')
        # 时间段号预约ID
        for delts in delts_value:
            detlid = delts.get('value')
            result = do_submit(sch_data, unit_id, dept_id, doctor_id, schedule_id, mid, time_type, detlid, detlid_realtime,
                  level_code)
            # 预约成功，退出
            if result:
                return True

    # 休眠后，再执行
    time.sleep(int(time_rate) / 1000)
    return False

def get_sch_list(unit_id, dept_id, doctor_ids, registration_days, registration_am_pm):
    sch_data = get_sch_edp(unit_id, dept_id)
    sch_list_value = []
    sch_list = sch_data.get('data').get('sch')
    for key in sch_list.keys():
        if key not in doctor_ids:
            continue
        sch = sch_list.get(key)
        ams = sch.get('am')
        if ams is not None and 'am' in registration_am_pm:
            for index in ams:
                am = ams.get(index)
                to_date = am.get('to_date')
                if am.get('y_state_desc') == '可预约' and registration_days is None or to_date in registration_days:
                    sch_list_value.append(am)
        pms = sch.get('pm')
        if pms is not None and 'pm' in registration_am_pm:
            for index in pms:
                pm = pms.get(index)
                to_date = pm.get('to_date')
                if pm.get('y_state_desc') == '可预约' and registration_days is None or to_date in registration_days:
                    sch_list_value.append(pm)
    return sch_list_value


def get_order(unit_id, dept_id, sch_id):
    res = session.get(constants.order % (unit_id, dept_id, sch_id))

    detlid_realtime = re.search(r'name="detlid_realtime"\s+value="(.*?)"', res.text, re.M | re.S | re.I).group(1)

    sch_data = re.search(r'name="sch_data"\s+value=\'(.*?)\'', res.text, re.M | re.S | re.I).group(1)

    delts = re.search(r'id="delts"(.*?)</ul>', res.text, re.M | re.S | re.I).group(1)
    delts_item_list = re.findall(r'<li(.*?)</li>', delts, re.M | re.S | re.I)
    delts_value = []
    for delts_item in delts_item_list:
        value = re.search(r'val="(.*?)"', delts_item, re.M | re.S | re.I).group(1)
        name = re.search(r'>(.*?)</', delts_item, re.M | re.S | re.I).group(1)
        delts_value.append({
            'name': name,
            'value': value
        })
    return {
        'detlid_realtime': detlid_realtime,
        'sch_data': sch_data,
        'delts_value': delts_value
    }
