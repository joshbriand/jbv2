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
    session = DBSession()
    users = session.query(User).order_by(User.id)
    DBSession.remove()
    if request.method == 'POST':
        # query all recipes
        session = DBSession()
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
        DBSession.remove()
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
        for user_login in login_session:
            print user_login
        if user_id == "":
            # render if user selects All Recipes or goes to '/recipes'
            # query all recipes to display on webpage
            session = DBSession()
            recipes = session.query(Recipe).order_by(Recipe.date.desc())
            DBSession.remove()
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
            session = DBSession()
            recipes = session.query(Recipe).filter_by(
                user_id=user_id).order_by(
                Recipe.date.desc())
            DBSession.remove()
            return render_template(
                'recipes.html',
                recipes=recipes,
                users=users,
                userSelect=user_id,
                meals=meals,
                cuisines=cuisines,
                STATE=state,
                likeOrder=likeOrder)

@app.route('/recipe/<int:recipe_id>/')
def showRecipe(recipe_id):
    '''handler for displaying webpage of an individual recipe'''
    if recipeExists(recipe_id):
        # check to see if recipe id exists
        # query recipe, method, ingredients, likes and comments
        sessioon = DBSession()
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
        DBSession.remove()
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
        session = DBSession()
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
        DBSession.remove()
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
        session = DBSession()
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
                        DBSession.remove()
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
                    DBSession.remove()
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
                else:
                    ingredientString = ""
                    for ingredient in oldIngredients:
                        ingredientString += ingredient.ingredient + "\n"
                    processString = ""
                    for process in oldProcesses:
                        processString += process.process + "\n"
                    DBSession.remove()
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
        session = DBSession()
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
                        DBSession.remove()
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
            session = DBSession()
            likes = session.query(Like).filter_by(recipe_id=recipe_id).all()
            if likes:
                # if likes exists
                if userLiked(likes):
                    # if user liked this recipe already
                    # redirect and error message
                    flash('User has already liked this recipe')
                    DBSession.remove()
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
            DBSession.remove()
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
            session = DBSession()
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
                    DBSession.remove()
                    return redirect(url_for('showRecipe', recipe_id=recipe_id))
                else:
                    # redirect and error message if user has not already liked
                    flash('User does not like this recipe')
                    DBSession.remove()
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
                    session = DBSession()
                    newComment = Comments(
                        comment=comment,
                        recipe_id=recipe_id,
                        user_id=login_session['user_id'],
                        date=date)
                    session.add(newComment)
                    session.commit()
                    # redirect and success message
                    flash('Comment has been added')
                    DBSession.remove()
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
    methods=['GET','POST'])
def editComment(recipe_id, comment_id):
    '''handler to edit comment'''
    if recipeExists(recipe_id):
        # recipe exists in database
        if commentExists(comment_id):
            # comment exists in database
            # query comment
            session = DBSession()
            commentToEdit = session.query(
                Comments).filter_by(id=comment_id).one()
            DBSession.remove()
            if request.method == 'POST':
                # query author id
                session = DBSession()
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
                            DBSession.remove()
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
                            DBSession.remove()
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
            session = DBSession()
            author = session.query(Comments).filter_by(
                id=comment_id).one().user
            commentToDelete = session.query(
                Comments).filter_by(id=comment_id).one()
            DBSession.remove()
            if 'username' in login_session:
                # user is logged in
                if author.id == login_session['user_id']:
                    # user id is the same as author id
                    if request.method == "POST":
                        if request.form['delete'] == "Yes":
                            # user confirm deletion
                            # delete comment from database
                            session = DBSession()
                            session.delete(commentToDelete)
                            session.commit()
                            # redirect and success message
                            flash('Comment Successfully Deleted')
                            DBSession.remove()
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
    session = DBSession()
    recipes = session.query(Recipe).all()
    DBSession.remove()
    return jsonify(recipes=[i.serialize for i in recipes])

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
