import logging
import datetime

class ErrorLogger:

    def __init__(self, log_file=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        
        if log_file is None:
            log_file = f"errors_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)

    def log(self, error, level='error'):
        if level == 'error':
            self.logger.error(error)
        elif level == 'warning':
            self.logger.warning(error)
        elif level == 'info':
            self.logger.info(error)
        elif level == 'debug':
            self.logger.debug(error)
        else:
            self.logger.error(f"Unknown log level: {level}. Original error: {error}")
