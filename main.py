# main.py

import asyncio
import time
from web_searcher import WebSearcher
from TextSummarizer import ImprovedText 
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger

async def summarize_content(summarizer, content):
  return await summarizer.summarize(content)

def main(query, num_results):

  scraper = WebSearcher()
  summarizer = ImprovedText()
  file_mgr = FileManager('summaries')
  dup_detector = DuplicateDetector()
  err_logger = ErrorLogger('main_errors.log')

  full_texts = []

  try:
    results = scraper.search_api.search(query, num_results=num_results)

    loop = asyncio.get_event_loop()
    for url in results:
      # 検索リクエストの間に5秒待機
      time.sleep(5) 

      content = scraper.fetch_page(url)
      
      # 要約結果の品質チェック
      if len(content) < 500:
        err_logger.log(f"Content too short to summarize: {url}")
        continue
            
      summary = loop.run_until_complete(summarize_content(summarizer, content))
      
      full_texts.append(summary)
      file_mgr.save_summary(summary, url)
      dup_detector.add(summary)

    if dup_detector.has_duplicates():
      file_mgr.make_zipfile("summaries.zip")
      
  except Exception as e:
    err_logger.log(f"An error occurred: {e}")
    
  return full_texts