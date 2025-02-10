from flask import Blueprint, request, jsonify
from models.models import db, User, Article, Category
import uuid

routes = Blueprint('routes', __name__)

# Create a new category if it doesn't exist
@routes.route('/categories', methods=['POST'])
def create_category():
  data = request.get_json()
  category_name = data.get('name')

  if not category_name:
    return jsonify({'error': 'Category name is required'}), 400
  
  existing_category = Category.query.filter_by(name=category_name).first()
  if existing_category:
    return jsonify({'message': 'Category already exists', 'category_id': existing_category}), 200

  new_category = Category(name=category_name)
  db.session.add(new_category)
  db.session.commit()

  return jsonify({'message': 'Category created', 'category_id': new_category.id}), 201

# Move an article to another category
@routes.route('/articles/<int:article_id>/move', methods=['PUT'])
def move_article(article_id):
  data = request.get_json()
  new_category_id = data.get('category_id')

  article = Article.query.get(article_id)
  if not article:
    return jsonify({'error': 'Article not found'}), 404
  
  category = Category.query.get(new_category_id)
  if not category:
    return jsonify({'error': 'Target category not found'}), 404
  
  article.category_id = new_category_id
  db.session.commit()

  return jsonify({'message': 'Article moved successfully'}), 200

# Generate a shareable link for an article
@routes.route('/articles/<int:article_id>/share', methods=['POST'])
def share_article(article_id):
  article = Article.query.get(article_id)
  if not article:
    return jsonify({'error': 'Article not found'}), 404
  
  if not article.shared_link:
    article.generate_shared_link()
    db.sesion.commit()
  
  # Change this with domain name after production
  return jsonify({'shared_link': f'http://localhost:5173/share/{article.shared_link}'}), 200

# Retrieve an article via a shared link
@routes.route('/share/<string:shared_link>', methods=['GET'])
def get_shared_article(shared_link):
  article = Article.query.filter_by(shared_link=shared_link).first()
  if not article:
    return jsonify({'error': 'Shared article not found'}), 404

  return jsonify({
    'title': article.title,
    'content': article.content,
    'annotations': article.annotations
  }), 200

# Delete an article
@routes.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
  article = Article.query.get(article_id)
  if not article:
    return jsonify({'error': 'Article not found'}), 404
  
  db.session.delete(article)
  db.session.commit()

  return jsonify({'message': 'Article deleted successfully'}), 200

# Edit an article and add annotations
@routes.route('/articles/<int:article_id>', methods=['PUT'])
def edit_article(article_id):
  data = request.get_json()
  article = Article.query.get(article_id)
  if not article:
    return jsonify({'error': 'Article not found'}), 404
  
  article.title = data.get('title', article.title)
  article.content = data.get('content', article.content)
  article.annotations = data.get('annotations', article.annotations)

  db.session.commit()

  return jsonify({'message': 'Article modified successfully'}), 200

# Manage user subscription status
@routes.route('/users/<int:user_id>/subscription', methods=['PUT'])
def update_subscription():
  data = request.get_json()
  user = User.query.get(user_id)

  if not user:
    return jsonify({'error': 'User not found'}), 404

  new_tier = data.get('subscription_tier')
  if new_tier not in ['free', 'pro', 'premium']:
    return jsonify({'error': 'Invalid subscription tier'}), 400

  user.subscription.tier = new_tier
  user.subscription.status = 'active'
  db.session.commit()

  return jsonify({'message': 'Subscription updated', 'new_tier': user.subscription.tier}), 200


  