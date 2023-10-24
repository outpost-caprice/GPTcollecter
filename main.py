import asyncio
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
        results = scraper.search_api.search(query, num_results)
        loop = asyncio.get_event_loop()

        for url in results:
            content = scraper.fetch_page(url)
            summary = loop.run_until_complete(summarize_content(summarizer, content))
            full_texts.append(summary)

            file_mgr.save_summary(summary, url)
            dup_detector.add(summary)  

        if dup_detector.has_duplicates():
            file_mgr.make_zipfile("summaries.zip")

    except Exception as e:
        err_logger.log(f"An error occurred: {e}")

    return full_texts

if __name__ == "__main__":
    print(main("sample query", 10))