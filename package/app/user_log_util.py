import logging

from utils import log_util

logger = log_util.LoggerFactory(level=logging.INFO).getLog()

def getLogger():
    return logger



