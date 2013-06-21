from app import db
from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()
Base = db.Model

class User(Base):
    __tablename__ = 'users'

    __table_args__ = {}


    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    recipes = db.relationship('Recipe', backref = 'author', lazy = 'dynamic')

    def to_json(self):
        return dict(id = self.id,
                    name=self.name,
                    email = self.email)

    def __repr__(self):
        return '<User %r>' % (self.name)

class Post(Base):
    __tablename__ = 'posts'

    __table_args__ = {}


    
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Recipe(Base):
    __tablename__ = 'recipes'

    __table_args__ = {}


    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    ingredients = db.Column(db.String(512))
    instructions = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return dict(id = self.id,
                    name=self.name,
                    ingredients=self.ingredients,
                    instructions=self.instructions,
                    author=self.author.name)
    
    def __repr__(self):
        return '<Recipe %r>' % (self.name)
