from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os

class WebSearcher:

  def __init__(self):
    self.api_key = os.environ.get('GOOGLE_API_KEY', '')  
    self.cse_id = os.environ.get('GOOGLE_CSE_ID', '')
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

  def search(self, query, num_results, start_index=1):
    try:
      service = build("customsearch", "v1", developerKey=self.api_key)
      result = service.list(q=query, cx=self.cse_id, 
              num=num_results, start=start_index).execute()
      return [item['link'] for item in result['items']]
    except Exception as e:
      print(f"An error occurred: {e}")
      return []

  def fetch_page(self, url):
    try:
      self.driver.get(url)
      element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
      WebDriverWait(self.driver, 10).until(element_present)  
      full_text = self.driver.find_element(By.TAG_NAME, 'body').text
      return full_text
    except Exception as e:
      print(f"An error occurred: {e}")
      return ""

  def __del__(self):
    self.driver.quit()