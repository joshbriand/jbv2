from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database_setup import Base, RecipeUsers, Recipes, RecipeComments, RecipeLikes, RecipeProcess, RecipeIngredients, ghostUser, ghostGame, ghostComplete, SurveyUsers, SurveyResults, SurveyQuestions

import psycopg2

engine = create_engine('sqlite:////var/www/jbv2/jbv2/jb.db')
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
users = session.query(RecipeUsers)
for user in users:
    print user.id
    print user.name
    if user.id > 2:
        session.remove(user)
print "cleaned"
users = session.query(RecipeUsers)
for user in users:
    print user.id
    print user.name

# names=['admin', 'josh', 'adam', 'paul', 'stephen', 'james', 'jonathan']
# passwords=['admin', 'josh', 'adam', 'paul', 'stephen', 'james', 'jonathan']
#
# for x in range(0,len(names)):
#     if names[x] in usernames:
#         print names[x] + " exists already"
#     else:
#         newUser = ghostUser(name=names[x], password=passwords[x], email="joshbriand@gmail.com", notifications="no")
#         session.add(newUser)
#         session.commit()
#         print names[x] + " added"
#
# newUser = SurveyUsers(username="admin", password="59545")
# session.add(newUser)
# session.commit()
# print "Added admin user"
