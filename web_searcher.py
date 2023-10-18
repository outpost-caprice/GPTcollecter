from googleapiclient.discovery import build
from selenium import webdriver

class WebSearcher:

  def __init__(self, api_key, cse_id):
    self.api_key = api_key
    self.cse_id = cse_id
    self.driver = webdriver.Firefox()

  def search(self, query, num_results=10):
    service = build("customsearch", "v1", developerKey=self.api_key)  
    result = service.cse().list(q=query, cx=self.cse_id, num=num_results).execute()
    return [item['link'] for item in result['items']]

  def fetch_page(self, url):
    self.driver.get(url)
    return self.driver.page_source
