from flask import Blueprint, jsonify, request
from models.models import Article, Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

articles_blueprint = Blueprint('articles', __name__)
CORS(articles_blueprint)

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