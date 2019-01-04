from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

Base = declarative_base()

class RecipeUsers(Base):
    __tablename__ = 'recipeUsers'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=True)
    email = Column(String(250), nullable=False)


class Recipes(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    cuisine = Column(String(250))
    meal = Column(String(250))
    date = Column(DateTime)
    picture = Column(String(500))
    user_id = Column(Integer, ForeignKey('recipeUsers.id'))
    user = relationship(RecipeUsers)

class RecipeIngredients(Base):
    __tablename__ = 'recipeIngredients'

    id = Column(Integer, primary_key=True)
    ingredient = Column(String(250))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship(Recipes)

class RecipeProcess(Base):
    __tablename__ = 'recipeProcess'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship(Recipes)
    process = Column(String(1000))


class RecipeComments(Base):
    __tablename__ = 'recipeComments'

    id = Column(Integer, primary_key=True)
    comment = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('recipeUsers.id'))
    user = relationship(RecipeUsers)
    date = Column(DateTime)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship(Recipes)


class RecipeLikes(Base):
    __tablename__ = 'recipeLikes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('recipeUsers.id'))
    user = relationship(RecipeUsers)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    recipe = relationship(Recipes)

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
    player1id = Column(Integer, ForeignKey('ghostUser.id'))
    player2id = Column(Integer, ForeignKey('ghostUser.id'))
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
    previousPlayer = Column(Integer, ForeignKey('ghostUser.id'))
    previousGhost = Column(String(4), nullable=False)

class ghostComplete(Base):
    __tablename__ = 'ghostComplete'

    id = Column(Integer, primary_key=True)
    gameid = Column(Integer,nullable=False)
    player1id = Column(Integer, ForeignKey('ghostUser.id'))
    player2id = Column(Integer, ForeignKey('ghostUser.id'))
    winnerid = Column(Integer, ForeignKey('ghostUser.id'))
    completed = Column(DateTime)
    won = Column(String(6))

class SurveyUsers(Base):
    __tablename__ = 'SurveyUsers'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)


class SurveyQuestions(Base):
    __tablename__ = 'SurveyQuestions'

    id = Column(Integer, primary_key=True)
    question = Column(String(1000), nullable=False)
    option1 = Column(String(1000), nullable=True)
    option2 = Column(String(1000), nullable=True)
    option3 = Column(String(1000), nullable=True)
    option4 = Column(String(1000), nullable=True)
    option5 = Column(String(1000), nullable=True)


class SurveyResults(Base):
    __tablename__ = 'SurveyResults'

    id = Column(Integer, primary_key=True)
    choice = Column(String(1000), nullable=False)
    question_id = Column(Integer, ForeignKey('SurveyQuestions.id'))
    question = relationship(SurveyQuestions)
    user_id = Column(Integer, ForeignKey('SurveyUsers.id'))
    user = relationship(SurveyUsers)


class PoolUsers(Base):
    __tablename__ = 'PoolUsers'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class PoolGolfers(Base):
    __tablename__ = 'PoolGolfers'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    country = Column(String(250), nullable=False)
    currentRank = Column(Integer, nullable=True)
    startingRank = Column(Integer, nullable=False)
    group_id = Column(Integer, ForeignKey('PoolGroups.id'))
    group = relationship(PoolGroups) 


class PoolGroups(Base):
    __tablename__ = 'PoolGroups'

    id = Column(Integer, primary_key=True)
    groupname = Column(String(1000), nullable=False)


class PoolChoices(Base):
    __tablename__ = 'PoolChoices'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('PoolGroups.id'))
    group = relationship(PoolGroups)
    golfer_id = Column(Integer, ForeignKey('PoolGolfers.id'))
    golfer = relationship(PoolGolfers)
    user_id = Column(Integer, ForeignKey('PoolUsers.id'))
    user = relationship(PoolUsers)


class PoolTournaments(Base):
    __tablename__ = 'PoolTournaments'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)

class PoolResults(Base):
    __tablename__ = 'PoolResults'

    id = Column(Integer, primary_key=True)
    golfer_id = Column(Integer, ForeignKey('PoolGolfers.id'))
    golfer = relationship(PoolGolfers)
    tournament_id = Column(Integer, ForeignKey('PoolTournaments.id'))
    tournament = relationship(PoolTournaments)
    position = Column(Integer, nullable=False)
    overall = Column(Integer, nullable=False)


engine = create_engine('sqlite:////var/www/jbv2/jbv2/jb.db')

Base.metadata.create_all(engine)
