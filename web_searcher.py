from googleapiclient.discovery import build
from selenium import webdriver

class ImprovedResearchAgent:
    def __init__(self, google_api_key, google_cse_id):
        self.google_api_key = google_api_key
        self.google_cse_id = google_cse_id
        self.driver = webdriver.Firefox(executable_path="Path to Firefox Driver")

    def get_search_results(self, query, num_results=10):
        service = build("customsearch", "v1", developerKey=self.google_api_key)
        result = service.cse().list(q=query, cx=self.google_cse_id, num=num_results).execute()
        return [item['link'] for item in result['items']]
