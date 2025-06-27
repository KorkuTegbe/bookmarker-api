from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.Text(), nullable=False)
   bookmarks = db.relationship('Bookmark', backref="user")
   # created_at = db.column(db.DateTime, default=datetime.now)
   # updated_at = db.column(db.DateTime, onupdate=datetime.now)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   def __repr__(self):
      return 'User>>>{self.username}'
   
   def serialize(self):
      return {
         "id": self.id,
         "username": self.username,
         "email": self.email,
         # "bookmarks": [bookmark.serialize() for bookmark in self.bookmarks],
         "created_at": self.created_at,
         "updated_at": self.updated_at
      }
   
class Bookmark(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   body = db.Column(db.Text, nullable=True)
   url = db.Column(db.Text, nullable=False)
   short_url = db.Column(db.String(3), nullable=True)
   visits = db.Column(db.Integer, default=0)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   # created_at = db.column(db.DateTime, default=datetime.now)
   # updated_at = db.column(db.DateTime, onupdate=datetime.now)
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   
   def generate_short_chars(self):
      characters = string.digits+string.ascii_letters
      picked_chars = ''.join(random.choices(characters, k=3))

      link=self.query.filter_by(short_url=picked_chars).first()

      if link:
         self.generate_short_chars()
      else:
         return picked_chars

   def __init__(self, **kwargs):
      super().__init__(**kwargs)

      self.short_url = self.generate_short_chars()
   
   def __repl__(self):
      return 'Bookmark>>> {self.url}'
   
   def serialize(self):
      return {
         "id": self.id,
         "body": self.body,
         "url": self.url,
         "short_url": self.short_url,
         "visits": self.visits,
         # "created_at": self.created_at,
         # "updated_at": self.updated_at
      }
