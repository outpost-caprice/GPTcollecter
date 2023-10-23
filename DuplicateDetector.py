import difflib
from error_log import ErrorLogger

class DuplicateDetector:

    def __init__(self, log_file="duplicate_detector_errors.log"):
        self.summaries = []
        self.logger = ErrorLogger(log_file)

    def add(self, text):
        try:
            self.summaries.append(text)
        except Exception as e:
            self.logger.log(f"テキストの追加中にエラーが発生しました: {e}")

    def has_duplicates(self, threshold=0.8):
        try:
            for i, summary1 in enumerate, 1, summary1 in enumerate(self.summaries):
                for j, summary2 in enumerate(self.summaries):
                    if i == j:
                        continue

                    # 差分チェック
                    sm = difflib.SequenceMatcher(None, summary1, summary2)
                    ratio = sm.ratio()

                    if ratio >= threshold:
                        self.logger.log(f"重複が見つかりました: {summary1} と {summary2}", level='info')
                        
                        # 一致しない部分を取得
                        diff = [diff_elem for diff_elem in sm.get_opcodes() if diff_elem[0] != 'equal']
                        
                        # 一致しない部分を先に出力されたテキストに追加
                        for tag, i1, i2, j1, j2 in diff:
                            if tag == 'replace':
                                self.summaries[i] += summary2[j1:j2]
                            elif tag == 'insert':
                                self.summaries[i] += summary2[j1:j2]
                        
                        return True

            return False
        except Exception as e:
            self.logger.log(f"重複の検出中にエラーが発生しました: {e}")
            return False
