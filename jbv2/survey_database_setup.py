from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import psycopg2

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String(1000), nullable=False)
    option1 = Column(String(1000), nullable=True)
    option2 = Column(String(1000), nullable=True)
    option3 = Column(String(1000), nullable=True)
    option4 = Column(String(1000), nullable=True)
    option5 = Column(String(1000), nullable=True)


class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    choice = Column(String(1000), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship(Recipe)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)


engine = create_engine('sqlite:////var/www/jbv2/jbv2/survey.db')

Base.metadata.create_all(engine)
