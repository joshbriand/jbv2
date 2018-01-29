from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    cuisine = Column(String(250))
    meal = Column(String(250))
    date = Column(DateTime)
    picture = Column(String(500))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'cuisine': self.cuisine,
            'meal': self.meal,
            'date': self.date,
            'picture': self.picture
        }


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    ingredient = Column(String(250))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'ingredient': self.ingredient
        }


class Process(Base):
    __tablename__ = 'process'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)
    process = Column(String(1000))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'process': self.process
        }


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    date = Column(DateTime)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)

class ghostUser(Base):
    __tablename__ = 'ghostUser'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    notifications = Column(String(2), nullable=False)

class ghostGame(Base):
    __tablename__ = 'ghostGame'

    id = Column(Integer, primary_key=True)
    player1id = Column(Integer, ForeignKey('user.id'))
    player2id = Column(Integer, ForeignKey('user.id'))
    date = Column(DateTime)
    b11 = Column(String(4))
    b21 = Column(String(4))
    b31 = Column(String(4))
    b41 = Column(String(4))
    b51 = Column(String(4))
    b61 = Column(String(4))
    b12 = Column(String(4))
    b22 = Column(String(4))
    b32 = Column(String(4))
    b42 = Column(String(4))
    b52 = Column(String(4))
    b62 = Column(String(4))
    b13 = Column(String(4))
    b23 = Column(String(4))
    b33 = Column(String(4))
    b43 = Column(String(4))
    b53 = Column(String(4))
    b63 = Column(String(4))
    b14 = Column(String(4))
    b24 = Column(String(4))
    b34 = Column(String(4))
    b44 = Column(String(4))
    b54 = Column(String(4))
    b64 = Column(String(4))
    b15 = Column(String(4))
    b25 = Column(String(4))
    b35 = Column(String(4))
    b45 = Column(String(4))
    b55 = Column(String(4))
    b65 = Column(String(4))
    b16 = Column(String(4))
    b26 = Column(String(4))
    b36 = Column(String(4))
    b46 = Column(String(4))
    b56 = Column(String(4))
    b66 = Column(String(4))
    previousPlayer = Column(Integer, ForeignKey('user.id'))
    previousGhost = Column(String(4), nullable=False)

class ghostComplete(Base):
    __tablename__ = 'ghostComplete'

    id = Column(Integer, primary_key=True)
    gameid = Column(Integer,nullable=False)
    player1id = Column(Integer, ForeignKey('user.id'))
    player2id = Column(Integer, ForeignKey('user.id'))
    winnerid = Column(Integer, ForeignKey('user.id'))
    completed = Column(DateTime)
    won = Column(String(6))


engine = create_engine('sqlite:////var/www/jbv2/jbv2/jb.db')

Base.metadata.create_all(engine)
