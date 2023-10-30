import asyncio
from asyncio import Semaphore  
import TextSummarizer 
from web_searcher import WebSearcher
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger, LogLevel

async def fetch_and_summarize(url, sem):
  async with sem:
    content = await get_content(url)
    summary = await TextSummarizer.summarize(content) 
    return url, summary

async def get_content(url):
  searcher = WebSearcher()
  return searcher.fetch_page(url)

async def main(query, num_results):

  logger = ErrorLogger('main.log')

  summarizer = TextSummarizer.ImprovedText()

  sem = Semaphore(10)

  try:
    searcher = WebSearcher()
    file_mgr = FileManager('summaries')
    dup_detector = DuplicateDetector()

    tasks = []
    results = searcher.search(query, num_results)

    for url in results:
      task = asyncio.create_task(fetch_and_summarize(url, sem))
      tasks.append(task)

    try:
      summaries = await asyncio.gather(*tasks, timeout=3600)
    except asyncio.TimeoutError:
      pending = asyncio.all_tasks() - {asyncio.current_task()}
      for task in pending:
        task.cancel()
      print("Processing timed out")
    finally:
      for task in pending:
        try:
          await task 
        except asyncio.CancelledError:
          pass
    
    for url, summary in summaries:
      filename = create_filename(url)
      file_mgr.save_summary(summary, filename) 
      dup_detector.add(summary, url)

    file_mgr.make_zipfile('summaries.zip')

  except Exception as e:
    logger.log(f"Error: {e}", LogLevel.ERROR)

  return summaries

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main("query", 10))
