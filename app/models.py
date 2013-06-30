from app import db
from sqlalchemy.ext.declarative import declarative_base


ROLE_USER = 0
ROLE_ADMIN = 1

#Base = declarative_base()
Base = db.Model

class User(Base):
    __tablename__ = 'user'

    __table_args__ = {}


    
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    recipes = db.relationship('Recipe')

    def to_json(self):
        return dict(id = self.id,
                    name=self.nickname,
                    email = self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Recipe(Base):
    __tablename__ = 'recipe'

    __table_args__ = {}


    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    ingredients = db.relationship("RecipeIngredient")
    instructions = db.Column(db.PickleType())
    author = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        return dict(id = self.id,
                    name=self.name,
                    ingredients=[x.name for x in self.ingredients],
                    instructions=self.instructions,
                    author=self.author)
    
    def __repr__(self):
        return '<Recipe %r>' % (self.name)

class RecipeIngredient(Base):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    parent_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def to_json(self):
        return dict(id = self.id,
                    name = self.name,
                    parent_id = self.parent_id)

    def __repr__(self):
        return 'Ingredient %r>' % (self.name)
