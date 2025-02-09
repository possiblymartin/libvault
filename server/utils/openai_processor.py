import os
from dotenv import load_dotenv
import json
import difflib
import time
from openai import OpenAI
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def normalize_category(category):
  words = category.strip().split()
  if len(words) > 1:
    return words[0]
  return category.strip()


def assign_category(predicted_category, user_categories, threshold=0.7):
  normalized_pred = predicted_category.lower().strip()
  normalized_user = [cat.lower().strip() for cat in user_categories]
  matches = difflib.get_close_matches(normalized_pred, normalized_user, n=1, cutoff=threshold)
  if matches:
    for cat in user_categories:
      if cat.lower().strip() == matches[0]:
        return cat, False
  
  new_cat = normalize_category(predicted_category)
  return new_cat, True

def summarize_and_sort(text, user_categories):
  categories_str = ','.join(user_categories)
  prompt = (
    "You are an assistant whose job is to summarize articles and determine the best category for the article "
    "from a given list of user-generated categories.\n\n"
    "Instructions:\n"
    "1. Summarize the article in exactly 3 concise bullet points.\n"
    "2. Given the user-generated categories: " + categories_str + ", assess whether the article fits into one of those categories. "
    "If it does, return that category exactly as provided. If it does not, suggest a new category that best describes the article; "
    "this new category must be a single word.\n\n"
    "Return your answer in JSON format with two keys: 'summary' (an array of bullet points) and 'category' (a string).\n"
    "For example: {\"summary\": [\"Bullet 1\", \"Bullet 2\", \"Bullet 3\"], \"category\": \"News\"}\n\n"
    "Article Text:\n" + text
  )


  try:
    # time.sleep(10)
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
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
      max_tokens=200
    )
    answer_str = response.choices[0].message.content
    if answer_str.startswith("```"):
      answer_str = re.sub(r"^```(json)?\n", "", answer_str)
      answer_str = re.sub(r"\n```")
    try:
      result = json.loads(answer_str)
    except json.JSONDecodeError as json_err:
      result = {
        "error": f"JSON parsing error: {str(json_err)}",
        "raw": answer_str,
        "prompt": prompt
      }
      return result
  except Exception as e:
    result = {
      "error": f"OpenAI processing failed: {str(e)}",
      "raw": answer_str if 'answer_str' in locals() else None
    }
    return result
  
  if "category" in result:
    predicted_category = result["category"]
    final_category, is_new = assign_category(predicted_category, user_categories)
    result["category"] = final_category
    result["is_new_category"] = is_new

  return result

if __name__ == "__main__":
  sample_text = (
    "SpaceX has launched its latest Starship rocket, designed for interplanetary travel. "
    "The innovative design focuses on reusability, advanced technology, and cost efficiency, "
    "making space travel more accessible than ever."
  )
  # Simulate user-generated categories:
  categories = ["Sci-Fi", "Technology", "News"]
  output = summarize_and_sort(sample_text, categories)
  print(json.dumps(output, indent=2))