from langchain.utilities.google_search import GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI
import os

class WebSearcher:
    def __init__(self):
        try:
            self.api_key = os.getenv('GOOGLE_API_KEY')
            self.cse_id = os.getenv('GOOGLE_CSE_ID')
            self.search_api = GoogleSearchAPIWrapper(google_api_key=self.api_key, cse_id=self.cse_id)
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            self.llm = ChatOpenAI(openai_api_key=self.openai_api_key, model_name='gpt-3.5-turbo-16k', temperature=0)
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