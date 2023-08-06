import logging
import sys

from prvsnlib.utils.colors import Colors


# https://docs.python.org/3/library/logging.html#logging-levels

class LoggingLevels:
    HEADER = 25
    SUCCESS = 26


def header(message, *args, **kwargs):
    logging.log(LoggingLevels.HEADER, message, *args, **kwargs)

logging.header = header
logging.addLevelName(LoggingLevels.HEADER, 'Header')

def success(message, *args, **kwargs):
    logging.log(LoggingLevels.SUCCESS, message, *args, **kwargs)

logging.success = success
logging.addLevelName(LoggingLevels.SUCCESS, 'Success')


class Formatter(logging.Formatter):

    def format(self, record):
        res = super(Formatter, self).format(record)

        if record.levelno == logging.NOTSET:
            pass
        elif record.levelno == logging.DEBUG:
            pass
        elif record.levelno == logging.INFO:
            pass
        elif record.levelno == LoggingLevels.HEADER:
            res = Colors.HEADER + '# ' + res + Colors.END
        elif record.levelno == LoggingLevels.SUCCESS:
            res = Colors.OK + res + Colors.END
        elif record.levelno == logging.WARNING:
            res = Colors.WARNING + res + Colors.END
        elif record.levelno == logging.ERROR:
            res = Colors.ERROR + res + Colors.END
        elif record.levelno == logging.CRITICAL:
            res = Colors.ERROR + res + Colors.END
        return res

formatter = Formatter()
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(formatter)
logging.root.addHandler(hdlr)
