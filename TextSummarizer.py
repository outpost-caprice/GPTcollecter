from ErrorLogger import ErrorLogger, LogLevel
logger = ErrorLogger("text_summarizer_errors.log")
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import Summarize
import os


class TextSummarizer:
    
  def __init__(self):
    self.openai_key = os.getenv('OPENAI_API_KEY')
    self.model = 'gpt-3.5-turbo'

    if not self.openai_key:
      raise ValueError("OPENAI_API_KEYが設定されていません")

  async def summarize(self, text):
    try:
      chunks = self.split_text(text)
      chain = Summarize(llm=self.model, openai_api_key=self.openai_key)
      summary = await chain.run(chunks)
      return summary

    except openai.OpenAIError as e:
      raise RuntimeError(f"OpenAI APIエラー: {e}") from e

    except Exception as e:
      raise RuntimeError(f"要約エラー: {e}") from e
      
  def split_text(self, text):
    splitter = RecursiveCharacterTextSplitter(3600, 100)
    return splitter.split(text)