from flask import Blueprint, request, jsonify
from models.models import db, User
from flask_jwt_extended import create_access_token

auth_blueprint = Blueprint('auth', __name__)

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
  return jsonify({
    'message': 'Login successful',
    'access_token': access_token
  }), 200
