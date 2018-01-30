from flask import (Flask, render_template, request, redirect, jsonify, url_for, flash)
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import (Base, User, Recipe, Comments, Like, Process, Ingredient, ghostUser, ghostGame, ghostComplete)
import random
import string
from datetime import datetime
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import simplejson
import json
import ast
import requests
import psycopg2
import re, hmac


app = Flask(__name__)

APPLICATION_NAME = "Josh Briand's website"

CLIENT_ID = json.loads(
    open('/home/ubuntu/google_client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Recipe Application"

engine = create_engine('sqlite:////var/www/jbv2/jbv2/jb.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# list of cuisines and meals used in app
cuisines = [
    "All", "American", "German", "Indian", "Japanese", "Mexican",
    "Middle Eastern", "Vegan"]
meals = [
    "All", "Appetizer", "Breakfast", "Dessert", "Dinner", "Drink", "Lunch",
    "Salad", "Side", "Snack"]

# code for Regular Expression validation
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")

#start of code for hashing
secret = "guest"

def validate(input, validation):
    return validation.match(input)

def hash_str(s):
    return hmac.new(secret, s).hexdigest()

def make_secure_val(password):
    return "%s" % (hash_str(password))

def check_secure_val(password):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

def make_temp_password(password):
    return make_secure_val(password)

#end of code for hashing

#does user exist?
def userExists(name):
    q = session.query(ghostUser).filter_by(name=name)
    return session.query(q.exists()).scalar()

#does game exist?
def gameExists(name):
    q = session.query(ghostGame).filter_by(id=id)
    return session.query(q.exists()).scalar()

def generateState():
    '''Create anti-forgery state token'''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return state

def generateState():
    '''Create anti-forgery state token'''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return state

@app.route('/', methods=['GET'])
def showIndexPage():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/breweries', methods=['GET'])
def showBreweriesPage():
    '''Handler for brewery web app.'''
    if request.method == 'GET':
        return render_template('breweries.html')





@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''Google Plus Oauth login'''
    if request.args.get('state') != login_session['state']:
        response = make_response(simplejson.dumps('Invalid state parameter.'),
                                 401)
        response.headers['Content-Type'] = 'application/simplejson'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            '/home/ubuntu/google_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            simplejson.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if user_id is None:
        createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    return output


@app.route('/disconnect')
def disconnect():
    '''Log user off of web app'''
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        flash("You have been logged out")
        return redirect(url_for('showRecipes'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('showRecipes'))


@app.route('/recipes/', methods=['GET', 'POST'])
@app.route('/recipes/<int:user_id>', methods=['GET', 'POST'])
def showRecipes(user_id=""):
    '''Handler for landing page of website.  Displays all recipes in database.
    Allows user to filter which recipes are shown and the order they are
    displayed'''
    # Ensure that first list element in cuisines and meals are 'All'
    cuisines[0] = "All"
    meals[0] = "All"
    likeOrder = ""
    users = session.query(User).order_by(User.id)
    if request.method == 'POST':
        # query all recipes
        recipes = session.query(Recipe)
        # get cuisine type for filtering
        cuisine = request.form['cuisine']
        if cuisine != "All":
            # query recipes for specific cuisine type
            recipes = recipes.filter_by(cuisine=cuisine)
        # get meal type for filtering
        meal = request.form['meal']
        if meal != "All":
            # query recipes for specific meal type
            recipes = recipes.filter_by(meal=meal)
        # get user for filtering
        userSelect = request.form['user']
        if userSelect != "All":
            userSelect = int(userSelect)
            # query recipes for specific user/author
            recipes = recipes.filter_by(user_id=userSelect)
        # get order for sorting
        order = request.form['order']
        if order == "Newest":
            # sort from newest first to oldest last
            recipes = recipes.order_by(Recipe.date.desc())
        elif order == "Oldest":
            # sort from oldest to newest
            recipes = recipes.order_by(Recipe.date.asc())
        elif order == "Alphabetically by Name":
            # sort alphabetically by recipe name
            recipes = recipes.order_by(Recipe.name.asc())
        elif order == "Popular":
            # sort by most popular recipe first
            likeOrder = getOrderedLikes()
        return render_template(
            'recipes.html',
            recipes=recipes,
            users=users,
            cuisine=cuisine,
            meal=meal,
            order=order,
            userSelect=userSelect,
            meals=meals,
            cuisines=cuisines,
            likeOrder=likeOrder)
    else:
        state = generateState()
        login_session['state'] = state
        if user_id == "":
            # render if user selects All Recipes or goes to '/recipes'
            # query all recipes to display on webpage
            recipes = session.query(Recipe).order_by(Recipe.date.desc())
            return render_template(
                'recipes.html',
                recipes=recipes,
                users=users,
                meals=meals,
                cuisines=cuisines,
                STATE=state,
                likeOrder=likeOrder)
        else:
            # webpage if user selects My Recipes
            recipes = session.query(Recipe).filter_by(
                user_id=user_id).order_by(
                Recipe.date.desc())
            return render_template(
                'recipes.html',
                recipes=recipes,
                users=users,
                userSelect=user_id,
                meals=meals,
                cuisines=cuisines,
                STATE=state,
                likeOrder=likeOrder)


@app.route('/addrecipe/', methods=['GET', 'POST'])
def addRecipe():
    '''handler for adding a new recipe'''
    # change first list elements of cuisines and meals to 'choose one' from
    # 'all'
    cuisines[0] = "Choose One"
    meals[0] = "Choose One"
    if request.method == 'POST':
        error = ""
        if request.form['cuisine'] == "Choose One":
            # error is user submits a recipe and doesn't choose a cuisine type
            error = "You must choose a cuisine type!"
        elif request.form['meal'] == "Choose One":
            # error is user submits a recipe and doesn't choose a meal type
            error = "You must choose a meal type!"
        cuisine = request.form['cuisine']
        meal = request.form['meal']
        name = request.form['name']
        ingredients = request.form['ingredients']
        '''splits ingredient list into individual elements, not useful in this
        iteration of the web app, but included in case the ability to look up
        recipes by ingredient is introduced in a future version'''
        ingredientList = ingredients.split("\n")
        process = request.form['process']
        processList = process.split("\n")
        picture = request.form['picture']
        if picture == "":
            # generic food image in case user does not include one
            picture = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
        user_id = login_session['user_id']
        date = datetime.now()
        if error != "":
            '''if there is an error, rerender webpage with prefilled out form and
            error message'''
            flash(error)
            return render_template(
                'addrecipe.html',
                name=name,
                ingredients=ingredients,
                process=process,
                picture=picture,
                cuisine=cuisine,
                meal=meal,
                meals=meals,
                cuisines=cuisines)
        # commit new recipe to database
        newRecipe = Recipe(
            name=name,
            cuisine=cuisine,
            meal=meal,
            date=date,
            picture=picture,
            user_id=user_id)
        session.add(newRecipe)
        session.commit()
        recipe_id = session.query(Recipe).filter_by(name=name).one().id
        for ingredient in ingredientList:
            # commit individual ingredients to database
            newIngredient = Ingredient(
                ingredient=ingredient, recipe_id=recipe_id)
            session.add(newIngredient)
            session.commit()
        for process in processList:
            # commit individual method steps to database
            newProcess = Process(process=process, recipe_id=recipe_id)
            session.add(newProcess)
            session.commit()
        # redirect user to newly created recipe webpage and success message
        flash('New Recipe %s Successfully Created' % newRecipe.name)
        return redirect(url_for('showRecipe', recipe_id=recipe_id))
        # return to recipe (no s!)
    else:
        if 'username' not in login_session:
            # redirect to '/' if user not logged in, error message
            flash('User not logged in')
            return redirect('/recipes/')
        else:
            return render_template(
                'addrecipe.html',
                meals=meals,
                cuisines=cuisines)


@app.route('/recipe/<int:recipe_id>/')
def showRecipe(recipe_id):
    '''handler for displaying webpage of an individual recipe'''
    if recipeExists(recipe_id):
        # check to see if recipe id exists
        # query recipe, method, ingredients, likes and comments
        recipe = session.query(Recipe).filter_by(id=recipe_id).one()
        ingredients = session.query(Ingredient).filter_by(
            recipe_id=recipe_id).all()
        processes = session.query(Process).filter_by(recipe_id=recipe_id).all()
        likes = session.query(Like).filter_by(recipe_id=recipe_id).all()
        comments = session.query(Comments).filter_by(
            recipe_id=recipe_id).order_by(
            Comments.id.desc()).all()
        liked = False
        if 'username' in login_session:
            # check to see if user is logged in
            if likes:
                # check to see if likes exist for this recipe
                '''check to see if user already likes to recipe (if so, the
                ability to like is changed to the ability to unlike when webpage
                is rendered)'''
                liked = userLiked(likes)
        state = generateState()
        login_session['state'] = state
        return render_template(
            'recipe.html',
            recipe=recipe,
            ingredients=ingredients,
            processes=processes,
            likes=likes,
            liked=liked,
            meals=meals,
            cuisines=cuisines,
            comments=comments,
            STATE=state)
    # redirect to '/' and flash error message if recipe id does not exist
    flash('Recipe does not exist')
    return redirect('/recipes/')


@app.route('/recipe/<int:recipe_id>/edit/', methods=['GET', 'POST'])
def editRecipe(recipe_id):
    '''handler to edit an existing recipe'''
    # change first list elements of cuisines and meals to 'choose one' from
    # 'all'
    cuisines[0] = "Choose One"
    meals[0] = "Choose One"
    if recipeExists(recipe_id):
        # if recipe if exists in database
        # query author, ingredients and process recipe from database
        author = session.query(Recipe).filter_by(id=recipe_id).one().user
        recipeToEdit = session.query(Recipe).filter_by(id=recipe_id).one()
        oldIngredients = session.query(
            Ingredient).filter_by(recipe_id=recipe_id).all()
        oldProcesses = session.query(Process).filter_by(
            recipe_id=recipe_id).all()
        if 'username' in login_session:
            if author.id == login_session['user_id']:
                # if author and user have the same user id
                # essentially the same process as used in creating a recipe
                if request.method == "POST":
                    error = ""
                    if request.form['cuisine'] == "Choose One":
                        error = "You must choose a cuisine type!"
                    elif request.form['meal'] == "Choose One":
                        error = "You must choose a meal type!"
                    cuisine = request.form['cuisine']
                    meal = request.form['meal']
                    name = request.form['name']
                    ingredients = request.form['ingredients']
                    ingredientList = ingredients.split("\n")
                    process = request.form['process']
                    processList = process.split("\n")
                    picture = request.form['picture']
                    if picture == "":
                        # generic food image in case user does not include one
                        picture = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
                    user_id = login_session['user_id']
                    date = datetime.now()
                    if error != "":
                        flash(error)
                        return render_template(
                            'editrecipe.html',
                            name=name,
                            ingredients=ingredients,
                            process=process,
                            picture=picture,
                            cuisine=cuisine,
                            meal=meal,
                            meals=meals,
                            cuisines=cuisines)
                    recipeToEdit.name = name
                    recipeToEdit.cuisine = cuisine
                    recipeToEdit.meal = meal
                    recipeToEdit.date = date
                    recipeToEdit.picture = picture
                    # update values of recipe to new values
                    session.add(recipeToEdit)
                    session.commit()
                    # delete old ingredients from database
                    for ingredient in oldIngredients:
                        session.delete(ingredient)
                        session.commit()
                    # add new ingredients to database
                    for ingredient in ingredientList:
                        newIngredient = Ingredient(
                            ingredient=ingredient, recipe_id=recipe_id)
                        session.add(newIngredient)
                        session.commit()
                    # delete old process from database
                    for process in oldProcesses:
                        session.delete(process)
                        session.commit()
                    # add new process to database
                    for process in processList:
                        newProcess = Process(
                            process=process, recipe_id=recipe_id)
                        session.add(newProcess)
                        session.commit()
                    flash(
                        'New Recipe %s Successfully Editted' %
                        recipeToEdit.name)
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
                else:
                    ingredientString = ""
                    for ingredient in oldIngredients:
                        ingredientString += ingredient.ingredient + "\n"
                    processString = ""
                    for process in oldProcesses:
                        processString += process.process + "\n"
                    return render_template(
                        'editrecipe.html',
                        recipe=recipeToEdit,
                        ingredientString=ingredientString,
                        processString=processString,
                        meals=meals,
                        cuisines=cuisines)
            else:
                # redirect and error if user id is not equal to author id
                flash('You are not authorized to edit this recipe')
                return redirect(url_for('showRecipe', recipe_id=recipe_id))
        else:
            # redirect and error if user is not logged in
            flash('User not logged in')
            return redirect(url_for('showRecipe', recipe_id=recipe_id))
    else:
        # redirect and error if recipe does not exist
        flash('Recipe does not exist')
    return redirect('/recipes/')


@app.route('/recipe/<int:recipe_id>/delete/', methods=['GET', 'POST'])
def deleteRecipe(recipe_id):
    '''handler to delete existing recipe'''
    if recipeExists(recipe_id):
        # if recipe if exists in database
        '''query author, ingredients, process, comments, likes and recipe from
        database'''
        author = session.query(Recipe).filter_by(id=recipe_id).one().user
        recipeToDelete = session.query(Recipe).filter_by(id=recipe_id).one()
        likesToDelete = session.query(Like).filter_by(recipe_id=recipe_id)
        commentsToDelete = session.query(
            Comments).filter_by(recipe_id=recipe_id)
        ingredientsToDelete = session.query(
            Ingredient).filter_by(recipe_id=recipe_id).all()
        processesToDelete = session.query(Process).filter_by(
            recipe_id=recipe_id).all()
        if 'username' in login_session:
            if author.id == login_session['user_id']:
                if request.method == "POST":
                    if request.form['delete'] == "Yes":
                        '''delete all traces of recipe from database when user
                        confirms deletion'''
                        for processToDelete in processesToDelete:
                            session.delete(processToDelete)
                            session.commit()
                        for likeToDelete in likesToDelete:
                            session.delete(likeToDelete)
                            session.commit()
                        for commentToDelete in commentsToDelete:
                            session.delete(commentToDelete)
                            session.commit()
                        for ingredientToDelete in ingredientsToDelete:
                            session.delete(ingredientToDelete)
                            session.commit()
			session.delete(recipeToDelete)
                        session.commit()
                        flash('Recipe Successfully Deleted')
                        return redirect('/recipes/')
                    else:
                        # redirect to recipe webpage if user cancels action
                        return redirect('/recipe/', recipe_id=recipe_id)
                else:
                    return render_template(
                        'deleterecipe.html', recipe=recipeToDelete)
            else:
                # error message and redirect if user id is not author id
                flash('You are not authorized to delete this recipe')
                return redirect(url_for('showRecipe', recipe_id=recipe_id))
        else:
            # error message and redirect if user is not logged in
            flash('User not logged in')
            return redirect(url_for('showRecipe', recipe_id=recipe_id))
    else:
        # error message and redirect if recipe does not exist
        flash('Recipe does not exist')
        return redirect('/recipes/')


@app.route('/recipe/<int:recipe_id>/like/')
def likeRecipe(recipe_id):
    '''handler to like a recipe'''
    if recipeExists(recipe_id):
        # if recipe id exists in database
        if 'username' in login_session:
            # if user is logged in
            # query likes in database
            likes = session.query(Like).filter_by(recipe_id=recipe_id).all()
            if likes:
                # if likes exists
                if userLiked(likes):
                    # if user liked this recipe already
                    # redirect and error message
                    flash('User has already liked this recipe')
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
            # if user has not liked this recipe already
            # add like to database
            newLike = Like(
                user_id=login_session['user_id'],
                recipe_id=recipe_id)
            session.add(newLike)
            session.commit()
            # redirect and success message
            flash('Recipe liked')
            return redirect(url_for('showRecipe', recipe_id=recipe_id))
        else:
            # redirect and error message if user not logged in
            flash('User not logged in')
            return redirect(url_for('showRecipe', recipe_id=recipe_id))
    else:
        # redirect and error message if recipe id does not exists
        flash('Recipe does not exist')
    return redirect('/recipes/')


@app.route('/recipe/<int:recipe_id>/unlike/')
def unlikeRecipe(recipe_id):
    '''handler for user to unlike a recipe'''
    if recipeExists(recipe_id):
        # if recipe id exists in database
        if 'username' in login_session:
            # if user is logged in
            # query likes from database
            likes = session.query(Like).filter_by(recipe_id=recipe_id).all()
            if likes:
                # if likes exist
                if userLiked(likes):
                    # if user likes recipe
                    # query user's like for recipe and delete
                    likeToDelete = session.query(Like).filter_by(
                        user_id=login_session['user_id'], recipe_id=recipe_id).first()
                    session.delete(likeToDelete)
                    session.commit()
                    # redirect and success message
                    flash('Recipe unliked')
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
                else:
                    # redirect and error message if user has not already liked
                    flash('User does not like this recipe')
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
        else:
            # redirect and error message if user not logged in
            flash('User not logged in')
            return redirect(url_for('showRecipe', recipe_id=recipe_id))
    else:
        # redirect and error message if recipe does not exist
        flash('Recipe does not exist')
    return redirect('/recipes/')


@app.route('/recipe/<int:recipe_id>/addcomment/', methods=['GET', 'POST'])
def addComment(recipe_id):
    '''handler for user to add comment to recipe'''
    if recipeExists(recipe_id):
        # recipe exists in database
        if request.method == 'POST':
            if 'username' in login_session:
                # if user if logged in
                # get comment from form

                comment = request.form['comment']
                if comment == "":
                        # error and redirect if no comment is entered
                    flash('You must enter a comment in order to submit one')
                    return render_template('addcomment.html')
                else:
                    # commit comment to database
                    date = datetime.now()
                    newComment = Comments(
                        comment=comment,
                        recipe_id=recipe_id,
                        user_id=login_session['user_id'],
                        date=date)
                    session.add(newComment)
                    session.commit()
                    # redirect and success message
                    flash('Comment has been added')
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
            else:
                # redirect and error message if user not logged in
                flash('User must be logged in to comment')
                return render_template('addcomment.html')
        else:
            return render_template('addcomment.html')
    else:
        # redirect and error message if recipe does not exist
        flash('Recipe does not exist')
        return redirect('/recipes/')


@app.route(
    '/recipe/<int:recipe_id>/editcomment/<int:comment_id>/',
    methods=[
        'GET',
        'POST'])
def editComment(recipe_id, comment_id):
    '''handler to edit comment'''
    if recipeExists(recipe_id):
        # recipe exists in database
        if commentExists(comment_id):
            # comment exists in database
            # query comment
            commentToEdit = session.query(
                Comments).filter_by(id=comment_id).one()
            if request.method == 'POST':
                # query author id
                author = session.query(Comments).filter_by(
                    id=comment_id).one().user
                if 'username' in login_session:
                    # user is logged in
                    editComment = request.form['comment']
                    if author.id == login_session['user_id']:
                        # user id is the same as author id
                        if editComment == "":
                            # redirect and error message if comment is empty
                            flash('You must enter a comment in order to submit one')
                            return render_template(
                                'editcomment.html', comment=commentToEdit)
                        else:
                            # commit editted comment to database
                            commentToEdit.comment = editComment
                            date = datetime.now()
                            commentToEdit.date = date
                            session.add(commentToEdit)
                            session.commit()
                            # redirect and success message
                            flash('Comment has been editted')
                            return redirect(
                                url_for(
                                    'showRecipe',
                                    recipe_id=recipe_id))
                    else:
                        # redirect and error message if user is not author
                        flash('You are not authorized to edit this comment')
                        return redirect(
                            url_for(
                                'showRecipe',
                                recipe_id=recipe_id))
                else:
                    # redirect and error message if user not logged in
                    flash('User not logged in')
                    return render_template('addcomment.html')
            else:
                return render_template(
                    'editcomment.html', comment=commentToEdit)
        else:
            # error message and redirect if comment does not exist
            flash('Comment does not exist')
            return render_template('addcomment.html')
    else:
        # redirect and error message if recipe does not exist
        flash('Recipe does not exist')
        return redirect('/recipes/')


@app.route(
    '/recipe/<int:recipe_id>/deletecomment/<int:comment_id>/',
    methods=[
        'GET',
        'POST'])
def deleteComment(recipe_id, comment_id):
    '''handler to delete comment'''
    if recipeExists(recipe_id):
        # recipe exists in database
        if commentExists(comment_id):
            # comment exists in database
            # query author and comment
            author = session.query(Comments).filter_by(
                id=comment_id).one().user
            commentToDelete = session.query(
                Comments).filter_by(id=comment_id).one()
            if 'username' in login_session:
                # user is logged in
                if author.id == login_session['user_id']:
                    # user id is the same as author id
                    if request.method == "POST":
                        if request.form['delete'] == "Yes":
                            # user confirm deletion
                            # delete comment from database
                            session.delete(commentToDelete)
                            session.commit()
                            # redirect and success message
                            flash('Comment Successfully Deleted')
                            return redirect(
                                url_for(
                                    'showRecipe',
                                    recipe_id=recipe_id))
                        else:
                            # user cancels deletion
                            return redirect(
                                url_for(
                                    'showRecipe',
                                    recipe_id=recipe_id))
                    else:
                        return render_template('deletecomment.html')
                else:
                    # error message and redirect if user is not author
                    flash('You are not authorized to delete this comment')
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
            else:
                # error message and redirect if user is not logged in
                flash('User not logged in')
                return redirect(url_for('showRecipe', recipe_id=recipe_id))
        else:
            # error message and redirect if comment does not exist
            flash('Comment does not exist')
            return redirect('/recipes/')
    else:
        # redirect and error message if recipe does not exist
        flash('Recipe does not exist')
        return redirect('/recipes/')


@app.route('/recipes/JSON/')
@app.route('/recipes/json/')
def recipesJSON():
    '''JSON API to view overview of all recipes'''
    recipes = session.query(Recipe).all()
    return jsonify(recipes=[i.serialize for i in recipes])


# JSON APIs to view Restaurant Information
@app.route('/recipe/<int:recipe_id>/JSON/')
@app.route('/recipe/<int:recipe_id>/json/')
def recipeJSON(recipe_id):
    '''JSON API to view detail of a recipe'''
    recipe = session.query(Recipe).filter_by(id=recipe_id).all()
    ingredients = session.query(Ingredient).filter_by(
        recipe_id=recipe_id).all()
    processes = session.query(Process).filter_by(recipe_id=recipe_id).all()
    return jsonify(
        recipe=[
            i.serialize for i in recipe], ingredients=[
            i.serialize for i in ingredients], processes=[
                i.serialize for i in processes])


@app.route('/ghosts/', methods=['GET', 'POST'])
@app.route('/ghosts/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form['login'] == "Log In":
            login_username = request.form['username']
            login_password = request.form['password']
            if login_username:
                if login_password:
                    users = session.query(ghostUser)
                    user = users.filter_by(name=login_username).first()
                    login_hashed_password = make_secure_val(login_password)
                    if userExists(login_username):
                        if user.name == login_password:
                            login_session['username'] = login_username
                            return redirect(url_for('changepassword'))
                        elif user.password == login_hashed_password:
                            login_session['username'] = login_username
                            return redirect(url_for('menu'))
                        else:
                            flash('Incorrect Password')
                            return render_template('login.html')
                    else:
                        flash('Username Not Found')
                        return render_template('login.html')
                else:
                    flash('No Password Entered')
                    return render_template('login.html')
            elif login_password:
                flash('No Username Entered')
                return render_template('login.html')
        elif request.form['login'] == "Create User":
            new_username = request.form['newUsername']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            new_email = request.form['newEmail']
            new_hashed_password = make_secure_val(new_password)
            if new_username:
                if userExists(new_username):
                    flash('Username Already Exists')
                    return render_template('login.html')
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('login.html')
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('login.html')
                        elif new_email:
                            #TODO
                            #RE email
                            newUser = ghostUser(name=new_username,
                                        password=new_hashed_password,
                                        email=new_email,
                                        notifications="n")
                            session.add(newUser)
                            session.commit()
                            login_session['username'] = new_username
                            return redirect(url_for('menu'))
                        else:
                            newUser = ghostUser(name=new_username,
                                        password=new_hashed_password,
                                        email="none",
                                        notifications="n")
                            session.add(newUser)
                            session.commit()
                            login_session['username'] = new_username
                            return redirect(url_for('menu'))
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('login.html')

            else:
                flash('No Username Entered')
                return render_template('login.html')

@app.route('/ghosts/logout/')
def logout():
    login_session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/ghosts/changepassword/', methods=['GET', 'POST'])
def changepassword():
    if 'username' in login_session:
        users = session.query(ghostUser)
        users = users.order_by(ghostUser.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        if request.method == 'GET':
            flash('Please Change Your Password')
            return render_template('changepassword.html',
                                    playerUsername=login_session['username'],
                                    userid=user.id)
        elif request.method == 'POST':
            if "changePassword" in request.form:
                print "database " + user.password
                current_password = request.form['currentPassword']
                print "current " + current_password
                new_password = request.form['newPassword']
                print "new " + new_password
                confirm_password = request.form['confirmPassword']
                current_hashed_password = make_secure_val(current_password)
                new_hashed_password = make_secure_val(new_password)
                print "new hashed " + new_hashed_password
                if current_hashed_password == user.password or current_password == user.password:
                    if new_password != current_password:
                        if new_password == confirm_password:
                            user.password = new_hashed_password
                            session.add(user)
                            session.commit()
                            flash('Password Successfully Changed')
                            return redirect(url_for('menu'))
                        else:
                            flash('Passwords Do Not Match')
                            return redirect(url_for('changepassword'))
                    else:
                        flash('New Password Must Be Different Than Current Password')
                        return redirect(url_for('changepassword'))
                else:
                    flash('Incorrect Current Password')
                    return redirect(url_for('changepassword'))
    else:
        flash('Please log in')
        return render_template('login.html')



@app.route('/ghosts/menu/', methods=['GET', 'POST'])
def menu():
    if 'username' in login_session:
        users = session.query(ghostUser)
        users = users.order_by(ghostUser.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        userNotification = user.notifications
        userGames = session.query(ghostGame).filter((ghostGame.player1id==user.id) | (ghostGame.player2id==user.id))
        userGames = userGames.order_by(ghostGame.id.asc())
        userCompleted = session.query(ghostComplete).filter((ghostComplete.player1id==user.id) | (ghostComplete.player2id==user.id)).all()
        userWins = session.query(ghostComplete).filter(ghostComplete.winnerid==user.id).all()
        blueWins = 0
        yellowWins = 0
        exitWins = 0
        for win in userWins:
            if win.won == 'blue':
                blueWins += 1
            elif win.won == 'yellow':
                yellowWins += 1
            elif win.won == 'exit':
                exitWins += 1
        if request.method == 'GET':
            return render_template('menu.html',
                                    playerUsername=login_session['username'],
                                    userid=user.id,
                                    users=users,
                                    userNotification=userNotification,
                                    userGames=userGames,
                                    userCompleted=userCompleted,
                                    userWins=userWins,
                                    blueWins=blueWins,
                                    yellowWins=yellowWins,
                                    exitWins=exitWins)
        elif request.method == 'POST':
            if "notifications" in request.form:
                notifications = request.form['notifications']
                print "-->" + notifications
                if notifications == 'on':
                    user.notifications = 'on'
                else:
                    user.notifications = 'no'
                session.add(user)
                session.commit()
                flash('Email Notifications Updated')
                return redirect(url_for('menu'))
            elif "changePassword" in request.form:
                current_password = request.form['currentPassword']
                new_password = request.form['newPassword']
                confirm_password = request.form['confirmPassword']
                current_hashed_password = make_secure_val(current_password)
                new_hashed_password = make_secure_val(new_password)
                if current_hashed_password == user.password:
                    if new_password != current_password:
                        if new_password == confirm_password:
                            user.password = new_hashed_password
                            session.add(user)
                            session.commit()
                            flash('Password Successfully Changed')
                            return redirect(url_for('menu'))
                        else:
                            flash('Passwords Do Not Match')
                            return redirect(url_for('menu'))
                    else:
                        flash('New Password Must Be Different Than Current Password')
                        return redirect(url_for('menu'))
                else:
                    flash('Incorrect Current Password')
                    return redirect(url_for('menu'))
            elif "startExistingGame" in request.form:
                game_id = request.form['existingGame']
                #add authentication here
                return redirect(url_for('game', game_id=game_id))
            elif "startGame" in request.form:
                opponent = request.form['opponent']
                date = datetime.now()
                new_game = ghostGame(player1id=user.id,
                    player2id=opponent,
                    date=date,
                    b11 = '',
                    b21 = '',
                    b31 = '',
                    b41 = '',
                    b51 = '',
                    b61 = '',
                    b12 = '',
                    b22 = '',
                    b32 = '',
                    b42 = '',
                    b52 = '',
                    b62 = '',
                    b13 = '',
                    b23 = '',
                    b33 = '',
                    b43 = '',
                    b53 = '',
                    b63 = '',
                    b14 = '',
                    b24 = '',
                    b34 = '',
                    b44 = '',
                    b54 = '',
                    b64 = '',
                    b15 = '',
                    b25 = '',
                    b35 = '',
                    b45 = '',
                    b55 = '',
                    b65 = '',
                    b16 = '',
                    b26 = '',
                    b36 = '',
                    b46 = '',
                    b56 = '',
                    b66 = '',
                    previousGhost='none',
                    previousPlayer=0
                )
                session.add(new_game)
                session.commit()
                game_id = session.query(ghostGame).filter_by(date=date).one().id
                return redirect(url_for('game', game_id=game_id))
    else:
        flash('Please log in')
        return redirect(url_for('login'))



@app.route('/ghosts/game/<int:game_id>/', methods=['GET', 'POST'])
def game(game_id):
    ghostList = ['p1b3','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b3','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
    deadGhosts = ['p1b3','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b3','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
    locationList = ['b11','b21','b31','b41','b51','b61','b22','b22','b32','b42','b52','b62','b13','b23','b33','b43','b53','b63','b14','b24','b34','b44','b54','b64','b15','b25','b35','b45','b55','b65','b16','b26','b36','b46','b56','b66']
    if 'username' in login_session:
        users = session.query(ghostUser)
        users = users.order_by(ghostUser.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        userid = user.id
        userNotification = user.notifications
        game = session.query(ghostGame).filter(ghostGame.id==game_id).one()
        print "previous player " + str(game.previousPlayer)
        if user.id == game.player1id:
            opponent = users.filter_by(id=game.player2id).one()
            opponentPlayer = 2
            startingVal = 20
            opponentStartingVal = 10
            userPlayer = 1
        elif user.id == game.player2id:
            opponent = users.filter_by(id=game.player1id).one()
            opponentPlayer = 1
            startingVal = 10
            opponentStartingVal = 20
            userPlayer = 2
        else:
            flash('You Are Not Part Of This Game')
            return redirect(url_for('menu'))
        for ghost in ghostList:
            if ghost == game.b11:
                deadGhosts.remove(ghost)
            elif ghost == game.b21:
                deadGhosts.remove(ghost)
            elif ghost == game.b31:
                deadGhosts.remove(ghost)
            elif ghost == game.b41:
                deadGhosts.remove(ghost)
            elif ghost == game.b51:
                deadGhosts.remove(ghost)
            elif ghost == game.b61:
                deadGhosts.remove(ghost)
            elif ghost == game.b12:
                deadGhosts.remove(ghost)
            elif ghost == game.b22:
                deadGhosts.remove(ghost)
            elif ghost == game.b32:
                deadGhosts.remove(ghost)
            elif ghost == game.b42:
                deadGhosts.remove(ghost)
            elif ghost == game.b52:
                deadGhosts.remove(ghost)
            elif ghost == game.b62:
                deadGhosts.remove(ghost)
            elif ghost == game.b13:
                deadGhosts.remove(ghost)
            elif ghost == game.b23:
                deadGhosts.remove(ghost)
            elif ghost == game.b33:
                deadGhosts.remove(ghost)
            elif ghost == game.b43:
                deadGhosts.remove(ghost)
            elif ghost == game.b53:
                deadGhosts.remove(ghost)
            elif ghost == game.b63:
                deadGhosts.remove(ghost)
            elif ghost == game.b14:
                deadGhosts.remove(ghost)
            elif ghost == game.b24:
                deadGhosts.remove(ghost)
            elif ghost == game.b34:
                deadGhosts.remove(ghost)
            elif ghost == game.b44:
                deadGhosts.remove(ghost)
            elif ghost == game.b54:
                deadGhosts.remove(ghost)
            elif ghost == game.b64:
                deadGhosts.remove(ghost)
            elif ghost == game.b15:
                deadGhosts.remove(ghost)
            elif ghost == game.b25:
                deadGhosts.remove(ghost)
            elif ghost == game.b35:
                deadGhosts.remove(ghost)
            elif ghost == game.b45:
                deadGhosts.remove(ghost)
            elif ghost == game.b55:
                deadGhosts.remove(ghost)
            elif ghost == game.b65:
                deadGhosts.remove(ghost)
            elif ghost == game.b16:
                deadGhosts.remove(ghost)
            elif ghost == game.b26:
                deadGhosts.remove(ghost)
            elif ghost == game.b36:
                deadGhosts.remove(ghost)
            elif ghost == game.b46:
                deadGhosts.remove(ghost)
            elif ghost == game.b56:
                deadGhosts.remove(ghost)
            elif ghost == game.b66:
                deadGhosts.remove(ghost)
        userDeadBlue = 0
        userDeadYellow = 0
        opponentDeadBlue = 0
        opponentDeadYellow = 0
        for ghost in deadGhosts:
            if ghost[1] == str(userPlayer) and ghost[2] == 'b':
                userDeadBlue +=1
            elif ghost[1] == str(userPlayer) and ghost[2] == 'y':
                userDeadYellow +=1
            elif ghost[1] == str(opponentPlayer) and ghost[2] == 'b':
                opponentDeadBlue +=1
            elif ghost[1] == str(opponentPlayer) and ghost[2] == 'y':
                opponentDeadYellow +=1
        if game.previousPlayer == 0 or game.previousPlayer > 2:
            winner = ''
            wonBy = ''
        else:
            if userDeadYellow == 4:
                wonBy = "yellow"
                winner = userPlayer
            elif userDeadBlue == 4:
                wonBy = "blue"
                winner = opponentPlayer
            elif opponentDeadYellow == 4:
                wonBy = "yellow"
                winner = opponentPlayer
            elif userDeadBlue == 4:
                wonBy = "blue"
                winner = opponentPlayer
            elif (game.b11[1:2] == "1b" or game.b61[1:3] == "1b") and game.previousPlayer == 2:
                wonBy = "exit"
                winner = 1
            elif (game.b16[1:2] == "2b" or game.b66[1:3] == "2b") and game.previousPlayer == 1:
                wonBy = "exit"
                winner = 2
            else:
                winner = ''
                wonBy = ''
        if request.method == 'GET':
            if game.previousPlayer == userPlayer or game.previousPlayer == userPlayer * 10:
                flash("Waiting for Opponent's Move, Please Check Back Later")
            return render_template('board.html',
                                    playerUsername=login_session['username'],
                                    userid=user.id,
                                    users=users,
                                    userNotification=userNotification,
                                    game=game,
                                    userPlayer=userPlayer,
                                    startingVal=startingVal,
                                    opponentStartingVal=opponentStartingVal,
                                    opponent=opponent,
                                    deadGhosts=deadGhosts,
                                    winner=winner,
                                    wonBy=wonBy)
        elif request.method == 'POST':
            rawMoves = request.form['moves']
            #ghost : location
            moveDict = ast.literal_eval(rawMoves)
            dead = request.form['dead']
            originalLocation = request.form['originalLocation']
            moveID = request.form['playerID']
            moveDirection = request.form['moveDirection']
            if str(game.b11).startswith('l'):
                game.b11 = ''
            elif game.b12[0] == 'l':
                game.b12 = ''
            elif str(game.b13).startswith('l'):
                game.b13 = ''
            elif game.b14[0] == 'l':
                game.b14 = ''
            elif game.b15[0] == 'l':
                game.b15 = ''
            elif game.b16[0] == 'l':
                game.b16 = ''
            elif game.b21[0] == 'l':
                game.b21 = ''
            elif game.b22[0] == 'l':
                game.b22 = ''
            elif game.b23[0] == 'l':
                game.b23 = ''
            elif game.b24[0] == 'l':
                game.b24 = ''
            elif game.b25[0] == 'l':
                game.b25 = ''
            elif game.b26[0] == 'l':
                game.b26 = ''
            elif game.b31[0] == 'l':
                game.b31 = ''
            elif game.b32[0] == 'l':
                game.b32 = ''
            elif game.b33[0] == 'l':
                game.b33 = ''
            elif game.b34[0] == 'l':
                game.b34 = ''
            elif game.b35[0] == 'l':
                game.b35 = ''
            elif game.b36[0] == 'l':
                game.b36 = ''
            elif game.b41[0] == 'l':
                game.b41 = ''
            elif game.b42[0] == 'l':
                game.b42 = ''
            elif game.b43[0] == 'l':
                game.b43 = ''
            elif game.b44[0] == 'l':
                game.b44 = ''
            elif game.b45[0] == 'l':
                game.b45 = ''
            elif game.b46[0] == 'l':
                game.b46 = ''
            elif game.b51[0] == 'l':
                game.b51 = ''
            elif game.b52[0] == 'l':
                game.b52 = ''
            elif game.b53[0] == 'l':
                game.b53 = ''
            elif game.b54[0] == 'l':
                game.b54 = ''
            elif game.b55[0] == 'l':
                game.b55 = ''
            elif game.b56[0] == 'l':
                game.b56 = ''
            elif game.b61[0] == 'l':
                game.b61 = ''
            elif game.b62[0] == 'l':
                game.b62 = ''
            elif game.b63[0] == 'l':
                game.b63 = ''
            elif game.b64[0] == 'l':
                game.b64 = ''
            elif game.b65[0] == 'l':
                game.b65 = ''
            elif game.b66[0] == 'l':
                game.b66 = ''
            if moveID == str(userid):
                for move in moveDict:
                    if game.previousPlayer == 1 or game.previousPlayer == 2:
                        tempDirection = 'last-' + moveDirection
                        exec("game.%s = '%s'") % (originalLocation, tempDirection)
                    exec("game.%s = move" % (moveDict[move]))
                    game.previousGhost = move
                game.date = datetime.now()
                if game.previousPlayer == 1:
                    game.previousPlayer = 2
                elif game.previousPlayer == 2:
                    game.previousPlayer = 1
                else:
                    game.previousPlayer = game.previousPlayer + userPlayer*10
                    if game.previousPlayer == 30:
                        game.previousPlayer = 2
                session.add(game)
                session.commit()
                if game.previousPlayer == userPlayer or game.previousPlayer == userPlayer * 10:
                    flash("Waiting for Opponent's Move, Please Check Back Later")
                return render_template('board.html',
                                        playerUsername=login_session['username'],
                                        userid=user.id,
                                        users=users,
                                        userNotification=userNotification,
                                        game=game,
                                        userPlayer=userPlayer,
                                        startingVal=startingVal,
                                        opponentStartingVal=opponentStartingVal,
                                        opponent=opponent,
                                        deadGhosts=deadGhosts,
                                        winner=winner,
                                        wonBy=wonBy)
            else:
                flash('ID Match Error, Please Try Again')
                return redirect(url_for('game', game_id=game_id))
    else:
        flash('Please log in')
        return redirect(url_for('login'))



'''
@app.route('/survey/logout/')

@app.route('/survey/')

@app.route('/survey/takepoll/')

@app.route('/survery/edit/')

@app.route('/survery/addquestion/')

@app.route('/survery/deletequestion/')

@app.route('/survery/adduser/')

@app.route('/survery/deleteuser/')

@app.route('/survey/changepassword/')
'''

def recipeExists(recipe_id):
    '''function to check if recipe exists in database'''
    q = session.query(Recipe).filter_by(id=recipe_id)
    return session.query(q.exists()).scalar()


def commentExists(comment_id):
    '''function to check if comment exists in database'''
    q = session.query(Comments).filter_by(id=comment_id)
    return session.query(q.exists()).scalar()


def userLiked(likes):
    '''function to check if user has liked recipe already'''
    for like in likes:
        if login_session['user_id'] == like.user_id:
            return True
    return False


def getOrderedLikes():
    '''function to order recipes based on how many likes each one has'''
    likeDict = {}
    recipes = session.query(Recipe)
    for recipe in recipes:
        likeDict[recipe.id] = 0
    likes = session.query(Like)
    for like in likes:
        likeDict[like.recipe_id] += 1
    likeList = sorted(likeDict, key=lambda k: likeDict[k], reverse=True)
    return likeList


def createUser(login_session):
    '''function to create a new user to database if user's email does not exist
    in the user table'''
    newUser = User(
        name=login_session['username'],
        email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    users = session.query(User).all()
    return user.id


def getUserID(email):
    '''function to look up and return user id from database'''
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except BaseException:
        return None



if __name__ == '__main__':
    app.secret_key = "Don't panic!"
    app.debug = True
    app.run()
