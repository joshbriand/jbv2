from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database_setup import Base, RecipeUsers, Recipes, RecipeComments, RecipeLikes, RecipeProcess, RecipeIngredients, ghostUser, ghostGame, ghostComplete, SurveyUsers, SurveyResults, SurveyQuestions, PoolUsers, PoolGolfers, PoolGroups, PoolChoices, PoolTournaments, PoolResults


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

# tournaments = session.query(PoolTournaments)
# for tournie in tournaments:
#     tournie.delete()

groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=13).one()
newGolfer=PoolGolfers(name='Lee Westwood', country='ENG', startingRank=64, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Zach Johnson', country='USA', startingRank=66, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Ryan Moore', country='USA', startingRank=77, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Ryan Palmer', country='USA', startingRank=79, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Stewart Cink', country='USA', startingRank=84, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Jimmy Walker', country='USA', startingRank=88, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=17).one()
newGolfer=PoolGolfers(name='Andrew Landry', country='USA', startingRank=104, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Shubhankar Sharma', country='IND', startingRank=116, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Jason Kokrak', country='USA', startingRank=126, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Anirban Lahiri', country='IND', startingRank=143, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Jamie Lovemark', country='USA', startingRank=150, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Harold Varner III', country='USA', startingRank=158, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Ollie Schniederjans', country='USA', startingRank=168, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=10).one()
newGolfer=PoolGolfers(name='Brandt Snedeker', country='USA', startingRank=49, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Brian Harman', country='USA', startingRank=51, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Charlie Hoffman', country='USA', startingRank=53, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Charles Howell III', country='USA', startingRank=58, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Adam Hadwin', country='CAN', startingRank=67, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=14).one()
newGolfer=PoolGolfers(name='Byeong Hun An', country='KOR', startingRank=52, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Siwoo Kim', country='KOR', startingRank=59, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Russell Knox', country='SCO', startingRank=68, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Thomas Pieters', country='BEL', startingRank=70, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Ross Fisher', country='ENG', startingRank=72, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Shane Lowry', country='IRL', startingRank=74, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=18).one()
newGolfer=PoolGolfers(name='Jason Dufner', country='USA', startingRank=105, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Jhonattan Vegas', country='VEN', startingRank=113, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Lucas Glover', country='USA', startingRank=130, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Chris Kirk', country='USA', startingRank=159, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Martin Kaymer', country='GER', startingRank=163, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Bill Haas', country='USA', startingRank=182, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Martin Laird', country='SCO', startingRank=194, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=11).one()
newGolfer=PoolGolfers(name='Kiradech Aphibarnrat', country='THA', startingRank=37, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Eddie Pepperell', country='ENG', startingRank=38, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Matthew Fitzpatrick', country='ENG', startingRank=40, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Thorbjorn Olesen', country='DEN', startingRank=43, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Emilano Grillo', country='ARG', startingRank=46, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Brendan Grace', country='RSA', startingRank=48, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Aaron Wise', country='USA', startingRank=50, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=15).one()
newGolfer=PoolGolfers(name='Aaron Wise', country='USA', startingRank=50, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Luke List', country='USA', startingRank=56, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Abraham Ancer', country='MEX', startingRank=60, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Chez Reavie', country='USA', startingRank=62, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Dylan Frittelli', country='RSA', startingRank=76, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Peter Uihlein', country='USA', startingRank=78, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Julian Suri', country='USA', startingRank=81, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=8).one()
newGolfer=PoolGolfers(name='Patrick Cantlay', country='USA', startingRank=20, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Tyrell Hatton', country='ENG', startingRank=24, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Hideki Matsuyama', country='JPN', startingRank=25, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Cameron Smith', country='AUS', startingRank=33, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Cameron Champ', country='USA', startingRank=97, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=12).one()
newGolfer=PoolGolfers(name='Daniel Berger', country='USA', startingRank=55, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Pat Perez', country='USA', startingRank=61, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Chesson Hadley', country='USA', startingRank=65, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Kevin Chappell', country='USA', startingRank=71, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Russell Henley', country='USA', startingRank=85, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Beau Hossler', country='USA', startingRank=87, group=newGolferGroup)
session.add(newGolfer)
session.commit()
groups = session.query(PoolGroups)
newGolferGroup = groups.filter_by(id=16).one()
newGolfer=PoolGolfers(name='Andrew Putnam', country='USA', startingRank=73, group=newGolferGroup)
newGolfer=PoolGolfers(name='Charl Schwartzel', country='RSA', startingRank=81, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Kevin Tway', country='USA', startingRank=91, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Danny Lee', country='NZL', startingRank=95, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='J.B. Holmes', country='USA', startingRank=96, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Patton Kizzire', country='USA', startingRank=98, group=newGolferGroup)
session.add(newGolfer)
session.commit()
newGolfer=PoolGolfers(name='Brendan Steele', country='USA', startingRank=103, group=newGolferGroup)
session.add(newGolfer)
session.commit()

# newGroup = PoolGroups(groupname="Group 1")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 2")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 3")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 4")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 5")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 6")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 7")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 8")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 9")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 10")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 11")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 12")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 13")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 14")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 15")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 16")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 17")
# session.add(newGroup)
# session.commit()
# newGroup = PoolGroups(groupname="Group 18")
# session.add(newGroup)
# session.commit()

# newTournament = PoolTournaments(year=2019, name="Sentry Tournament of Champions", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Farmers Insurance Open", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Waste Management Phoenix Open", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="AT&T Pebble Beach National", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Genesis Open", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="WGC Mexico Championship", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="The Honda Championship", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="The Players Championship", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="WGC Match Play Championship", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Masters Tournament", tier=1)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Wells Fargo Championship", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="PGA Championship", tier=1)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="The Memorial Tournament", tier=3)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="US Open", tier=1)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="British Open", tier=1)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="WGC Fed-Ex St Jude Invitational", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Wyndam Championship", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="The Northern Trust", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="BMW Championship", tier=2)
# session.add(newTournament)
# session.commit()
# newTournament = PoolTournaments(year=2019, name="Tour Championship", tier=2)
# session.add(newTournament)
# session.commit()
#
# newUser = PoolUsers(username="admin", password="59543", email="joshbriand@gmail.com")
# session.add(newUser)
# session.commit()

# newUser = PoolUsers(username="admin", password="triple20", email="joshbriand@gmail.com")
# session.add(newUser)
# session.commit()

# newUser = RecipeUsers(name="joshbriand", email="joshbriand@gmail.com", password="joshbriand")
# session.add(newUser)
# session.commit()
# newUser = RecipeUsers(name="seancasey", email="seancasey@gmail.com", password="seancasey")
# session.add(newUser)
# session.commit()
# print "Added users"
#
# newRecipe = Recipes(
#     name="Panko Fish",
#     cuisine="Japanese",
#     meal="Dinner",
#     date=datetime.now(),
#     picture="https://www.takemefishing.org/tmf/assets/images/fish/albacore-464x170.png",
#     user_id=2)
# session.add(newRecipe)
# session.commit()
# recipe_id = session.query(Recipes).filter_by(user_id=2).first().id
# newIngredient = RecipeIngredients(
#     ingredient="3/4 cup Japanese panko breadcrumbs",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="3/4 cup Parmesan cheese finely grated",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="3 tablespoons unsalted butter room temperature",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="3 tablespoons mayonnaise",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="3 green onions, green tops only thinly sliced",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="1 teaspoon Worchestershire sauce",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="1/2 teaspoon Tabasco or other hot pepper sauce",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="1 1/2 tablespoons lemon juice freshly squeezed (approx. 1/2 lemon)",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="salt and pepper to taste",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="4 white fish fillets approx. 6 oz; 1/2 to 3/4 inch thick",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="2 tablespoons fresh flat-leaf parsely finely chopped",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newProcess = RecipeProcess(
#     process="Preheat oven to 400f. Lightly butter a baking dish or individual grain dishes for the fillets.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="n medium bowl, mix together the cheese, breadcrumbs, butter, mayonnaise, green onions, Worcestershire sauce, Tabasco and lemon juice; season to taste with salt and pepper. Set aside until needed.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="Pat the fish fillets completely dry with paper towels (removing the moisture ensures they won't get mushy while baking); season generously with salt and pepper. Arrange the fish in a lightly buttered baking dish or individual gratin dishes.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="Spread about 3 tablespoons of the cheese mixture over each fillet.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="Place in preheated oven and bake until bubbly and almost cooked through, about 10 minutes. Temperature should be approximately 125-130f when tested at thickest part of fillet with meat thermometer.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="Move fillets to broiler for 2 to 3 minutes to brown and crisp the tops. When done, the fish should flake easily with a fork.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="Remove from oven, garnish with fresh parsley and serve immediately.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newRecipe = Recipes(
#     name="Roast Beetroot and Sweet Potato Buddha Bowl with Spicy Tahini Honey Dressing",
#     cuisine="Vegan",
#     meal="Dinner",
#     date=datetime.now(),
#     picture="http://www.thefoodiecorner.gr/wp-content/uploads/2017/03/Roast-Beetroot-and-Sweet-Potato-Buddha-Bowl-with-Spicy-Tahini-Honey-Dressing-www.thefoodiecorner.gr-8-1.jpg",
#     user_id=1)
# session.add(newRecipe)
# session.commit()
# recipe_id = session.query(Recipes).filter_by(user_id=1).first().id
# newIngredient = RecipeIngredients(
#     ingredient="500g sweet potato cubed",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="400g beetroot, cubed",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="4 tbs olive oil", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="1 tsp salt", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="1 cup brown rice", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="6-8 handfuls greens",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="3-4 tbs dried cranberries",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="2-3 tbs sunflower seeds",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="For the dressing:", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="4 tbs tahini", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="2 tbs honey", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="2 tbs olive oil", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="2 tbs water", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="1 tbs orange juice",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="1/4 tsp cinnamon", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="1/4 tsp salt", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(
#     ingredient="1/8 tsp chilli powder",
#     recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newIngredient = RecipeIngredients(ingredient="1/8 tsp cumin", recipe_id=recipe_id)
# session.add(newIngredient)
# session.commit()
# newProcess = RecipeProcess(process="""Preheat oven to 180C fan assisted (200C
# conventional). Line two baking sheets with grease proof paper. Put the sweet
# potato, 2 tablespoons of oil and half a teaspoon of salt in a bowl and mix with
# your hands to coat. Spread it out on a baking sheet (the pieces need to have
# room, no crowding!). Do the same with the beetroot, the other 2 tbs oil and half
#  teaspoon salt. Put both sheets in the oven to roast the veggies. The beetroot
#  should need about 25 minutes till softened and the sweet potato about 30 till
#  softened and starting to brown.""", recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="Boil the rice according to instructions.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(
#     process="To make the dressing whisk all the ingredients in a bowl. If needed warm it up a bit in the microwave to make it runnier.",
#     recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# newProcess = RecipeProcess(process="""Assemble the bowls with a little of each
# vegetable, some rice, a small handful of spinach and rocket, a sprinkling of
# cranberries and sunflower seeds, and a drizzle of dressing. Start modestly with
# the dressing as it's strong tasting, and add more if desired. Serve warm or at
# room temperature.""", recipe_id=recipe_id)
# session.add(newProcess)
# session.commit()
# print "recipes added"


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
