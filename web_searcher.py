from langchain.utilities import GoogleSearchAPIWrapper, LoadDocumentFromURL 
from langchain.chat_models import ChatOpenAI
import os

class WebSearcher:

    def __init__(self):
        # 環境変数からAPIキーを取得
        self.api_key = os.getenv('GOOGLE_API_KEY')  
        self.cse_id = os.getenv('GOOGLE_CSE_ID')
        self.openai_key = os.getenv('OPENAI_API_KEY')

        # APIの初期化
        self.search_api = GoogleSearchAPIWrapper(self.api_key, self.cse_id)
        self.url_loader = LoadDocumentFromURL()
        self.chat_api = ChatOpenAI(self.openai_key)

    def search(self, query, num):
        try:
            results = self.search_api.search(query, num)
            return [r['link'] for r in results]
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    # ドキュメントローダーを使用 
    def fetch_page(self, url):
        try:
            text = self.url_loader.load(url)
            return text
        except Exception as e:
            print(f"Error: {e}")
            return ""
