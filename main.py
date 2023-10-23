import asyncio
from web_searcher import WebSearcher
from ImprovedText import ImprovedText
from FileManager import FileManager
from difference import DuplicateDetector  # 重複検出クラスをインポート
from error_log import ErrorLogger

async def summarize_content(summarizer, content):
    return summarizer.summarize_text(content)

def main(query, num_results):
    scraper = WebSearcher()
    summarizer = ImprovedText()
    file_mgr = FileManager('summaries')
    dup_detector = DuplicateDetector()  # 重複検出インスタンスを作成
    err_logger = ErrorLogger('main_errors.log')
    full_texts = []

    try:
        results = scraper.search(query, num_results)
        loop = asyncio.get_event_loop()

        for url in results:
            content = scraper.fetch_page(url)
            summary = loop.run_until_complete(summarize_content(summarizer, content))
            full_texts.append(summary)

            file_mgr.save_summary(summary, url)
            dup_detector.add(summary)  # 重複検出に要約を追加

        if dup_detector.has_duplicates():  # 重複があるかチェック
            # ここで重複処理を行います。
            # 重複がある場合、DuplicateDetectorクラスが内部で処理を行います。

        file_mgr.make_zipfile("summaries.zip")

    except Exception as e:
        err_logger.log(f"An error occurred: {e}")

    finally:
        scraper.__del__()

    return full_texts

if __name__ == "__main__":
    print(main("sample query", 10))
