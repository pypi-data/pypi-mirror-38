import logging
import sys

from prvsnlib.utils.colors import Colors


class StdoutLogger:

    def __enter__(self):

        class Redirection:

            def write(self, message):
                logging.info(message.strip())

            def flush(self):
                pass

        self._stdout = sys.stdout
        sys.stdout = Redirection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._stdout


class LoggingLevels:
    HEADER = 25
    SUCCESS = 26


logging.header = lambda message, *args, **kwargs: logging.log(LoggingLevels.HEADER, message, *args, **kwargs)
logging.addLevelName(LoggingLevels.HEADER, 'Header')

logging.success = lambda message, *args, **kwargs: logging.log(LoggingLevels.SUCCESS, message, *args, **kwargs)
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
            res = Colors.HEADER + '### ' + res + Colors.END
        elif record.levelno == LoggingLevels.SUCCESS:
            res = Colors.OK + res + Colors.END
        elif record.levelno == logging.WARNING:
            res = Colors.WARNING + '/!\\ ' + res + Colors.END
        elif record.levelno == logging.ERROR:
            res = Colors.ERROR + res + Colors.END
        elif record.levelno == logging.CRITICAL:
            res = Colors.ERROR + res + Colors.END
        return res


formatter = Formatter()
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logging.root.addHandler(stream_handler)
