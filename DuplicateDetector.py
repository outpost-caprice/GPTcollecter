import difflib
import hashlib
from ErrorLogger import ErrorLogger

class DuplicateDetector:

    def __init__(self, log_file="duplicate_detector_errors.log"):
        self.summaries = []
        self.hashes = set()
        self.logger = ErrorLogger(log_file)

    def add(self, text):
        try:
            text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            if text_hash not in self.hashes:
                self.summaries.append(text)
                self.hashes.add(text_hash)
            else:
                self.logger.log(f"重複テキスト検出: {text[:30]}...")
        except Exception as e:
            self.logger.log(f"テキスト追加中にエラー発生: {e}")

    def has_duplicates(self):
        return len(self.summaries) != len(self.hashes)