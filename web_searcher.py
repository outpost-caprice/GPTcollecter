from langchain.utilities.google_search import GoogleSearchAPIWrapper
import langchain
import requests
import os
from langchain.document_loaders import UnstructuredURLLoader

API_KEY = os.environ.get('GOOGLE_API_KEY', '')
CSE_ID  = os.environ.get('GOOGLE_CSE_ID', '')
class WebSearcher:
    def __init__(self):
        try:
            self.api_key = API_KEY
            self.cse_id = CSE_ID
            self.url_loader = UnstructuredURLLoader()
            self.search_api = GoogleSearchAPIWrapper(api_key=self.api_key, cse_id=self.cse_id)
        except Exception as e:
            print(f"初期化中に未知のエラーが発生しました: {e}")

    def search(self, query, num_results, start_index=1):
        try:
            results = self.search_api.search(query, num_results=num_results, start_index=start_index)
            return [item['link'] for item in results]
        except ConnectionError:
            print("接続エラー: Google Search APIに接続できませんでした。")
            return []
        except TimeoutError:
            print("タイムアウトエラー: Google Search APIへのリクエストがタイムアウトしました。")
            return []
        except Exception as e:
            print(f"検索中に未知のエラーが発生しました: {e}")
            return []

    def fetch_page(self, url):
        try:
            full_text = self.url_loader.load(url)
            return full_text
        except Exception as e:
            print(f"ページ取得中に未知のエラーが発生しました: {e}")
            return ""