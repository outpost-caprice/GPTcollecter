import difflib
import hashlib

class DuplicateDetector:

  def __init__(self, logger, log_file="duplicate_detector_errors.log"):
    self.summaries = []
    self.hashes = set()
    self.logger = logger  # ErrorLoggerのインスタンスを受け取る

  def add(self, text, url):
    try:
      text_hash = hashlib.sha256((text + url).encode('utf-8')).hexdigest()
      if text_hash not in self.hashes:
        self.summaries.append((text, url))
        self.hashes.add(text_hash)
      else:
        self.logger.log(f"重複テキスト検出: {text[:30]}...")
    except Exception as e:
      self.logger.log(f"テキスト追加中にエラー発生: {e}")

  def has_duplicates(self):
    return len(self.summaries) != len(self.hashes)