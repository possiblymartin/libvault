from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from api.routes import api_blueprint
from models.models import db

db = SQLAlchemy()
migrate = Migrate()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libvault.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  migrate.init_app(app, db)

  app.register_blueprint(api_blueprint, url_prefix='/api')

  return app

if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)