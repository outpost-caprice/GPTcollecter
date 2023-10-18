import streamlit as st
from web_searcher import WebScraper 
from TextSummarizer import TextSummarizer
from FileManager import FileManager
from DuplicateDetector import DuplicateDetector
from ErrorLogger import ErrorLogger

st.set_page_config(page_title='Text Summarizer')

st.sidebar.header('検索クエリを入力')
query = st.sidebar.text_input('検索語句:')

progress_bar = st.progress(0) 

@st.cache
def run_search_and_summarize(query):

  scraper = WebScraper()
  summarizer = TextSummarizer()
  file_mgr = FileManager('summaries')
  dup_detector = DuplicateDetector()
  err_logger = ErrorLogger('errors.log')

  try:
    results = scraper.search(query)
    
    for url in results:
      content = scraper.get_content(url)
      summary = summarizer.summarize(content)

      file_mgr.save(summary, url)
      dup_detector.add(summary)

    if dup_detector.has_duplicates():
      st.error('Duplicate summaries found!')

    file_mgr.compress()
    
    progress_bar.progress(100)

  except Exception as e:
    err_logger.log(e)
    st.error('Error occurred during processing')

  finally:
    scraper.close()

if st.button('Summarize'):
  with st.spinner('Searching and summarizing...'):
    run_search_and_summarize(query)
  
  st.success('Summarization complete!')

  st.download_button(
    label='Download Summaries',
    data=file_mgr.get_zip_file(), 
    file_name='summaries.zip'
  )