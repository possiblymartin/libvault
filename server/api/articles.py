from flask import Blueprint, jsonify, request
from models.models import db, Article, Category, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from bs4 import BeautifulSoup
from utils.openai_processor import summarize_and_sort
from utils.extensions import limiter
import requests
import re

articles_blueprint = Blueprint('articles', __name__)

def normalize_spacing(text):
  """Ensure space after periods when missing before lowercase letters"""
  text = re.sub(r'\.([a-zA-Z])', r'. \1', text)
  return re.sub(r'\n{3,}', '\n\n', text)

def insert_missing_paragraph_breaks(text):
  """
  It is safe to assume after a full stop, if whitespace is not present in the text, a new paragraph begins. 
  """
  # Look for a period directly followed by a non-whitespace character.
  return re.sub(r'\.(?=\S)', '.\n\n', text)

def clean_extracted_text(text):
  """
  Cleans the extracted text by removing lines that are weird i.e. chapter headers or navigation text. 
  """
  text = normalize_spacing(text)

  paragraphs = []
  current_para = []

  for line in text.splitlines():
    stripped = line.strip()
    if not stripped:
      if current_para:
        paragraphs.append(" ".join(current_para))
        current_para = []
      continue

    if any(re.match(p, stripped, re.I) for p in [
      r'^(Ch\.?\s*\d+)$',
      r'^(Chapter\s+\d+:?)$'
    ]):
      continue

    sentences = re.split(r'\. (?=[A-Z])', stripped)
    current_para.extend(sentences)
  
  if current_para:
    paragraphs.append(" ".join(current_para))
  
  cleaned_text = "\n\n".join(
    p.replace('. ', '.\n')
     .replace('  ', ' ')
     .strip()
    for p in paragraphs if p.strip()
  )
  return cleaned_text

def is_potential_navigation(div):
  """
  If the number of words is low in comparison to the number of links the div is likely
  to part of a navigation or footer element. 
  """
  text = div.get_text(separator=" ", strip=True)
  words = text.split()
  num_words = len(words)
  num_links = len(div.find_all("a"))
  if num_links and (num_words / num_links) < 3:
    return True
  return False

def extract_main_content(html):
  """
  Given HTML content, attempt to extract the main article body.
  First, it checks for candidate IDs or class names that are common
  for article content (e.g. "maincontent", "article-body", etc.).
  If none are found, it falls back to scanning all <div> elements and
  selecting the one with the largest block of text that does not appear
  to be navigational.
  """
  soup = BeautifulSoup(html, 'html.parser')

  # Remove generally rubbish tags
  for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

  # List of common identifiers used for the content of an article
  candidate_identifiers = [
    "maincontent", "article-body", "text-block", "main-content", "entry-content", "post-content"
  ]

  main_elem = None
  # Try finding by ID
  for candidate in candidate_identifiers:
    main_elem = soup.find(id=lambda x: x and candidate in x.lower())
    if main_elem:
      break

  # If not found try by class
  if not main_elem:
    for candidate in candidate_identifiers:
      main_elem = soup.find(class_=lambda c: c and candidate in c.lower())
      if main_elem:
        break

  # FALLBACK
  # Perhaps we should be keeping links within the text?
  if not main_elem:
    divs = soup.find_all("div")
    best_div = None
    max_text_length = 0
    for div in divs:
      for tag in div.find_all(["script", "style", "header", "footer", "iframe", "video"]):
        tag.decompose()
      text = div.get_text(separator="\n", strip=True)
      # Skip very short candidates
      if len(text) < 200:
        continue
      links = div.find_all("a")
      if links:
        words = text.split()
        if len(words) / len(links) < 3:
          continue
      if len(text) > max_text_length:
        max_text_length = len(text)
        best_div = div
    main_elem = best_div

  # LAST RESORT :(
  if not main_elem:
    main_elem = soup.find("body")
  
  for tag in main_elem.find_all(["script", "style", "nav", "header", "footer", "iframe", "video"]):
    tag.decompose()

  paragraphs = main_elem.find_all("p")
  if paragraphs:
    extracted_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
  else:
    extracted_text = main_elem.get_text(separator="\n", strip=True)
  
  cleaned_text = clean_extracted_text(extracted_text)
  return cleaned_text


@articles_blueprint.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
  user_id = get_jwt_identity()
  categories = Category.query.filter_by(user_id=user_id).all()
  return jsonify([{"id": c.id, "name": c.name} for c in categories]), 200

@articles_blueprint.route('/analyze-content', methods=['GET'])
@limiter.limit("5 per minute")
@jwt_required()
def analyze_content():
  """Analyze content without URL processing"""
  data = request.json
  content = data.get('content', '')[:10000] # Limit input size
  user_id = get_jwt_identity()

  if not content:
    return jsonify({"error": "no content provided"}), 400

  try:
    # Get user's existing categories
    user_categories = [cat.name for cat in Category.query.filter_by(user_id=user_id).all()]

    # Process with OpenAI
    processed = summarize_and_sort(content, user_categories)

    if 'error' in processed:
      return jsonify({"error": processed["error"]}), 400

    return jsonify({
      "summary": processed.get('summary', []),
      "category": processed.get('category', 'Uncategorized'),
      "is_new_category": processed.get('is_new_category', False)
    }), 200
  
  except Exception as e:
    return jsonify({
      "error": f"Content processing failed: {str(e)}",
      "status": "error"
    }), 500


@articles_blueprint.route('/process-url', methods=['POST'])
@limiter.limit("5 per minute")
@jwt_required()
def process_url():
  data = request.get_json()
  url = data.get('url')
  user_id = get_jwt_identity()
  current_user = User.query.get(user_id)

  try:
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.get_text(strip=True) if soup.title else "Untitled"

    content = extract_main_content(html)
    if not content:
      return jsonify({"error": "No article content found at this URL"}), 400

  except Exception as e:
    return jsonify({"error": f"Failed to scrape article: {str(e)}"}), 400

  user_categories = [cat.name for cat in current_user.categories]

  # Summarize and categorize the scraped content using OpenAI
  try:
    processed = summarize_and_sort(content, user_categories)
    if 'error' in processed:
      return jsonify(processed), 500
  except Exception as e:
    return jsonify({"error": f"Processing failed: {str(e)}"}), 500
  
  # Handle new category if necessary
  if processed.get('is_new_category', False):
    new_category = Category(
      name=processed['category'],
      user_id=user_id
    )
    db.session.add(new_category)
    db.session.commit()
    category_id = new_category.id
  else:
    category = Category.query.filter_by(name=processed['category'], user_id=user_id).first()
    category_id = category.id if category else None

  # Save processed article
  try:
    new_article = Article(
      title=title,
      content=content,
      summary='\n'.join(processed['summary']),
      url=url,
      category_id=category_id,
      user_id=user_id
    )
    db.session.add(new_article)
    db.session.commit()
  except Exception as e:
    return jsonify({"error": f"Failed saving new article: {str(e)}"}), 500
  
  return jsonify({
    "message": "Article processed and saved",
    "article": {
      "id": new_article.id,
      "title": title,
      "summary": processed['summary'],
      "category": processed['category'],
      "url": url
    }
  }), 201


@articles_blueprint.route('/articles', methods=['GET'])
@jwt_required()
def get_articles():
  user_id = get_jwt_identity()
  category_id = request.args.get('category')

  query = Article.query.filter_by(user_id=user_id)
  if category_id:
    query = query.filter_by(category_id=category_id)
  
  articles = query.all()

  return jsonify([{
    "id": a.id,
    "title": a.title,
    "summary": a.summary,
    "url": a.url,
    "content": a.content
  } for a in articles]), 200


@articles_blueprint.route('/articles/<int:article_id>', methods=['GET'])
@jwt_required()
def get_article(article_id):
  user_id = get_jwt_identity()
  article = Article.query.filter_by(id=article_id, user_id=user_id).first()

  if not article:
    return jsonify({"error": "Article not found or does not exist"}), 404

  return jsonify({
    "id": article.id,
    "title": article.title,
    "summary": article.summary,
    "content": article.content,
    "url": article.url,
    "category": article.category_obj.name if article.category_obj else "Uncategorized"
  }), 200