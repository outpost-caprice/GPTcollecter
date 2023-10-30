import asyncio
import time
from web_searcher import WebSearcher
from TextSummarizer import ImprovedText 
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger

async def summarize_content(summarizer, content):
  return await summarizer.summarize(content)

async def main(query, num_results):
  scraper = WebSearcher()
  if scraper.search_api is None:
    print("Google Search API is not initialized. Exiting.")
    return

  summarizer = ImprovedText()
  file_mgr = FileManager('summaries')
  dup_detector = DuplicateDetector()
  err_logger = ErrorLogger('main_errors.log')

  full_texts = []

  try:
    results = scraper.search_api.search(query, num_results=num_results)
    tasks = []

    for url in results:
      await asyncio.sleep(5)  # 非同期のsleep

      content = scraper.fetch_page(url)
      
      if len(content) < 500:
        err_logger.log(f"Content too short to summarize: {url}")
        continue

      task = asyncio.ensure_future(summarize_content(summarizer, content))
      tasks.append(task)

    summaries = await asyncio.gather(*tasks)

    for summary, url in zip(summaries, results):
      full_texts.append(summary)
      file_mgr.save_summary(summary, url)
      dup_detector.add(summary)

    if dup_detector.has_duplicates():
      file_mgr.make_zipfile("summaries.zip")
      
  except Exception as e:
    err_logger.log(f"An error occurred: {e}")

  return full_texts

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main("your_query_here", 10))
