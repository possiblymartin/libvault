from flask import Blueprint, request, jsonify
from authlib.integrations.flask_client import OAuth
from models.models import db, User
from flask_jwt_extended import create_access_token
import os
from dotenv import load_dotenv

load_dotenv()

auth_blueprint = Blueprint('auth', __name__)
oauth = OAuth()

google = oauth.register(
  name='google',
  client_id=os.getenv("GOOGLE_CLIENT_ID"),
  client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
  access_token_url='https://oauth2.googleapis.com/token',
  authorize_url='https://accounts.google.com/o/oauth2/auth',
  api_base_url='https://www.googleapis.com/oauth2/v1/',
  client_kwargs={'scope': 'email profile'},
)

@auth_blueprint.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({'error': 'Email and password are required.'}), 400
  
  if User.query.filter_by(email=email).first():
    return jsonify({'error': 'Email already exists.'}), 400

  user = User(email=email)
  user.set_password(password)

  db.session.add(user)
  db.session.commit()

  return jsonify({'message': 'User created successfully.'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({'error': 'Email and password are required.'}), 400

  user = User.query.filter_by(email=email).first()
  if not user or not user.check_password(password):
    return jsonify({'error': 'Invalid credentials.'}), 400

  access_token = create_access_token(identity=user.id)
  return jsonify(access_token=access_token), 200

@auth_blueprint.route('/google', methods=['POST'])
def google_auth():
  """Handle Google Oauth login/registration"""
  code = request.json.get('code')
  if not code:
    return jsonify({"error": "Authorization code required"}), 400

  try:
    token = google.fetch_access_token(code=code)
    user_info = google.get('userinfo').json()
  except Exception as e:
    return jsonify({"error": f"Google authentication failed: {str(e)}"}), 401

  user = User.query.filter_by(email=user_info['email']).first()
  if not user:
    user = User(
      email=user_info['email'],
      name=user_info.get('name', ''),
      # OAuth users do not need a password
      password_hash=''
    )
    db.session.add(user)
    db.session.commit()
  
  access_token = create_access_token(identity=user.id)
  return jsonify(access_token=access_token), 200
