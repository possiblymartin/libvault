from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  name = db.Column(db.String(100))
  avatar = db.Column(db.String(200))
  auth_provider = db.Column(db.String(20), default='email')
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  articles = db.relationship('Article', backref='author', lazy=True)
  categories = db.relationship('Category', backref='owner', lazy=True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  articles = db.relationship('Article', backref='category_obj', lazy=True, foreign_keys='Article.category_id', primaryjoin='Category.id == Article.category_id')
      
class Article(db.Model):
  __tablename__ = 'articles'
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(500), unique=True, nullable=False)
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text, nullable=False)
  summary = db.Column(db.Text)
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  def __repr__(self):
    return f'<Article(id={self.id}, title={self.title})>'
