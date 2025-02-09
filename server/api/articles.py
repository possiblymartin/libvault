from flask import Blueprint, jsonify, request
from models.models import db, Article, Category, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from bs4 import BeautifulSoup
from utils.openai_processor import summarize_and_sort
from utils.extensions import limiter
import requests
import re

articles_blueprint = Blueprint('articles', __name__)

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
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the page title
    title = soup.title.get_text(strip=True) if soup.title else "Untitled"

    article_element = soup.find('article')
    if article_element:
      for tag in article_element.find_all(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
      content = article_element.get_text(separator="\n", strip=True)
    else:
      content_wrapper = soup.find('div', id=re.compile(r'content|main', re.I)) or \
                        soup.find('div', class_=re.compile(r'content|main|article', re.I))
      if content_wrapper:
        for tag in content_wrapper.find_all(["script", "style", "nav", "header", "footer"]):
          tag.decompose()
        content = content_wrapper.get_text(separator="\n", strip=True)
      else:
        for tag in soup(["script", "style", "nav", "header", "footer"]):
          tag.decompose()
        content = soup.get_text(separator="\n", strip=True)

    if not content:
      return jsonify({"error": "No article found at this URL"}), 400
      
  except Exception as e:
    return jsonify({"error": f"Failed to scrape article: {str(e)}"}), 400
  
  user_categories = [cat.name for cat in current_user.categories]

  # Summarize and sort scraped content
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
    db.session.rollback()
    return jsonify({"error": f"Failed to save article: {str(e)}"}), 500
  
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