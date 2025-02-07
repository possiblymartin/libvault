import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.routes import api_blueprint
from models.models import db

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///libvault.db')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  Migrate(app, db)

  app.register_blueprint(api_blueprint, url_prefix='/api')

  return app

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    db.create_all()
  app.run(debug=True)