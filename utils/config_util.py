import configparser
import threading
import time

class Config(object):
    """
    读取config.ini配置文件
    """

    def __init__(self, config_file):
        self.config_file_path = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file, encoding="utf-8")
        # 创建保存线程
        self.change = False
        self.save_thread = threading.Thread(target=self.auto_save_config_to_file)
        self.save_thread.daemon = True
        self.save_thread.start()

    def auto_save_config_to_file(self):
        while True:
            self.save_config_to_file()
            time.sleep(20)


    def save_config_to_file(self):
        if self.change:
            self.config.write(open(self.config_file_path, "w"))
            self.change = False

    def get(self, section, option):
        if self.config.has_option(section, option):
            return self.config.get(section, option)
        return None

    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        if value is None:
            value = ''
        if isinstance(value, list):
            value = ','.join(str(v) for v in value)
        elif not isinstance(value, str):
            value = str(value)
        self.config.set(section, option, value)
        self.change = True

    def getConfigToDict(self, section, conf: dict):
        for key in conf:
            if not self.config.has_option(section, key):
                continue
            value = conf.get(key)
            config_value = self.config.get(section, key)
            if config_value == '' or config_value is None:
                conf[key] = config_value
            elif isinstance(value, int):
                conf[key] = int(config_value)
            elif isinstance(value, float):
                conf[key] = float(config_value)
            elif isinstance(value, bool):
                conf[key] = True if config_value == 'true' or config_value == 'True' else False
            elif isinstance(value, list):
                conf[key] = config_value.split(',')
            else:
                conf[key] = config_value
        return conf
