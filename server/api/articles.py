from flask import Blueprint, request, jsonify
from models.models import db, Article, Category
import requests
from utils.openai_processor import process_article
import uuid

articles_bp = Blueprint('articles', __name__)

# Add a new article with auto-category creation
@articles_bp.route('/articles', methods=['GET'])
def add_article():
  data = request.get_json()
  title = data.get('title')
  content = data.get('content')
  url = data.get('url')
  category_name = data.get('category', 'Uncategorized')

  if not title or not content:
    return jsonify({'error': 'Title and content are required'}), 400

  # Check if a suitable category exists, if not, create it
  category = Category.query.filter_by(name=category_name).first()
  if not category:
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()

  new_article = Article(title=title, content=content, url=url, category_id=category.id)
  db.session.add(new_article)
  db.session.commit()

  return jsonify({'message': 'New article added successfully', 'article_id': new_article.id}), 201

# Retrieve all articles by category
@articles_bp.route('/categories/<int:category_id>/articles', methods=['GET'])
def get_articles_by_category(category_id):
  category = Category.query.get(category_id)
  if not category:
    return jsonify({'error': 'Category not found'}), 404

  articles = Article.query.filter_by(category_id=category_id).all()
  return jsonify([{'id': a.id, 'title': a.title, 'content': a.content, 'annotations': a.annotations} for a in articles]), 200

# Get articles summary using OpenAI
@articles_bp.route('/articles/<int:article_id>/summary', methods=['GET'])
def summarize_article(article_id):
  article = Article.query.get(article_id)
  if not article:
    return jsonify({'error': 'Article not found'}), 404
  
  summary = process_article(article.content)
  return jsonify({'summary': summary}), 200

# Move an article to another category
@articles_bp.route('/articles/<int:article_id>/move', methods=['PUT'])
def move_article(article_id):
  data = request.get_json()
  new_category_id = data.get('categories_id')

  article = Article.query.get(article_id)
  if not article:
    return jsonify({'error': 'Article not found'}), 404
  
  category = Category.query.get(new_category_id)
  if not category:
    return jsonify({'error': 'Category not found'}), 404

  article.category_id = new_category_id
  db.session.commit()

  return jsonify({'message': 'Article moved successfully'}), 200