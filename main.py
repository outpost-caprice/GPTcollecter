import asyncio
from asyncio import Semaphore
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger, LogLevel
from web_searcher import WebSearcher  # WebSearcherをインポート
from TextSummarizer import TextSummarizer  # TextSummarizerをインポート

async def fetch_and_summarize(url, sem, summarizer, logger):  # loggerを引数に追加
    try:
        async with sem:
            content = await get_content(url, logger)  # loggerを引数に追加
            summary = await summarizer.summarize(content)
            return url, summary
    except Exception as e:
        logger.log(f"Error while fetching and summarizing: {e}", LogLevel.ERROR)
        return url, None

async def get_content(url, logger):  # loggerを引数に追加
    searcher = WebSearcher(logger)  # loggerを渡す
    return await searcher.fetch_page_with_async_chromium_loader([url])  # 非同期メソッドを呼び出す


async def get_content(url):
    searcher = WebSearcher(logger)  # loggerを渡す
    return await searcher.fetch_page_with_async_chromium_loader([url])  # 非同期メソッドを呼び出す

async def main(query, num_results):
    logger = ErrorLogger(log_file="main_errors.log", log_level=LogLevel.INFO)
    searcher = WebSearcher(logger)
    summarizer = TextSummarizer(logger)
    file_mgr = FileManager(logger, 'summaries')
    dup_detector = DuplicateDetector(logger)
    sem = Semaphore(10)

    tasks = []
    try:
        results = searcher.search(query, num_results)
        for url in results:
            task = asyncio.create_task(fetch_and_summarize(url, sem, summarizer))
            tasks.append(task)
        summaries = await asyncio.gather(*tasks)
    except Exception as e:
        logger.log(f"Error: {e}", LogLevel.ERROR)
        return []

    return summaries

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("query", 10))
