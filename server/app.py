import os
from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.models import db
from api.auth import oauth
from utils.extensions import limiter
from datetime import timedelta

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///libvault.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
  app.config.setdefault('RATELIMIT_STORAGE_URI', 'memory://')


  db.init_app(app)
  oauth.init_app(app)
  limiter.init_app(app)
  Migrate(app, db)
  JWTManager(app)
  CORS(
    app,
    resources={r"/*": {
      "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "allow_headers": ["Content-Type", "Authorization"]
    }},
    supports_credentials=True
  )

  @app.before_request
  def handle_options():
    if request.method == 'OPTIONS':
      return '', 200

  from api.routes import api_blueprint
  from api.articles import articles_blueprint
  from api.users import users_api_blueprint, public_users_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api')
  app.register_blueprint(articles_blueprint, url_prefix='/api')
  app.register_blueprint(users_api_blueprint, url_prefix='/api/users')
  app.register_blueprint(public_users_blueprint)

  return app

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    db.create_all()
  app.run(debug=True)