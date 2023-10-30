from ErrorLogger import ErrorLogger, LogLevel
logger = ErrorLogger("main_errors.log")
import asyncio
from asyncio import Semaphore
import TextSummarizer
from web_searcher import WebSearcher
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import LogLevel
import ErrorLogger


async def fetch_and_summarize(url, sem):
  try:
    
    async with sem:
      content = await get_content(url)
      summary = await TextSummarizer.summarize(content)
      return url, summary
      
  except Exception as e:
    logger.log(f"Error while fetching and summarizing: {e}", LogLevel.ERROR)
    return url, None
    

async def get_content(url):
  searcher = WebSearcher()
  return searcher.fetch_page(url)

async def main(query, num_results):

  logger = ErrorLogger.ErrorLogger()

  summarizer = TextSummarizer.TextSummarizer(logger)

  sem = Semaphore(10)

  try:
    searcher = WebSearcher.WebSearcher()
    file_mgr = FileManager.FileManager('summaries')
    dup_detector = DuplicateDetector.DuplicateDetector()

    tasks = []
    results = searcher.search(query, num_results)

    for url in results:
      task = asyncio.create_task(fetch_and_summarize(url, sem))
      tasks.append(task)

    summaries = await asyncio.gather(*tasks)
  
  except Exception as e:
    logger.log(f"Error: {e}", LogLevel.ERROR)

  return summaries

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main("query", 10))