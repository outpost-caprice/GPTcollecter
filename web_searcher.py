from langchain.utilities import GoogleSearchAPIWrapper, LoadDocumentFromURL
from langchain.chat_models import ChatOpenAI  
import os
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
import asyncio

class WebSearcher:

  def __init__(self, logger):
    self.api_key = os.getenv('GOOGLE_API_KEY')    
    self.cse_id = os.getenv('GOOGLE_CSE_ID')
    self.openai_key = os.getenv('OPENAI_API_KEY')
    self.logger = logger  # ErrorLoggerのインスタンスを受け取る
    self.search_api = GoogleSearchAPIWrapper(self.api_key, self.cse_id)
    self.url_loader = LoadDocumentFromURL()
    self.chat_api = ChatOpenAI(self.openai_key)
    self.async_chromium_loader = AsyncChromiumLoader()
    self.html2text_transformer = Html2TextTransformer()

  def search(self, query, num):
    try:
      results = self.search_api.search(query, num)
      return [r['link'] for r in results]
    except Exception as e:
      print(f"Error: {e}")
      return []

#非同期Chromiumローダーを使用してページをフェッチ
  async def fetch_page_with_async_chromium_loader(self, urls):
    try:
      docs = await self.async_chromium_loader.load(urls)
      return docs
    except Exception as e:
      print(f"Error: {e}")
      return []

#Html2Textトランスフォーマーを使用してHTMLをテキストに変換
  def transform_html_to_text(self, docs):
    try:
      transformed_docs = self.html2text_transformer.transform_documents(docs)
      return transformed_docs
    except Exception as e:
      print(f"Error: {e}")
      return []
