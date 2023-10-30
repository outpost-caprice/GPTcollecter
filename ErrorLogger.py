from enum import Enum
import logging
import datetime

class LogLevel(Enum):
  DEBUG = 10
  INFO = 20 
  WARNING = 30
  ERROR = 40

class ErrorLogger:

  def __init__(self, log_file=None):

    if log_file is None:
      now = datetime.datetime.now()
      log_file = now.strftime("errors_%Y%m%d_%H%M%S.log")

    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    self.logger.addHandler(file_handler)

  def log(self, message, level=LogLevel.ERROR):

    if level == LogLevel.DEBUG:
      self.logger.debug(message)

    elif level == LogLevel.INFO:
      self.logger.info(message)

    elif level == LogLevel.WARNING:
      self.logger.warning(message)

    elif level == LogLevel.ERROR:
      self.logger.error(message)

    else:
      self.logger.error(f"Unknown log level: {level}")