from flask import Blueprint, request, jsonify
from models.models import db, User

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
  password = User(password)

  db.session.add(user)
  db.session.commit()

  return jsonify({'message': 'User created successfully.'}), 201