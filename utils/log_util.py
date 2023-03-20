import collections
import datetime
import logging


class LoggerFactory(logging.Logger):

    def __init__(self, name='.info.log', level=logging.DEBUG):
        super(LoggerFactory, self).__init__(name, level)
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def callback_msg(self, msg):
        if self.callback:
            self.callback(msg=msg)

    def error(self, msg, *args, **kwargs) -> None:
        super(LoggerFactory, self).error(msg, *args, **kwargs)
        self.callback_msg(self.getMessage(msg, *args))

    def debug(self, msg, *args, **kwargs):
        super(LoggerFactory, self).debug(msg, *args, **kwargs)
        self.callback_msg(self.getMessage(msg, *args))

    def info(self, msg, *args, **kwargs):
        super(LoggerFactory, self).info(msg, *args, **kwargs)
        self.callback_msg(self.getMessage(msg, *args))


    def warning(self, msg, *args, **kwargs):
        super(LoggerFactory, self).warning(msg, *args, **kwargs)
        self.callback_msg(self.getMessage(msg, *args))

    def getLog(self):
        self.addHandler(self.consoleHandler())
        return self

    def getFileLog(self, file='info.log'):
        self.addHandler(self.fileHandler(file))
        return self

    def getTimedRotatingFileLog(self, file='info.log'):
        self.addHandler(self.timedRotatingFileHandler(file))
        return self

    def consoleHandler(self):
        # 第一种方式输入到控制台
        heard = logging.StreamHandler()
        heard.setFormatter(logging.Formatter(
            fmt="%(asctime)s -[%(filename)s] -[%(levelname)s] -%(lineno)d -%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        return heard

    def fileHandler(self, file):
        heard = logging.FileHandler(file)
        fromatter = logging.Formatter(
            fmt="%(asctime)s -[%(filename)s] -[%(levelname)s] -%(lineno)d -%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        heard.setFormatter(fromatter)
        return heard

    def timedRotatingFileHandler(self, file):
        heard = logging.handlers.TimedRotatingFileHandler(file,
                                                          when='midnight',
                                                          interval=1,
                                                          backupCount=7,
                                                          atTime=datetime.time(0, 0, 0, 0)
                                                          )
        fromatter = logging.Formatter(
            fmt="%(asctime)s -[%(filename)s] -[%(levelname)s] -%(lineno)d -%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        heard.setFormatter(fromatter)
        return heard


    def getMessage(self, msg, *args):
        if (args and len(args) == 1 and isinstance(args[0], collections.abc.Mapping)
                and args[0]):
            args = args[0]
        now = datetime.datetime.now()
        str_time = now.strftime("%Y-%m-%d %H:%M:%S - ")
        msg = str_time + str(msg)
        if args:
            msg = msg % args
        return msg