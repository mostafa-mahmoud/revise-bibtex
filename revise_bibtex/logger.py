import logging
import os


logging.PRINT = 200
logging.addLevelName(logging.PRINT, "PRINT")


class ColoredFormatter(logging.Formatter):
    # FORMAT = "[%(asctime)s][%(pathname)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s"
    FORMAT = "[%(asctime)s %(levelname)s]: %(message)s"
    DATE_FMT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, use_highlight=True):
        super().__init__(ColoredFormatter.FORMAT, datefmt=ColoredFormatter.DATE_FMT)
        self.use_highlight = use_highlight

    def format(self, record):
        record.pathname = os.path.relpath(record.pathname)
        if record.levelno == logging.PRINT:
            self._style._fmt = '%(message)s'
        if os.name == 'posix':  # coloring doesn't always work well for Windows
            if self.use_highlight and hasattr(record, 'highlight') and record.highlight != 0:
                start = '\033[%dm' % (record.highlight + 30)
                end = '\033[%dm' % 39
                return start + super().format(record) + end
        result = super().format(record)
        self._style._fmt = ColoredFormatter.FORMAT
        return result


class CustomLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        highlight = kwargs.get('highlight', 0)
        if not isinstance(highlight, int) and highlight not in range(0, 9):
            raise ValueError('highlight should be between 0 and 8')
        kwargs['extra'] = {'highlight': highlight}
        if 'highlight' in kwargs.keys():
            del kwargs['highlight']
        return msg, kwargs

    def addOutputHandler(self, filename):
        if filename is None:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(ColoredFormatter(use_highlight=True))
            return self.logger.addHandler(console_handler)
        else:
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(ColoredFormatter(use_highlight=False))
            return self.logger.addHandler(file_handler)

    def removeOutputHandler(self):
        return self.logger.removeHandler(self.logger.handlers[-1])

    def print(self, msg, *args, **kwargs):
        self.log(logging.PRINT, msg, *args, **kwargs)


logger = CustomLogger(logger=logging.getLogger(__name__), extra=None)
logger.addOutputHandler(None)
logger.addOutputHandler('debug.log')
logger.setLevel(logging.DEBUG)
