import logging
import datetime

class ErrorLogger:

    def __init__(self, log_file=None):
        
        # ログファイル名の自動生成
        if log_file is None:
            now = datetime.datetime.now()
            log_file = now.strftime("errors_%Y%m%d_%H%M%S.log")
            
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # ログのフォーマット指定
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

        # ログハンドラの設定
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, message, level='error'):
        
        # レベルに応じたログ出力
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        else:
            # 不明なログレベルの場合はエラーレベルで出力
            self.logger.error(f"Unknown log level: {level}")