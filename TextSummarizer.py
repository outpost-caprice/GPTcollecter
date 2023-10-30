import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import Summarize
import os

class ImprovedText:
    
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.model = 'gpt-3.5-turbo'
        
    async def summarize(self, text):
        try:
            chunks = self.split_text(text)
            chain = Summarize(llm=self.model, openai_api_key=self.openai_key)  
            summary = await chain.run(chunks)
            return summary
        except Exception as e:
            print(f"Error: {e}")
            return ""
            
    def split_text(self, text):
        splitter = RecursiveCharacterTextSplitter(3600, 100)
        return splitter.split(text)