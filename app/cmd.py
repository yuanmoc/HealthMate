import click
from app import info, client_config, client_util


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


@click.command(help='清除信息')
def clear():
    client_config.clear_user_config()


@click.command(help='启动挂号')
def start():
    pass


cmd.add_command(version)
cmd.add_command(init)
cmd.add_command(clear)
cmd.add_command(init_reg)
cmd.add_command(start)
cmd.add_command(init_cron)



def init_config():
    username = input_config_value('username', '请输入用户名: ')
    password = input_config_value('password', '请输入密码: ')
    # 登录
    client_util.init_login_cookie(username, password)
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
    select_registration_days()
    select_cron()


def init_registration():
    username = client_config.get_user_config('username')
    password = client_config.get_user_config('password')
    # 登录
    client_util.init_login_cookie(username, password)
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
    select_registration_days()
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
    client_config.save_user_config('city_id', city_id)
    client_config.save_user_config('city_name', city_name)


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
    client_config.save_user_config('unit_id', unit_id)
    client_config.save_user_config('unit_name', unit_name)


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
    client_config.save_user_config('dept_id', dept_id)
    client_config.save_user_config('dept_name', dept_name)


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
    if len(doctor_id_list) != len(doctor_name_list):
        print('你选择的医生不存在', doctor_id_list, doctor_name_list)
        exit(0)
    client_config.save_user_config('doctor_ids', doctor_id_list)
    client_config.save_user_config('doctor_names', doctor_name_list)


def select_member():
    member_list = client_util.get_member()
    if member_list is None or len(member_list) == 0:
        print('请添加好就诊人后再在挂号')
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
    client_config.save_user_config('member_id', member_id)
    client_config.save_user_config('member_name', member_name)


def select_registration_days():
    input_config_value('registration_days', '挂号时间段，默认全部，如：2023-11-12,2023-11-15: ')
    input_config_value('registration_am_pm', '挂号时间（上午,下午），默认全部，如：am,pm: ')
    input_config_value('time_rate', '挂号轮询时间间隔(单位毫秒)，默认10000: ')


def select_cron():
    input_config_value('time_range', '抢号时间段，默认启动挂号，如：2023-11-15 11:12:00,2023-11-16 11:12:00\n')


def input_config_value(key, desc):
    value = input(desc)
    if value is None or value == '':
        return None
    client_config.save_user_config(key, value)
    return value
