import os
import logging
import socket
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


logger = logging.getLogger()
logger.setLevel(logging.INFO)

f = ContextFilter()
logger.addFilter(f)

syslog = SysLogHandler(address=(os.environ.get("PAPERTRAIL_ADDRESS"), os.environ.get("PAPERTRAIL_PORT")))
formatter = logging.Formatter(
    '%(levelname)s %(asctime)s sg-start-pipeline: %(message)s', datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)
