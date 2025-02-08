import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.routes import api_blueprint
from models.models import db

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///libvault.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

  CORS(
    app,
    resources={r"/api/*": {
      "origins": "http://localhost:5173",
      "supports_credentials": True,
      "expose_headers": ["Authorization"]
    }},
    supports_credentials=True
  )


  db.init_app(app)
  Migrate(app, db)
  JWTManager(app)

  app.register_blueprint(api_blueprint, url_prefix='/api')

  return app

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    db.create_all()
  app.run(debug=True)