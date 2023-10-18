from web_searcher import WebSearcher
from TextSummarizer import ImprovedText
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger

error_log = ErrorLogger('main_errors.log') 

def main():

  scraper = WebSearcher()
  summarizer = ImprovedText()
  file_mgr = FileManager('summaries') 
  dup_detector = DuplicateDetector()
  err_logger = ErrorLogger('errors.log')

  try:
    results = scraper.search('query')
    
    for url in results:
      content = scraper.get_content(url)
      summary = summarizer.summarize(content) 

      file_mgr.save(summary, url)
      dup_detector.add(summary)

    if dup_detector.has_duplicates():
      # handle duplicates  

        file_mgr.compress()

  except Exception as e:
    err_logger.log(e)

  finally:
    scraper.close()