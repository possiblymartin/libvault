from flask import Blueprint, request, jsonify
from models.models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('profile', methods=['GET'])
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

@users_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  if not user:
    return jsonify({"error": "User not found"}), 404
  
  data = request.get_json()
  new_name = data.get("name")
  new_avatar = data.get("avatar")

  if new_name:
    user.name = new_name
  if new_avatar:
    user.avatar = new_avatar

  try:
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500
