from flask import Blueprint, request, jsonify
from models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')

# Register new user
@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  if not email or not password:
    return jsonify({'error': 'Email and password are required'}), 400

  existing_user = User.query.filter_by(email).first()
  if existing_user:
    return jsonify({'error': 'A user with this email already exists'}), 400

  hashed_password = generate_password_hash(password)
  new_user = User(email=email, password_hash=hashed_password)
  db.session.add(new_user)
  db.session.commit()

  return jsonify({'message': 'User created successfully'}), 201

# Login user
@auth_bp.route('/login', methods=['GET'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')

  user = User.query.filter_by(email=email).first()
  if not user or not check_password_hash:
    return jsonify({'error': 'Invalid credentials'}), 401

  token = jwt.encode({
    'user_id': user.id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
  }, SECRET_KEY, algorithm='HS256')

  return jsonify({'token': token, 'subscription_tier': user.subscription_tier}), 200

# Get subscription details
@auth_bp.route('/users/<int:user_id>/subscription', methods=['GET'])
def get_subscription(user_id):
  user = User.query.get(user_id)
  if not user:
    return jsonify({'error': 'User not found'}), 404

  return jsonify({'subscription_tier': user.subscription_tier, 'status': user.subscription_status}), 200