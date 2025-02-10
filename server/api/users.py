from flask import Blueprint, request, jsonify
from models.models import db, User, Article
from flask_jwt_extended import jwt_required, get_jwt_identity

users_api_blueprint = Blueprint('users_api', __name__)

@users_api_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  if not user:
    return jsonify({"error": "User not found"}), 404

  return jsonify({
    "id": user.id,
    "email": user.email,
    "name": user.name,
    "avatar": user.avatar
  }), 200

@users_api_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  if not user:
    return jsonify({"error": "User not found"}), 404
  
  data = request.get_json()
  new_username = data.get("username")
  new_full_name = data.get("full_name")
  new_library_status = data.get("is_library_public")

  if new_username and new_username != user.username:
    if User.query.filter_by(username=new_username).first():
      return jsonify({"error": "Username already exists, choose a different one"}), 400
    user.username = new_username

  if new_full_name:
    user.full_name = new_full_name
  
  if new_library_status is not None:
    user.is_library_public = bool(new_library_status)
  
  try:
    db.session.commit()
    return jsonify({
      "message": "Profile updated successfully",
      "username": user.username,
      "is_library_publc": user.is_library_public}), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

public_users_blueprint = Blueprint('public_users', __name__)

@public_users_blueprint.route('/<string:username>', methods=['GET'])
def public_library(username):
  """Public route that displays the username in the following format libvault.io/username"""
  user = User.query.filter_by(username=username).first()
  if not user:
    return jsonify({"error": "This user's library is private"}), 403
  
  articles = Article.query.filter_by(user_id=user.id).all()
  articles_data = [{
    "id": article.id,
    "title": article.title,
    "summary": article.summary,
    "url": article.url
  } for article in articles]

  return jsonify({
    "username": user.username,
    "full_name": user.full_name,
    "avatar": user.avatar,
    "articles": articles_data
  }), 200
