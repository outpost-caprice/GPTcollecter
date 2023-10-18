from web_searcher import WebSearchAndScraping
from TextSummarizer import TextSummarization
from FileManager import FileManagement
from DuplicateDetector import DuplicateContentManagement
from ErrorLogger import ErrorHandling

error_log = ErrorHandling('main_errors.log') 

def main():
    #全クラス初期化
    web_search = WebSearchAndScraping()
    text_summ = TextSummarization()
    file_mng = FileManagement()
    dup_mng = DuplicateContentManagement()
    err_mng = ErrorHandling()
    
    # Your logic here to control all the modules and handle errors
    try:
        # Web search and information collection
        urls = web_search.get_search_results("Your Query")
        
        for url in urls:
            # Fetch and summarize text from each URL
            raw_text = web_search.fetch_page_content(url)
            summary = text_summ.summarize_text(raw_text)
            
            # Save the summary to a file
            file_mng.save_to_file(summary, url)
            
            # Add summary for duplicate checking
            dup_mng.add_summary(summary)
            
    except Exception as e:
        err_mng.log_error("Main Function", str(e))
    
    # Find similar summaries and handle them
    similar_pairs = dup_mng.find_similar()
    # ここに80パーセント以上の重複時の処理を追加しておくこと
    
    # Create a zip file for all the saved summaries
    file_mng.create_zip_file()


if __name__ == "__main__":
    main()
