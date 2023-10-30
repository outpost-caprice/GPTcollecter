
import logging
from enum import Enum
import datetime

class LogLevel(Enum):
  DEBUG = 10
  INFO = 20
  WARNING = 30
  ERROR = 40

class ErrorLogger:

  def __init__(self, log_file=None):
    # ログファイル名の自動設定
    if log_file is None:
      now = datetime.datetime.now()
      log_file = now.strftime("errors_%Y%m%d_%H%M%S.log")
    
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.INFO)

    # loggingモジュールのフォーマッタを使用 
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    self.logger.addHandler(file_handler)

  def log(self, message, level=LogLevel.INFO):
    # dictでlevelの条件分岐を置き換え
    level_map = {
      LogLevel.DEBUG: self.logger.debug,
      LogLevel.INFO: self.logger.info,
      LogLevel.WARNING: self.logger.warning,
      LogLevel.ERROR: self.logger.error
    }

    level_map[level](message)
