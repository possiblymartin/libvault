from flask import Blueprint, jsonify

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/')
def index():
  return jsonify({"message": "libvault API is running correctly"})