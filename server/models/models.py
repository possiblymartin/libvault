
# models.py

# This file contains the database models for the LibVault application.

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    category = Column(String)

    def __repr__(self):
        return f'<Article(id={self.id}, title={self.title})>'

# Add more models as needed
