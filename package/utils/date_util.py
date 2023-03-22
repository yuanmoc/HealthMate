import time


def get_date_str():
    """
    获取当前天数
    :return:  当天字符串
    """
    return time.strftime("%Y-%m-%d", time.localtime())
