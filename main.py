import asyncio
from web_searcher import WebSearcher
from ImprovedText import ImprovedText
from FileManager import FileManager
from difference import DuplicateDetector
from error_log import ErrorLogger

async def summarize_content(summarizer, content):
    return summarizer.summarize_text(content)

def main(query, num_results):
    scraper = WebSearcher()
    summarizer = ImprovedText()
    file_mgr = FileManager('summaries')
    dup_detector = DuplicateDetector()
    err_logger = ErrorLogger('main_errors.log')

    try:
        results = scraper.search(query, num_results)
        loop = asyncio.get_event_loop()

        for url in results:
            print("Fetching content...")  # フロントエンドに表示するメッセージ
            content = scraper.fetch_page(url)

            print("Summarizing content...")  # フロントエンドに表示するメッセージ
            summary = loop.run_until_complete(summarize_content(summarizer, content))

            print("Saving summary...")  # フロントエンドに表示するメッセージ
            file_mgr.save_summary(summary, url)
            dup_detector.add(summary)

        print("Checking for duplicates...")  # フロントエンドに表示するメッセージ
        if dup_detector.has_duplicates():
            # 重複処理（省略）

        print("Compressing files...")  # フロントエンドに表示するメッセージ
        file_mgr.make_zipfile("summaries.zip")

    except Exception as e:
        err_logger.log(f"An error occurred: {e}")

    finally:
        scraper.__del__()

if __name__ == "__main__":
    main("sample query", 10)
