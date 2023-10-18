import openai
import os
class ImprovedText:
    def __init__(self, *args, **kwargs):
        pass

def split_text(self, text, chunk_size=4000):

  chunks = []
  index = 0

  while index < len(text):
    end = min(index + chunk_size, len(text))
    chunk = text[index:end]
    chunks.append(chunk)
    index += chunk_size

  return chunks


def combine_summaries(self, summaries):
  
  combined = ""

  for summary in summaries: 
    combined += summary + "\n\n"

  return combined

def openai_api_summarize(self, text):
        messages = [
            {"role": "system", "content": "あなたは優秀な要約アシスタントです。提供された文章を、できる限り多くの情報を保ちつつ要約してください。"},
            {"role": "user", "content": text}
        ]

        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            completion = openai.ChatCompletion.create(
              model="gpt-3.5-turbo-16k",
              messages=messages,
              max_tokens=10000
            )
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            return text[:50]

        return completion.choices[0].message['content']

def summarize_text(self, text):
        text_chunks = self.split_text(text)
        summaries = [self.openai_api_summarize(chunk) for chunk in text_chunks]
        return " ".join(summaries)