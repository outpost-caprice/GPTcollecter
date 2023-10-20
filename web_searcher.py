from googleapiclient.discovery import build
from selenium import webdriver
import os

class WebSearcher:
  def __init__(self):
    self.api_key = os.environ['GOOGLE_API_KEY']
    self.cse_id = os.environ['GOOGLE_CSE_ID']
    
    # ChromeDriverの場所を指定
    driver_path = os.environ["DRIVER_PATH"]
    # FirefoxからChromeに変更
    self.driver = webdriver.Chrome(executable_path=driver_path)

  def search(self, query, num_results=10):
    service = build("customsearch", "v1", developerKey=self.api_key)
    result = service.cse().list(q=query, cx=self.cse_id, num=num_results).execute()
    return [item['link'] for item in result['items']]

  def fetch_page(self, url):
    self.driver.get(url)
    return self.driver.page_source
