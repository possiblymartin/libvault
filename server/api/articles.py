from flask import Blueprint, jsonify, request
from models.models import db, Article, Category, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from bs4 import BeautifulSoup
from utils.openai_processor import summarize_and_sort
import requests

articles_blueprint = Blueprint('articles', __name__)

@articles_blueprint.route('/process-url', methods=['POST'])
@jwt_required()
def process_url():
  data = request.get_json()
  url = data.get('url')
  user_id = get_jwt_identity()
  current_user = User.query.get(user_id)

  # Scrape article's content
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Untitled"
    article_body = soup.find('article') or soup.find('div', class_='article-body')
    content = ' '.join([p.get_text(strip=True) for p in article_body.find_all('p')]) if article_body else ""
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

@articles_blueprint.route('/articles', methods=["GET", "POST", "OPTIONS"])
def get_articles():
  if request.method == "OPTIONS":
    return jsonify({}), 200

  @jwt_required()
  def protected_route():
    user_id = get_jwt_identity()
    articles = Article.query.filter_by(user_id=user_id).all()

    articles_by_category = {}
    for article in articles:
      category_name = article.category_obj.name if article.category_obj else "Uncategorized"
      if category_name not in articles_by_category:
        articles_by_category[category_name] = []
        articles_by_category[category_name].append({
          "id": article.id,
          "title": article.title,
          "summary": article.summary,
          "url": article.url
        })
    return jsonify(articles_by_category), 200
  return protected_route()

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