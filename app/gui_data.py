import json
import os
import threading
from datetime import datetime, timedelta

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal, QEvent, Qt, QDateTime
import sys
from app import client_util, client_config, user_log_util

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)

data_format = '%Y-%m-%d'
q_datetime_format = 'yyyy-MM-dd HH:mm:ss'

class Login_Form(QtWidgets.QDialog):
    # 创建槽信号
    login_status = pyqtSignal()
    close_status = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = self.init_ui()
        self.ui.reset_button.clicked.connect(self.reset)
        self.ui.login_button.clicked.connect(self.login)
        self.my_close()

    def closeEvent(self, event):
        if not self.my_close_type:
            self.close_status.emit()

    def my_close(self):
        self.my_close_type = True
        self.close()
        self.my_close_type = False

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.my_close()
        return super().eventFilter(obj, event)

    def center(self):
        # 得到一个指定主窗口几何形状的矩形
        qr = self.frameGeometry()
        # 计算出显示器的分辨率，通过分辨率得出中心点
        cp = self.screen().availableGeometry().center()
        # 设置为屏幕的中心，矩形大小不变
        qr.moveCenter(cp)
        # 将应用程序的左上角移动到矩形的左上角，使屏幕在窗口正中
        self.move(qr.topLeft())

    def show(self) -> None:
        self.ui.username.setText(client_config.get_user_config('username'))
        self.setWindowFlag(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        self.setModal(True)
        super(Login_Form, self).show()

    def init_ui(self):
        return uic.loadUi(path+"/login-ui.ui", self)

    def reset(self):
        self.ui.username.clear()
        self.ui.pwd.clear()

    def login(self):
        username = self.ui.username.text()
        pwd = self.ui.pwd.text()
        if username is None or username == '' \
                or pwd is None or pwd == '':
            QMessageBox.warning(self, "标题", "用户名密码不能为空", QMessageBox.StandardButton.Ok)
            return
        user_log_util.getLogger().info('用户名：%s', username)
        client_config.save_user_config('username', username)
        self.ui.login_button.setEnabled(False)
        flag = client_util.init_login_cookie(username, pwd)
        if flag:
            self.login_status.emit()
            self.my_close()
        else:
            QMessageBox.warning(self, "标题", "登录失败", QMessageBox.StandardButton.Ok)
        self.ui.login_button.setEnabled(True)
class Main_Form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login_form = Login_Form()
        self.login_form.login_status.connect(self.login_change_status)
        self.login_form.close_status.connect(self.close)
        self.ui = self.init_ui()
        # 输出日志
        user_log_util.getLogger().set_callback(self.input_log)
        self.ui.log_input.clear()

        self.ui.login_button.clicked.connect(self.login_button_click)

        self.ui.city_box.clear()
        self.ui.city_box.clicked.connect(self.city_select)
        self.ui.city_box.currentIndexChanged[int].connect(self.city_change_event)

        self.ui.unit_box.clicked.connect(self.unit_select)
        self.ui.unit_box.currentIndexChanged[int].connect(self.unit_change_event)

        self.ui.dept_box.clicked.connect(self.dept_select)
        self.ui.dept_box.currentIndexChanged[int].connect(self.dept_change_event)

        self.ui.doctor_box.clear()
        self.ui.doctor_box.clicked.connect(self.doctor_select)
        self.ui.doctor_box.itemChecked[list].connect(self.doctor_change_event)

        self.ui.member_box.clear()
        self.ui.member_box.clicked.connect(self.member_select)
        self.ui.member_box.currentIndexChanged[int].connect(self.member_change_event)

        self.ui.registration_days_combo_box.clicked.connect(self.registration_days_select)
        self.ui.registration_days_combo_box.itemChecked[list].connect(self.registration_days_change_event)

        self.ui.am_check_box.stateChanged.connect(self.am_check_box_click)
        self.ui.pm_check_box.stateChanged.connect(self.pm_check_box_click)

        self.ui.time_rate_spin_box.textChanged.connect(self.time_rate_spin_box_input)

        self.ui.fixed_time_check_box.stateChanged.connect(self.fixed_time_click)

        self.ui.time_range_begin_datetime.dateChanged.connect(self.time_range_begin_select)
        self.ui.time_range_begin_datetime.setCalendarPopup(True)

        self.ui.time_range_end_datetime.dateChanged.connect(self.time_range_end_select)
        self.ui.time_range_end_datetime.setCalendarPopup(True)

        self.ui.task_button.clicked.connect(self.task_button_click)

        self.ui.log_label.mousePressEvent = self.clear_log

        self.init_data()

        self.task_thread = None
        self.task_activity = False

    def init_ui(self):
        return uic.loadUi(path+"/main-ui.ui", self)

    def input_log(self, msg):
        if isinstance(msg, str):
            self.ui.log_input.append(msg)
        if isinstance(msg, int):
            self.ui.log_input.append(str(msg))
        if isinstance(msg, dict):
            self.ui.log_input.append(json.dumps(msg, ensure_ascii=False))
        # 自动划到底
        self.ui.log_input.verticalScrollBar().setValue(self.ui.log_input.verticalScrollBar().maximum())

    def center(self):
        # 得到一个指定主窗口几何形状的矩形
        qr = self.frameGeometry()
        # 计算出显示器的分辨率，通过分辨率得出中心点
        cp = self.screen().availableGeometry().center()
        # 设置为屏幕的中心，矩形大小不变
        qr.moveCenter(cp)
        # 将应用程序的左上角移动到矩形的左上角，使屏幕在窗口正中
        self.move(qr.topLeft())


    def login_button_click(self):
        self.ui.login_button.setEnabled(False)
        if self.ui.login_button.text() == '退出登录':
            self.logout()
            self.ui.login_button.setEnabled(True)
            return True
        flag = client_util.check_login_status()
        if flag:
            self.login_change_status()
            self.ui.login_button.setEnabled(True)
            return True
        self.login_form.show()
        self.ui.login_button.setEnabled(True)
        return False

    def login_change_status(self):
        self.ui.login_button.setText('退出登录')
        self.init_data()

    def logout(self):
        client_config.clear_user_config()
        self.ui.login_button.setText('点击登录')

    def init_data(self):
        username = client_config.get_user_config('username')
        if username == '' or username is None or not client_util.check_login_status():
            self.login_form.show()
            return
        self.ui.login_button.setText('退出登录')
        # 就诊人
        member_id = client_config.get_user_config('member_id')
        if member_id is not None and member_id > 0:
            self.member_select()
            index = self.ui.city_box.findData(member_id)
            self.ui.member_box.setCurrentIndex(index)

        # 挂号时间
        self.registration_days_select()
        registration_days = client_config.get_user_config('registration_days')
        if registration_days is not None and len(registration_days) > 0:
            for registration_day in registration_days:
                self.ui.registration_days_combo_box.check_ok(registration_day)

        registration_am_pm = client_config.get_user_config('registration_am_pm')
        if registration_am_pm is not None and len(registration_am_pm) > 0:
            if 'am' in registration_am_pm:
                self.ui.am_check_box.setChecked(True)
            if 'pm' in registration_am_pm:
                self.ui.pm_check_box.setChecked(True)
        else:
            self.ui.am_check_box.setChecked(True)
            self.ui.pm_check_box.setChecked(True)

        # 定时抢号
        fixed_time = client_config.get_user_config('fixed_time')
        if fixed_time is not None and fixed_time != '':
            self.ui.fixed_time_check_box.setChecked(fixed_time == 1)

        time_range = client_config.get_user_config('time_range')
        if time_range is not None and len(time_range) > 0:
            self.ui.time_range_begin_datetime.setDateTime(QDateTime.fromString(time_range[0], q_datetime_format))
            self.ui.time_range_end_datetime.setDateTime(QDateTime.fromString(time_range[1], q_datetime_format))
        else:
            self.ui.time_range_begin_datetime.setDateTime(QDateTime.currentDateTime())
            self.ui.time_range_end_datetime.setDateTime(QDateTime.currentDateTime())

        # 抢时频率
        time_rate = client_config.get_user_config('time_rate')
        if time_rate is not None and time_rate != '':
            self.ui.time_rate_spin_box.setValue(time_rate)
        else:
            self.ui.time_rate_spin_box.setValue(1000)

        # city
        city_id = client_config.get_user_config('city_id')
        if city_id is None or city_id < 0:
            return
        self.city_select()
        index = self.ui.city_box.findData(city_id)
        if index == -1:
            return
        self.ui.city_box.setCurrentIndex(index)
        # 医院
        unit_id = client_config.get_user_config('unit_id')
        if unit_id is None or unit_id < 0:
            return
        self.unit_select()
        index = self.ui.unit_box.findData(unit_id)
        if index == -1:
            return
        self.ui.unit_box.setCurrentIndex(index)
        # 科室
        dept_id = client_config.get_user_config('dept_id')
        if dept_id is None or dept_id < 0:
            return
        self.dept_select()
        index = self.ui.dept_box.findData(dept_id)
        if index == -1:
            return
        self.ui.dept_box.setCurrentIndex(index)
        # 医生
        doctor_names = client_config.get_user_config('doctor_names')
        if doctor_names is None or len(doctor_names) < 0:
            return
        self.doctor_select()
        for doctor_name in doctor_names:
            self.ui.doctor_box.check_ok(doctor_name)


    def city_select(self):
        cities = client_config.get_cities()
        for index, city in enumerate(cities):
            self.ui.city_box.addItem(city.get('name'), userData=city.get('cityId'))

    def city_change_event(self):
        city_id = self.ui.city_box.currentData()
        city_name = self.ui.city_box.currentText()
        if not city_id:
            return
        client_config.save_user_config('city_id', city_id)
        client_config.save_user_config('city_name', city_name)
        self.ui.unit_box.clear()
        self.ui.dept_box.clear()
        self.ui.doctor_box.clear()

    def unit_select(self):
        city_id = client_config.get_user_config('city_id')
        if city_id is None or city_id == '':
            QMessageBox.warning(self, "标题", "请选择城市", QMessageBox.StandardButton.Ok)
            return
        units = client_util.get_all_unit_by_city(city_id)
        for unit in units:
            self.ui.unit_box.addItem(unit.get('unit_name'), userData=unit.get('unit_id'))

    def unit_change_event(self):
        unit_id = self.ui.unit_box.currentData()
        unit_name = self.ui.unit_box.currentText()
        if not unit_id:
            return
        client_config.save_user_config('unit_id', unit_id)
        client_config.save_user_config('unit_name', unit_name)
        self.ui.dept_box.clear()
        self.ui.doctor_box.clear()

    def dept_select(self):
        unit_id = client_config.get_user_config('unit_id')
        if unit_id is None or unit_id == '':
            QMessageBox.warning(self, "标题", "请先选择医院", QMessageBox.StandardButton.Ok)
            return
        depts = client_util.get_all_dept_by_unit(unit_id)
        for dept in depts:
            self.ui.dept_box.addItem(dept.get('dep_name'), userData=dept.get('dep_id'))


    def dept_change_event(self):
        dept_id = self.ui.dept_box.currentData()
        dept_name = self.ui.dept_box.currentText()
        if not dept_id:
            return
        client_config.save_user_config('dept_id', dept_id)
        client_config.save_user_config('dept_name', dept_name)
        self.ui.doctor_box.clear()
        pass

    def doctor_select(self):
        unit_id = client_config.get_user_config('unit_id')
        dept_id = client_config.get_user_config('dept_id')
        if dept_id is None or dept_id == '' or unit_id is None or unit_id == '':
            QMessageBox.warning(self, "标题", "请先选择医院-科室", QMessageBox.StandardButton.Ok)
            return
        sch_edp = client_util.get_sch_edp(unit_id, dept_id)
        for doctor in sch_edp.get('data').get('doc'):
            self.ui.doctor_box.addItem(doctor.get('doctor_name'), userData=doctor.get('doctor_id'))


    def doctor_change_event(self, datas):
        if not datas and len(datas) < 0:
            return
        client_config.save_user_config('doctor_ids', list(data[1] for data in datas))
        client_config.save_user_config('doctor_names', list(data[0].text() for data in datas))

    def member_select(self):
        members = client_util.get_member()
        if members is None or len(members) <= 0:
            QMessageBox.warning(self, "标题", "无就诊人，请到https://user.91160.com/member.html完善信息", QMessageBox.StandardButton.Ok)
            return
        for member in members:
            self.ui.dept_box.addItem(member.get('name'), userData=member.get('id'))


    def member_change_event(self):
        member_id = self.ui.member_box.currentData()
        member_name = self.ui.member_box.currentText()
        if not member_id:
            return
        client_config.save_user_config('member_id', member_id)
        client_config.save_user_config('member_name', member_name)

    def registration_days_select(self):
        now = datetime.now()
        for i in range(14):
            new_now = now + timedelta(days=i)
            date_str = new_now.strftime(data_format)
            self.ui.registration_days_combo_box.addItem(date_str, date_str)

    def registration_days_change_event(self, datas):
        if not datas and len(datas) < 0:
            return
        client_config.save_user_config('registration_days', list(data[1] for data in datas))

    def am_check_box_click(self, state):
        self.am_pm()

    def pm_check_box_click(self, state):
        self.am_pm()

    def am_pm(self):
        list = []
        if self.ui.am_check_box.isChecked():
            list.append('am')
        if self.ui.pm_check_box.isChecked():
            list.append('pm')
        if len(list) == 0:
            list.append('am')
            list.append('pm')
        client_config.save_user_config('registration_am_pm', list)

    def time_rate_spin_box_input(self):
        text = self.ui.time_rate_spin_box.value()
        client_config.save_user_config('time_rate', text)


    def fixed_time_click(self):
        flag = 0
        if self.ui.fixed_time_check_box.isChecked():
            flag = 1
        client_config.save_user_config('fixed_time', flag)


    def time_range_begin_select(self):
        self.time_range()


    def time_range_end_select(self):
        self.time_range()


    def time_range(self):
        begin_datetime = self.ui.time_range_begin_datetime.dateTime()
        end_datetime = self.ui.time_range_end_datetime.dateTime()
        list = [begin_datetime.toString(q_datetime_format), end_datetime.toString(q_datetime_format)]
        client_config.save_user_config('time_range', list)

    def task_button_click(self):
        if self.ui.task_button.text() == '自动挂号':
            if self.task_thread is None or not self.task_thread.is_alive():
                self.task_activity = True
                self.task_thread = threading.Thread(target=self.task)
                self.task_thread.daemon = True
                self.task_thread.start()
                self.ui.task_button.setText('挂号中')
        else:
            self.ui.task_button.setText('自动挂号')
            self.task_activity = False

    def task(self):
        while self.task_activity:
            if client_util.registration_task():
                user_log_util.getLogger().info('挂号成功')
                self.ui.task_button.setText('自动挂号')
                self.task_activity = False
                return


    def clear_log(self, event):
        self.ui.log_input.clear()

def main():
    main_app = QtWidgets.QApplication(sys.argv)
    window = Main_Form()
    window.show()
    sys.exit(main_app.exec())



