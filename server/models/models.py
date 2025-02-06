from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  articles = db.relationship('Article', backref='author', lazy=True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
      
class Article(db.Model):
  __tablename__ = 'articles'
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(500), unique=True, nullable=False)
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text, nullable=False)
  summary = db.Column(db.Text)
  category = db.Column(db.String(100))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  def __repr__(self):
    return f'<Article(id={self.id}, title={self.title})>'
