import asyncio
from web_searcher import WebSearcher
from TextSummarizer import ImprovedText
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger

async def fetch_and_summarize(url, summarizer):
    content = await get_content(url)
    summary = await summarizer.summarize(content)
    return summary

async def get_content(url):
    searcher = WebSearcher()
    return searcher.fetch_page(url)

async def main(query, num_results):
    
    logger = ErrorLogger('main.log')
    
    try:
        searcher = WebSearcher()
        summarizer = ImprovedText()
        file_mgr = FileManager('summaries')
        dup_detector = DuplicateDetector()
        
        tasks = []
        results = searcher.search(query, num_results)
        
        for url in results:
            task = asyncio.create_task(fetch_and_summarize(url, summarizer))
            tasks.append(task)
    
        summaries = await asyncio.gather(*tasks)
            
        for summary in summaries:
            file_mgr.save_summary(summary, url) 
            dup_detector.add(summary)
    
        if dup_detector.has_duplicates():
            file_mgr.make_zipfile('summaries.zip')
            
    except Exception as e:
        logger.log(f'Error: {e}', 'error')
        
    return summaries
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("query", 10))