import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.models import db

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///libvault.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')


  db.init_app(app)
  Migrate(app, db)
  JWTManager(app)
  CORS(
    app,
    resources={r"/api/*": {
      "origins": "http://localhost:5173",
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "allow_headers": ["Content-Type", "Authorization"]
    }},
    supports_credentials=True
  )

  from api.routes import api_blueprint
  from api.articles import articles_blueprint
  app.register_blueprint(api_blueprint, url_prefix='/api')
  app.register_blueprint(articles_blueprint, url_prefix='/api')

  return app

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    db.create_all()
  app.run(debug=True)