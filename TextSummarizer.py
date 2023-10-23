import openai
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

class ImprovedText:

    def __init__(self, *args, **kwargs):
        try:
            self.openai_api_key = os.environ.get('OPENAI_API_KEY', '')
            self.llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0, openai_api_key=self.openai_api_key)
        except Exception as e:
            print(f"初期化中に未知のエラーが発生しました: {e}")

    def split_text(self, text, chunk_size=3600, chunk_overlap=100):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            return splitter.split(text)
        except MemoryError:
            print("メモリエラー: テキストが大きすぎて処理できません。")
            return []
        except Exception as e:
            print(f"テキスト分割中に未知のエラーが発生しました: {e}")
            return []

    def summarize_text(self, text):
        try:
            text_chunks = self.split_text(text)
            chain = load_summarize_chain(self.llm, chain_type='map_reduce')
            summaries = chain.run(text_chunks)
            return " ".join(summaries)
        except TimeoutError:
            print("タイムアウトエラー: 要約処理がタイムアウトしました。")
            return ""
        except Exception as e:
            print(f"テキスト要約中に未知のエラーが発生しました: {e}")
            return ""
