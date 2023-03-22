import threading

import click
from app import info, client_util, client_config


@click.group()
def cmd():
    pass


@click.command(name='version', help='版本号')
def version():
    click.echo(info.__name__ + ' -> ' + str(info.__version__))


@click.command(help='初始化信息')
def init():
    init_config()


@click.command(help='初始化挂号信息')
def init_reg():
    init_registration()


@click.command(help='设置定时挂号信息')
def init_cron():
    select_cron()


@click.command(help='设置挂号时间')
def init_reg_day():
    select_registration_days()

@click.command(help='清除信息')
def clear():
    client_config.clear_user_config()


@click.command(help='启动挂号')
def start():
    task_thread = threading.Thread(target=task)
    task_thread.daemon = True
    task_thread.start()

def task():
    while True:
        if client_util.registration_task():
            print('挂号成功')
            return


cmd.add_command(version)
cmd.add_command(init)
cmd.add_command(clear)
cmd.add_command(init_reg)
cmd.add_command(init_reg_day)
cmd.add_command(start)
cmd.add_command(init_cron)


def init_config():
    username = input('请输入用户名: ')
    client_config.save_user_config('username', username, True)
    password = input('请输入密码: ')
    client_config.save_user_config('password', password)
    # 登录
    flag = client_util.init_login_cookie(username, password)
    if not flag:
        print('登录失败')
        exit(0)
    init_registration()


def init_registration():
    # 选择城市
    select_city()
    # 选择医院
    select_unit()
    # 选择科室
    select_dept()
    # 选择医生
    select_doctor()
    # 选择就诊人
    select_member()
    # 挂号信息
    select_registration_days()
    # 定时任务
    select_cron()


def select_city():
    city_name = input('请输入医院城市名称: ')
    cities = client_util.search_city(client_config.get_cities(), city_name)
    print("===== 城市（输入你选择的城市编号） ======")
    for city in cities:
        print("城市名称: ", city.get('name'), '-->', "城市编号: ", city.get('cityId'))
    city_id = input("输入以上查询出来的城市编号: ")

    city_name = None
    for city in cities:
        if int(city_id) == int(city.get('cityId')):
            city_name = city.get('name')
    if city_name is None:
        print('你选择的城市不存在')
        exit(0)
    client_config.save_user_config('city_id', city_id, True)
    client_config.save_user_config('city_name', city_name, True)


def select_unit():
    unit_name = input('请输入医院名称: ')
    units = client_util.search_unit_by_city(client_config.get_user_config('city_id'), unit_name)
    print("===== 医院（输入你选择的医院编号） ======")
    for unit in units:
        print("医院名称: ", unit.get('unit_name'), '-->', "医院编号: ", unit.get('unit_id'))
    unit_id = input("输入以上查询出来的医院编号: ")

    unit_name = None
    for unit in units:
        if int(unit_id) == int(unit.get('unit_id')):
            unit_name = unit.get('unit_name')
    if unit_name is None:
        print('你选择的医院不存在')
        exit(0)
    client_config.save_user_config('unit_id', unit_id, True)
    client_config.save_user_config('unit_name', unit_name, True)


def select_dept():
    dept_name = input('请输入科室名称: ')
    depts = client_util.search_dept_by_unit(client_config.get_user_config('unit_id'), dept_name)
    print("===== 科室（输入你选择的科室编号） ======")
    for dept in depts:
        print("科室名称: ", dept.get('dep_name'), '-->', "科室编号: ", dept.get('dep_id'))
    dept_id = input("输入以上查询出来的科室编号: ")

    dept_name = None
    for dept in depts:
        if int(dept_id) == int(dept.get('dep_id')):
            dept_name = dept.get('dep_name')
    if dept_name is None:
        print('你选择的科室不存在')
        exit(0)
    client_config.save_user_config('dept_id', dept_id, True)
    client_config.save_user_config('dept_name', dept_name, True)


def select_doctor():
    doctor_name = input('输入医生名称（不输入列出全部）: ')
    data = client_util.get_sch_edp(client_config.get_user_config('unit_id'), client_config.get_user_config('dept_id'))
    doc = data.get('data').get('doc')
    print("===== 医生（输入你选择的医生编号）=====")
    for doctor in doc:
        if doctor_name is None or doctor_name == '':
            print(doctor.get('doctor_name'), '(', doctor.get('zc_name'), ')', '-->', '医生编号：',
                  doctor.get('doctor_id'), '-->' + doctor.get('expert'))
        elif doctor_name in doctor.get('doctor_name'):
            print(doctor.get('doctor_name'), '(', doctor.get('zc_name'), ')', '-->', '医生编号：',
                  doctor.get('doctor_id'), '-->' + doctor.get('expert'))

    doctor_ids_str = input('输入医生编号（多个使用,分隔）: ')
    doctor_id_list = doctor_ids_str.split(',')
    doctor_name_list = []
    for doctor_id in doctor_id_list:
        for doctor in doc:
            if int(doctor_id) == int(doctor.get('doctor_id')):
                doctor_name_list.append(doctor.get('doctor_name'))
    if doctor_name_list is None or len(doctor_id_list) != len(doctor_name_list):
        print('你选择的医生不存在', doctor_id_list, doctor_name_list)
        exit(0)
    client_config.save_user_config('doctor_ids', doctor_id_list, True)
    client_config.save_user_config('doctor_names', doctor_name_list, True)


def select_member():
    member_list = client_util.get_member()
    if member_list is None or len(member_list) == 0:
        print('请添加好就诊人后再在挂号,地址：https://user.91160.com/member.html')
        exit(0)
    for member in member_list:
        print('就诊人：', member.get('name'), '-->', '编号', member.get('id'))
    member_id = input('输入就诊人编号: ')
    member_name = None
    for member in member_list:
        if int(member_id) == int(member.get('id')):
            member_name = member.get('name')
    if member_name is None:
        input('输入就诊人编号有误')
        exit(0)
    client_config.save_user_config('member_id', member_id, True)
    client_config.save_user_config('member_name', member_name, True)


def select_registration_days():
    registration_days = input('挂号时间段，默认全部，如：2023-11-12,2023-11-15\n')
    client_config.save_user_config('registration_days', registration_days.split(','), True)
    registration_am_pm = input('挂号时间（上午,下午），默认全部，如：am,pm: ')
    if registration_am_pm == '' or registration_am_pm is None:
        registration_am_pm = 'am,pm'
    client_config.save_user_config('registration_am_pm', registration_am_pm.split(','), True)
    time_rate = input('挂号轮询时间间隔(单位毫秒)，默认1000: ')
    if time_rate == '' or time_rate is None:
        time_rate = '1000'
    client_config.save_user_config('time_rate', time_rate, True)


def select_cron():
    fixed_time = input('定时抢号yes/no: ')
    if fixed_time == 'yes':
        fixed_time_value = 1
    else:
        fixed_time_value = 0
    client_config.save_user_config('fixed_time', fixed_time_value, True)
    time_range = input('抢号时间段，如：2023-11-15 11:12:00,2023-11-16 11:12:00\n')
    client_config.save_user_config('time_range', time_range.split(','), True)
    print_config_info()


def print_config_info():
    config = client_config.get_config()
    print("当前用户配置如下：")
    print('用户名: ', config.get('username'))
    print('城市: ', config.get('city_name'))
    print('医院: ', config.get('unit_name'))
    print('科室: ', config.get('dept_name'))
    print('医生: ', config.get('doctor_names'))
    print('就诊人: ', config.get('member_name'))
    print('挂号时间: ', config.get('registration_days'))
    print('挂号时间: ', config.get('registration_am_pm'))
    print('抢号频率: ', config.get('time_rate'), '(毫秒)')
    print('是否定时抢号: ', 'yes' if int(config.get('fixed_time')) == 1 else 'no')
    print('定时抢号时间段: ', config.get('time_range'))
