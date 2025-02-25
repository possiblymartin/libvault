from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  subscription_tier = db.Column(db.String(50), default="free") # free, pro, premium
  subscription_status = db.Column(db.String(20), default="inactive") # active, inactive
  avatar = db.Column(db.String(200))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  articles = db.relationship('Article', backref=db.backref('user', lazy=True))

  def __repr__(self):
    return f'<User {self.email}, Tier: {self.subscription_tier}>'

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return f'<Category {self.name}>'
      
class Article(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text, nullable=False)
  url = db.Column(db.String(500), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
  category = db.relationship('Category', backref=db.backref('articles', lazy=True))
  shared_link = db.Column(db.String(100), unique=True, nullable=True)
  annotations = db.Column(db.Text, nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def generate_shared_link(self):
    self.shared_link = str(uuid.uuid4())
  
  def __repr__(self):
    return f'<Article(id={self.id}, title={self.title})>'
