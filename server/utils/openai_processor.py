import os
import re
import json
import difflib
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

# ---------------------------- CATEGORY FUNCTIONS ---------------------------- #
def normalize_category(category: str) -> str:
  """
  Normalizes category names by stripping whitespace and using only the first word 
  if the category consists of multiple words.
  """
  words = category.strip().split()
  return words[0] if len(words) > 1 else category.strip()

def assign_category(predicted_category: str, user_categories: list, threshold: float = 0.7):
  """
  Assigns the best category based on the AI's predicted category and the user's predefined categories.

  - If a close match is found in `user_categories`, return that existing category.
  - If no close match is found, create a new normalized category.

  Returns:
    - final_category (str): The assigned or newly created category.
    - is_new (bool): True if a new category was created, False if matched with an existing category.
  """
  normalized_pred = predicted_category.lower().strip()
  normalized_user = [cat.lower().strip() for cat in user_categories]

  # Find a close match in the user-provided categories
  matches = difflib.get_close_matches(normalized_pred, normalized_user, n=1, cutoff=threshold)
  
  if matches:
    for cat in user_categories:
      if cat.lower().strip() == matches[0]:
        return cat, False  # Found an existing category

  # No match found, create a new category
  new_category = normalize_category(predicted_category)
  return new_category, True

def categorize_article(text: str, user_categories: list):
  """
  Determines the most suitable category for the given article.

  - If it fits into an existing user-defined category, return that category.
  - Otherwise, suggest a new category (single word).

  Returns:
    - "category": The assigned or newly created category.
    - "is_new_category": Boolean indicating if a new category was created.
    - "emoji": An emoji representing the category.
  """
  categories_str = ', '.join(user_categories) if user_categories else "None"

  prompt = (
    "You are an AI that categorizes articles based on user-provided categories and generates a matching emoji for the category.\n\n"
    "Instructions:\n"
    "1. Given the following user-generated categories: " + categories_str + ", determine if the article fits into one of these categories.\n"
    "   - If it does, return the category exactly as provided and a matching emoji that represents that category.\n"
    "   - If it does not, suggest a new category using a **single word** and provide a matching emoji for that category.\n\n"
    "Return the response in JSON format:\n"
    "{ \"category\": \"SelectedCategory\", \"emoji\": \"MatchingEmoji\" }\n\n"
    "Article Text:\n" + text
  )

  try:
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You categorize articles based on user categories and generate an appropriate emoji for the category."},
        {"role": "user", "content": prompt}
      ],
      temperature=0.5,
      max_tokens=60
    )

    answer_str = response.choices[0].message.content

    # Ensure JSON is properly formatted
    if answer_str.startswith("```"):
      answer_str = re.sub(r"^```(json)?\n", "", answer_str)
      answer_str = re.sub(r"\n```", "", answer_str)

    result = json.loads(answer_str)
  except Exception as e:
    return {"error": f"OpenAI categorization failed: {str(e)}"}

  # Assign the final category
  if "category" in result:
    predicted_category = result["category"]
    final_category, is_new = assign_category(predicted_category, user_categories)
    result["category"] = final_category
    result["is_new_category"] = is_new
    if "emoji" not in result or not result["emoji"]:
      result["emoji"] = "❓"
  return result

# ---------------------------- DUPLICATE DETECTION ---------------------------- #
def is_duplicate_article(new_text: str, existing_articles: list, similarity_threshold: float = 0.9):
  """
  Checks if the new article is a duplicate of an existing one using a similarity comparison.

  - Uses difflib to compare similarity between new text and stored articles.
  - Returns True if a duplicate is found, otherwise False.
  """
  new_text_lower = new_text.lower().strip()

  for article in existing_articles:
    existing_text_lower = article.lower().strip()
    similarity = difflib.SequenceMatcher(None, new_text_lower, existing_text_lower).ratio()
    
    if similarity >= similarity_threshold:
      return True  # Found a duplicate article
  
  return False  # No duplicate found

# ---------------------------- SUMMARIZATION & TAGGING ---------------------------- #
def summarize_and_tag(text: str):
  """
  Summarizes the article and generates relevant tags.

  - Summary: Generates exactly 3 bullet points.
  - Title: AI generates a concise, engaging title.
  - Tags: AI suggests 3-5 relevant tags based on the article content.

  Returns:
    - "title": AI-generated article title.
    - "summary": List of 3 bullet points summarizing the article.
    - "tags": Suggested tags as a list of strings.
  """

  prompt = (
    "You are an AI assistant that summarizes and tags articles.\n\n"
    "Instructions:\n"
    "1. Summarize the article in exactly 3 concise bullet points.\n"
    "2. Generate a short, engaging title for the article.\n"
    "3. Suggest 3-5 relevant **tags** for this article, separated by commas.\n\n"
    "Return the response in JSON format:\n"
    "{\n"
    "   \"title\": \"Generated Article Title\",\n"
    "   \"summary\": [\"Bullet 1\", \"Bullet 2\", \"Bullet 3\"],\n"
    "   \"tags\": [\"tag1\", \"tag2\", \"tag3\"]\n"
    "}\n\n"
    "Article Text:\n" + text
  )

  try:
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You summarize and tag articles."},
        {"role": "user", "content": prompt}
      ],
      temperature=0.7,
      max_tokens=250
    )

    answer_str = response.choices[0].message.content

    match = re.search(r'({.*})', answer_str, re.DOTALL)
    if match:
      result = json.loads(match.group(1))
    else:
      return result
    
  except json.JSONDecodeError as e:
    return {"error": f"Failed to parse JSON response: {str(e)}"}
  except Exception as e:
    return {"error": f"OpenAI summarization failed: {str(e.__class__.__name__): {str(e)}}"}

# ---------------------------- FINAL PROCESSING FUNCTION ---------------------------- #
def process_article(text: str, user_categories: list):
  """
  Main function that processes an article by:
  1. Summarizing it and generating a title.
  2. Categorizing it based on user categories.
  3. Generating relevant tags.

  Returns:
    - "title": AI-generated article title.
    - "summary": List of 3 bullet points summarizing the article.
    - "category": The assigned category.
    - "is_new_category": Boolean indicating if a new category was created.
    - "tags": Suggested tags as a list of strings.
  """
  summary_data = summarize_and_tag(text)
  category_data = categorize_article(text, user_categories)

  # Combine results
  return {**summary_data, **category_data}
