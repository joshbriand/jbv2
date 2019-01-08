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

newTournament = PoolTournaments(year=2019, name="Sentry Tournament of Champions", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Farmers Insurance Open", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Waste Management Phoenix Open", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="AT&T Pebble Beach National", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Genesis Open", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="WGC Mexico Championship", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="The Honda Championship", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="The Players Championship", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="WGC Match Play Championship", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Masters Tournament", tier=1)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Wells Fargo Championship", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="PGA Championship", tier=1)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="The Memorial Tournament", tier=3)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="US Open", tier=1)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="British Open", tier=1)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="WGC Fed-Ex St Jude Invitational", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Wyndam Championship", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="The Northern Trust", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="BMW Championship", tier=2)
session.add(newTournament)
session.commit()
newTournament = PoolTournaments(year=2019, name="Tour Championship", tier=2)
session.add(newTournament)
session.commit()

print "bingo!!"

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
