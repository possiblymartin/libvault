import os
from dotenv import load_dotenv
import json
import time
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_and_sort(text, user_categories):
  categories_str = ','.join(user_categories)
  prompt = (
    "You are an assistant whose job is to summarize articles and determine the best category for the article from a given list of user-generated categories.\n\n"
    "Instructions:\n"
    "1. Summarize the article in exactly 3 concise bullet points.\n"
    "2. Given the user-generated categories: " + categories_str + ", assess whether the article "
    "fits into one of those categories. If it does, select that category; otherwise, suggest a new category name.\n\n"
    "Return your answer in JSON format with two keys: 'summary' (an array of bullet points) and 'category' (a string).\n\n"
    "Article Text:\n" + text
  )

  try:
    time.sleep(10)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
      {
       "role": "system", 
       "content": "You are an assistant that summarizes articles and categorizes them based on user provided categories."
      },
      {
       "role": "user", 
       "content": prompt
      }
    ],
    temperature=0.7,
    max_tokens=200)
    answer_str = response.choices[0].message.content
    result = json.loads(answer_str)
  except Exception as e:
    result = {
      "error": f"OpenAI processing failed: {str(e)}",
      "raw": answer_str if 'answer_str' in locals() else None
    }

  return result