from flask import Blueprint, jsonify
from api.auth import auth_blueprint

api_blueprint = Blueprint('api', __name__)
api_blueprint.register_blueprint(auth_blueprint, url_prefix='/auth')

@api_blueprint.route('/')
def index():
  return jsonify({"message": "libvault API is running correctly"})