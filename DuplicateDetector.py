import difflib

class DuplicateDetector:

  def __init__(self):
    self.summaries = []

  def add(self, text):
    self.summaries.append(text)

  def has_duplicates(self, threshold=0.8):
    for i, summary1 in enumerate(self.summaries):
      for j, summary2 in enumerate(self.summaries):
        if i == j:
          continue
            
        # 差分チェック
        ratio = difflib.SequenceMatcher(None, summary1, summary2).ratio()

        if ratio >= threshold:
          print(f"Found duplicate: {summary1} and {summary2}")
          return True

    return False