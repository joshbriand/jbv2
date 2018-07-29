from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from survey_database_setup import Base, Users, Questions, Answers, Results

import psycopg2

engine = create_engine('sqlite:////var/www/jbv2/jbv2/survey.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

newUser = Users(username="admin", password="59545")
session.add(newUser)
session.commit()
print "Added admin user"
