# coding: utf-8
import os, sys

settings = {}

# Api URL
settings['apiURL'] = 'https://api.bitbankpay.jp/api/v1/'

# Api key you created at bitbankpay
settings['apiKey'] = 'API Key'

# BTC or JPY
settings['currency'] = 'BTC'

# costomer's url where after paying
settings['redirect_url'] = ''

# log Setting
settings['isLogging'] = True
settings['logLevel'] = 'ERROR'

logger = None
def get_logger():
    """
    Logger Factory
    """
    global logger
    if logger is None:
        if settings['isLogging']:
            logger = Logger(settings['logLevel'])
        else:
            logger = NullLogger(settings['logLevel'])
    return logger


class NullLogger(object):
    """
    This Logger do nothing.
    """
    def __init__(self, level):
        pass

    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

    def critical(self, msg):
        pass


class Logger(NullLogger):
    """
    Wrapper Class to change it to a favorite logger.
    """
    def __init__(self, level):
        import logging, logging.handlers

        script_dir_path = os.path.abspath(os.path.dirname(__file__))
        log_file_name = 'bitbankpay.log'
        log_file_path = os.path.join(script_dir_path, log_file_name)

        logger = logging.getLogger()

        formatter = logging.Formatter(
            '%(asctime)s\t%(module)s:%(funcName)s\t%(lineno)d\t%(levelname)s\t- %(message)s'
        )
        #Stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

        #Rotating file
        rotating_file_handler = logging.handlers.RotatingFileHandler(
            log_file_path, maxBytes=(5*1024*1024), backupCount=1000)
        rotating_file_handler.setFormatter(formatter)
        logger.addHandler(rotating_file_handler)

        logger.setLevel(getattr(logging ,level))

        self._logger = logger

    def debug(self, msg):
        self._logger.debug(msg)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)

    def critical(self, msg):
        self._logger.critical(msg)
