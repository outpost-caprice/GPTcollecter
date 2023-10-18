import logging

class ErrorLogger:

  def __init__(self, log_file):
    self.logger = logging.getLogger(__name__)
    handler = logging.FileHandler(log_file)
    self.logger.addHandler(handler)

  def log(self, error):
    self.logger.error(error)