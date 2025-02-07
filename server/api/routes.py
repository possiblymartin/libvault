from flask import Blueprint, jsonify, request
from api.auth import auth_blueprint
from utils.openai_processor import summarize_and_sort

api_blueprint = Blueprint('api', __name__)
api_blueprint.register_blueprint(auth_blueprint, url_prefix='/auth')

@api_blueprint.route("/process-article", methods=["POST"])
def process_article():
  data = request.get_json()
  article_text = data.get("text")
  user_categories = data.get("user_categories") # Expected to be a list

  if not article_text:
    return jsonify({"error": "Article text is required"}), 400
  
  if not user_categories or not isinstance(user_categories, list):
    return jsonify({"error": "User categories are required as a list"}), 400
  
  result = summarize_and_sort(article_text, user_categories)
  if "error" in result:
    return jsonify(result), 500
  return jsonify(result), 200

@api_blueprint.route('/')
def index():
  return jsonify({"message": "libvault API is running correctly"})