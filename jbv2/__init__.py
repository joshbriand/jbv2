from flask import (Flask, render_template, request, redirect, jsonify, url_for, flash)
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database_setup import (Base, RecipeUsers, Recipes, RecipeComments, RecipeLikes, RecipeProcess, RecipeIngredients, ghostUser, ghostGame, ghostComplete, SurveyUsers, SurveyResults, SurveyQuestions, PoolUsers, PoolGolfers, PoolGroups, PoolChoices, PoolTournaments, PoolResults)
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
import re, hmac
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

APPLICATION_NAME = "Josh Briand's website"

CLIENT_ID = json.loads(
    open('var/www/jbv2/jbv2/google_client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Recipe Application"

'''engine = create_engine('sqlite:///jb.db')'''
engine = create_engine('sqlite:////var/www/jbv2/jbv2/jb.db')

Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
#session = DBSession()

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
    session = DBSession()
    q = session.query(ghostUser).filter_by(name=name)
    exists = session.query(q.exists()).scalar()
    DBSession.remove()
    return exists

def surveyUserExists(name):
    session = DBSession()
    z = session.query(SurveyUsers).filter_by(username=name)
    DBSession.remove()
    return session.query(z.exists()).scalar()

def poolUserExists(name):
    session = DBSession()
    z = session.query(PoolUsers).filter_by(username=name)
    DBSession.remove()
    return session.query(z.exists()).scalar()

def poolGolferExists(name):
    session = DBSession()
    z = session.query(PoolGolfers).filter_by(name=name)
    DBSession.remove()
    return session.query(z.exists()).scalar()

def poolRankExists(rank):
    session = DBSession()
    z = session.query(PoolGolfers).filter_by(startingRank=rank)
    DBSession.remove()
    return session.query(z.exists()).scalar()

def recipeUserExists(name):
    session = DBSession()
    z = session.query(RecipeUsers).filter_by(name=name)
    DBSession.remove()
    return session.query(z.exists()).scalar()

def recipeExists(recipe_id):
    '''function to check if recipe exists in database'''
    session = DBSession()
    q = session.query(Recipes).filter_by(id=recipe_id)
    DBSession.remove()
    return session.query(q.exists()).scalar()


def commentExists(comment_id):
    '''function to check if comment exists in database'''
    session = DBSession()
    q = session.query(RecipeComments).filter_by(id=comment_id)
    DBSession.remove()
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
    session = DBSession()
    recipes = session.query(Recipes)
    for recipe in recipes:
        likeDict[recipe.id] = 0
    likes = session.query(RecipeLikes)
    for like in likes:
        likeDict[like.recipe_id] += 1
    likeList = sorted(likeDict, key=lambda k: likeDict[k], reverse=True)
    DBSession.remove()
    return likeList

#does game exist?
def gameExists(name):
    session = DBSession()
    q = session.query(ghostGame).filter_by(id=id)
    exists = session.query(q.exists()).scalar()
    DBSession.remove()
    return exists

def calculate_rank(vector):
    a = {}
    rank = 1
    print sorted(vector, reverse = True)
    for num in sorted(vector, reverse = True):
        if num not in a:
            a[num] = rank
            rank = rank + sorted(vector, reverse = True).count(num)
    results = [a[i] for i in vector]
    resultsFinal = results[:]
    for i in range(0, len(results) - 1):
        if results.count(results[i]) > 1:
            resultsFinal[i] = "T" + str(results[i])
        else:
            resultsFinal[i] = str(results[i])
    return resultsFinal

def calculate_golfer_rank(vector):
    points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for tournament in vector:
        for i in range(0, len(tournament) - 1):
            points[i] += tournament[i]
    a = {}
    rank = 1
    for num in sorted(points, reverse = True):
        if num not in a:
            a[num] = rank
            rank = rank + sorted(points, reverse = True).count(num)
    results = [a[i] for i in points]
    resultsFinal = results[:]
    for i in range(0, len(results) - 1):
        if results.count(results[i]) > 1:
            resultsFinal[i] = "T" + str(results[i])
        else:
            resultsFinal[i] = str(results[i])
    return resultsFinal

@app.route('/', methods=['GET'])
def showIndexPage():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/merch', methods=['GET'])
@app.route('/settlement', methods=['GET'])
def showMerchandiseSettlement():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('settlement.html')

@app.route('/cash', methods=['GET'])
def showCashCounter():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('cash.html')

@app.route('/breweries', methods=['GET'])
def showBreweriesPage():
    '''Handler for brewery web app.'''
    if request.method == 'GET':
        return render_template('breweries.html')

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
                    session = DBSession()
                    users = session.query(ghostUser)
                    user = users.filter_by(name=login_username).first()
                    login_hashed_password = make_secure_val(login_password)
                    DBSession.remove()
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
                            session = DBSession()
                            newUser = ghostUser(name=new_username,
                                        password=new_hashed_password,
                                        email=new_email,
                                        notifications="n")
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
                            login_session['username'] = new_username
                            return redirect(url_for('menu'))
                        else:
                            session = DBSession()
                            newUser = ghostUser(name=new_username,
                                        password=new_hashed_password,
                                        email="none",
                                        notifications="n")
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
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
    session = DBSession()
    login_session.pop('username', None)
    DBSession.remove()
    return redirect(url_for('login'))

@app.route('/ghosts/changepassword/', methods=['GET', 'POST'])
def changepassword():
    if 'username' in login_session:
        session = DBSession()
        users = session.query(ghostUser)
        users = users.order_by(ghostUser.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        DBSession.remove()
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
                            session = DBSession()
                            session.add(user)
                            session.commit()
                            DBSession.remove()
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
        session = DBSession()
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
            DBSession.remove()
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
                DBSession.remove()
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
                            DBSession.remove()
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
                DBSession.remove()
                return redirect(url_for('game', game_id=game_id))
    else:
        flash('Please log in')
        return redirect(url_for('login'))

@app.route('/ghosts/game/<int:game_id>/', methods=['GET', 'POST'])
def game(game_id):
    if 'username' in login_session:
        session = DBSession()
        users = session.query(ghostUser)
        users = users.order_by(ghostUser.name.asc())
        user = users.filter_by(name=login_session['username']).one()
        userid = user.id
        userNotification = user.notifications
        game = session.query(ghostGame).filter(ghostGame.id==game_id).one()
        print "previous player " + str(game.previousPlayer)
        if user.id == game.player1id:
            opponent = users.filter_by(id=game.player2id).one()
            opponentid = opponent.id
            opponentPlayer = 2
            startingVal = 20
            opponentStartingVal = 10
            userPlayer = 1
        elif user.id == game.player2id:
            opponent = users.filter_by(id=game.player1id).one()
            opponentid = opponent.id
            opponentPlayer = 1
            startingVal = 10
            opponentStartingVal = 20
            userPlayer = 2
        else:
            flash('You Are Not Part Of This Game')
            DBSession.remove()
            return redirect(url_for('menu'))
        if request.method == 'GET':
            ghostList = ['p1b3','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b3','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
            deadGhosts = ['p1b3','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b3','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
            locationList = ['b11','b21','b31','b41','b51','b61','b22','b22','b32','b42','b52','b62','b13','b23','b33','b43','b53','b63','b14','b24','b34','b44','b54','b64','b15','b25','b35','b45','b55','b65','b16','b26','b36','b46','b56','b66']
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
            if game.previousPlayer != 9 and (game.previousPlayer == 0 or game.previousPlayer > 2):
                winner = ''
                wonBy = ''
            else:
                if userDeadYellow == 4:
                    wonBy = "yellow"
                    winner = userPlayer
                    winnerid = userid
                elif userDeadBlue == 4:
                    wonBy = "blue"
                    winner = opponentPlayer
                    winnerid = opponentid
                elif opponentDeadYellow == 4:
                    wonBy = "yellow"
                    winner = opponentPlayer
                    winnerid = opponentid
                elif opponentDeadBlue == 4:
                    wonBy = "blue"
                    winner = userPlayer
                    winnerid = userid
                elif (game.b11[1:2] == "1b" or game.b61[1:3] == "1b") and game.previousPlayer == 2:
                    wonBy = "exit"
                    winner = 1
                    winnerid = game.player1id
                elif (game.b16[1:2] == "2b" or game.b66[1:3] == "2b") and game.previousPlayer == 1:
                    wonBy = "exit"
                    winner = 2
                    winnerid = game.player2id
                else:
                    winner = ''
                    wonBy = ''
                if winner != '' and game.previousPlayer != 9:
                    date = datetime.now()
                    complete_game = ghostComplete(
                        gameid=game.id,
                        player1id=game.player1id,
                        player2id=game.player2id,
                        winnerid=winnerid,
                        completed=date,
                        won=wonBy)
                    session.add(complete_game)
                    session.commit()
                    game.previousPlayer = 9
                    session.add(game)
                    session.commit()
            if game.previousPlayer == userPlayer or game.previousPlayer == userPlayer * 10:
                flash("Waiting for Opponent's Move, Please Check Back Later")
            DBSession.remove()
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
            elif str(game.b12).startswith('l'):
                game.b12 = ''
            elif str(game.b13).startswith('l'):
                game.b13 = ''
            elif str(game.b14).startswith('l'):
                game.b14 = ''
            elif str(game.b15).startswith('l'):
                game.b15 = ''
            elif str(game.b16).startswith('l'):
                game.b16 = ''
            elif str(game.b21).startswith('l'):
                game.b21 = ''
            elif str(game.b22).startswith('l'):
                game.b22 = ''
            elif str(game.b23).startswith('l'):
                game.b23 = ''
            elif str(game.b24).startswith('l'):
                game.b24 = ''
            elif str(game.b25).startswith('l'):
                game.b25 = ''
            elif str(game.b26).startswith('l'):
                game.b26 = ''
            elif str(game.b31).startswith('l'):
                game.b31 = ''
            elif str(game.b32).startswith('l'):
                game.b32 = ''
            elif str(game.b33).startswith('l'):
                game.b33 = ''
            elif str(game.b34).startswith('l'):
                game.b34 = ''
            elif str(game.b35).startswith('l'):
                game.b35 = ''
            elif str(game.b36).startswith('l'):
                game.b36 = ''
            elif str(game.b41).startswith('l'):
                game.b41 = ''
            elif str(game.b42).startswith('l'):
                game.b42 = ''
            elif str(game.b43).startswith('l'):
                game.b43 = ''
            elif str(game.b44).startswith('l'):
                game.b44 = ''
            elif str(game.b45).startswith('l'):
                game.b45 = ''
            elif str(game.b46).startswith('l'):
                game.b46 = ''
            elif str(game.b51).startswith('l'):
                game.b51 = ''
            elif str(game.b52).startswith('l'):
                game.b52 = ''
            elif str(game.b53).startswith('l'):
                game.b53 = ''
            elif str(game.b54).startswith('l'):
                game.b54 = ''
            elif str(game.b55).startswith('l'):
                game.b55 = ''
            elif str(game.b56).startswith('l'):
                game.b56 = ''
            elif str(game.b61).startswith('l'):
                game.b61 = ''
            elif str(game.b62).startswith('l'):
                game.b62 = ''
            elif str(game.b63).startswith('l'):
                game.b63 = ''
            elif str(game.b64).startswith('l'):
                game.b64 = ''
            elif str(game.b65).startswith('l'):
                game.b65 = ''
            elif str(game.b66).startswith('l'):
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
                session = DBSession()
                session.add(game)
                session.commit()
                game = session.query(ghostGame).filter(ghostGame.id==game_id).one()
                ghostList = ['p1b3','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b3','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
                deadGhosts = ['p1b3','p1b2','p1b3','p1b4','p1y1','p1y2','p1y3','p1y4','p2b3','p2b2','p2b3','p2b4','p2y1','p2y2','p2y3','p2y4']
                locationList = ['b11','b21','b31','b41','b51','b61','b22','b22','b32','b42','b52','b62','b13','b23','b33','b43','b53','b63','b14','b24','b34','b44','b54','b64','b15','b25','b35','b45','b55','b65','b16','b26','b36','b46','b56','b66']
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
                print "winning condition"
                print game.b11[1:2]
                if game.previousPlayer == 0 or game.previousPlayer > 2:
                    winner = ''
                    wonBy = ''
                else:
                    if userDeadYellow == 4:
                        wonBy = "yellow"
                        winner = userPlayer
                        winnerid = userid
                    elif userDeadBlue == 4:
                        wonBy = "blue"
                        winner = opponentPlayer
                        winnerid = opponentid
                    elif opponentDeadYellow == 4:
                        wonBy = "yellow"
                        winner = opponentPlayer
                        winnerid = opponentid
                    elif userDeadBlue == 4:
                        wonBy = "blue"
                        winner = userplayer
                        winnerid = userid
                    elif (game.b11[1:3] == "1b" or game.b61[1:3] == "1b") and game.previousPlayer == 2:
                        print "won by exit at top"
                        wonBy = "exit"
                        winner = 1
                        winnerid = game.player1id
                    elif (game.b16[1:3] == "2b" or game.b66[1:3] == "2b") and game.previousPlayer == 1:
                        print "won by exit at bottom"
                        wonBy = "exit"
                        winner = 2
                        winnerid = game.player2id
                    else:
                        winner = ''
                        wonBy = ''
                if winner != '' and game.previousPlayer != 9:
                    date = datetime.now()
                    complete_game = ghostComplete(
                        gameid=game.id,
                        player1id=game.player1id,
                        player2id=game.player2id,
                        winnerid=winnerid,
                        completed=date,
                        won=wonBy)
                    session = DBSession()
                    session.add(complete_game)
                    session.commit()
                    game.previousPlayer = 9
                    session.add(game)
                    session.commit()
                print opponent.email
                print opponent.notifications
                print game.previousPlayer
                print opponentPlayer
                if game.previousPlayer == userPlayer and opponent.notifications == 'on' and opponent.email != 'none':
                    print "email attempted"
                    me = 'joshbriand@gmail.com'
                    you = opponent.email
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = "Ghosts Turn Update"
                    msg['From'] = me
                    msg['To'] = you
                    text = "Hi %s!\nIt's your turn in Ghosts game #%s against %s" %(opponent.name,game.id,user.name)
                    part1 = MIMEText(text, 'plain')
                    msg.attach(part1)
                    #s = smtplib.SMTP('localhost')
                    #s.sendmail(me, you, msg.as_string())
                    #s.quit()
                if game.previousPlayer == userPlayer or game.previousPlayer == userPlayer * 10:
                    flash("Waiting for Opponent's Move, Please Check Back Later")
                #DBSession.remove()
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
                DBSession.remove()
                return redirect(url_for('game', game_id=game_id))
    else:
        flash('Please log in')
        DBSession.remove()
        return redirect(url_for('login'))

'''
Pool
-api (espn?)
-styling
-sort
-calculate points on result entry
-error handling when results exist
'''
@app.route('/pool', methods=['GET', 'POST'])
@app.route('/pool/', methods=['GET', 'POST'])
@app.route('/pool/login', methods=['GET', 'POST'])
@app.route('/pool/login/', methods=['GET', 'POST'])
def poolLogin():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('pool/login.html')
    elif request.method == 'POST':
        if request.form['login'] == "Log In":
            login_username = request.form['username']
            login_password = request.form['password']
            if login_username:
                if login_password:
                    session = DBSession()
                    pool_users = session.query(PoolUsers).all()
                    DBSession.remove()
                    for user in pool_users:
                        if user.username == login_username:
                            pool_user = user
                            print "success"
                            break
                    if poolUserExists(login_username):
                        if pool_user.username == 'admin':
                            login_hashed_password = login_password
                        else:
                            login_hashed_password = make_secure_val(login_password)
                        if pool_user.username == login_password:
                            login_session['username'] = login_username
                            return redirect(url_for('changePoolPassword'))
                        elif pool_user.password == login_hashed_password:
                            login_session['username'] = login_username
                            if login_username == 'admin':
                                print "successful admin log in"
                                return redirect(url_for('poolAdmin'))
                            else:
                                print "successful log in"
                                return redirect(url_for('poolStandings'))
                        else:
                            flash('Incorrect Password')
                            return render_template('pool/login.html')
                    else:
                        flash('Username Not Found')
                        return render_template('pool/login.html')
                else:
                    flash('No Password Entered')
                    return render_template('pool/login.html')
            elif login_password:
                flash('No Username Entered')
                return render_template('pool/login.html')
        elif request.form['login'] == "Create User":
            session = DBSession()
            new_username = request.form['newUsername']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            new_hashed_password = make_secure_val(new_password)
            if new_username:
                if poolUserExists(new_username):
                    flash('Username Already Exists')
                    return render_template('pool/login.html')
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('pool/login.html')
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('pool/login.html')
                        else:
                            newUser = PoolUsers(username=new_username,
                                            password=new_hashed_password)
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
                            print "new user added"
                            login_session['username'] = new_username
                            return redirect(url_for('poolResults'))
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('pool/login.html')
            else:
                flash('No Username Entered')
                return render_template('pool/login.html')

@app.route('/pool/logout/', methods=['GET'])
def poolLogout():
    login_session.pop('username', None)
    return redirect(url_for('poolLogin'))

@app.route('/pool/changepassword/', methods=['GET', 'POST'])
def changePoolPassword():
    if 'username' in login_session:
        print login_session['username']
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            admin = False
        if request.method == 'GET':
            flash('Please Change Your Password')
            return render_template('pool/changepassword.html',
                                    admin = admin,
                                    user = user.username)
        elif request.method == 'POST':
            current_password = user.password
            new_password = request.form['password']
            confirm_password = request.form['verify']
            new_secure_password = make_secure_val(new_password)
            if new_secure_password != current_password:
                if new_password == confirm_password:
                    user.password = new_secure_password
                    session.add(user)
                    session.commit()
                    DBSession.remove()
                    flash('Password Succesfully Changed!')
                    return redirect(url_for('poolStandings'))
                else:
                    flash('Password Do Not Match!')
                    return render_template(url_for('changePoolPassword'))
            else:
                flash('New Password Must Be Different Than Current Password')
                return render_template(url_for('changePoolPassword'))
    else:
        flash('Please Log In')
        return render_template(url_for('poolLogin'))

@app.route('/pool/addgolfer/', methods=['GET', 'POST'])
@app.route('/pool/addgolfer', methods=['GET', 'POST'])
def poolAdmin():
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        groups = session.query(PoolGroups).all()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/admin.html',
                                    admin = admin,
                                    user = user,
                                    groups = groups)
        elif request.method == 'POST':
            new_golfer_name = request.form['golferName']
            new_golfer_country = request.form['golferCountry']
            new_golfer_rank = request.form['golferRank']
            new_golfer_group = request.form['golferGroup']
            if new_golfer_name and new_golfer_country and new_golfer_rank and new_golfer_group:
                if poolGolferExists(new_golfer_name):
                    flash('Golfer Name Already Exists')
                    return render_template('pool/admin.html',
                                            admin = admin,
                                            user = user,
                                            groups = groups)
                elif poolRankExists(new_golfer_rank):
                    flash('Golfer Rank Already Exists')
                    return render_template('pool/admin.html',
                                            admin = admin,
                                            user = user,
                                            groups = groups)
                else:
                    try:
                        rank = int(new_golfer_rank)
                        groups = session.query(PoolGroups)
                        newGolferGroup = groups.filter_by(id=new_golfer_group).one()
                        newGolfer = PoolGolfers(
                            name = new_golfer_name,
                            country = new_golfer_country,
                            startingRank = rank,
                            group = newGolferGroup)
                        session.add(newGolfer)
                        session.commit()
                        DBSession.remove()
                        print "new golfer added"
                        flash('Golfer Added Seccessfully!')
                        return render_template('pool/admin.html',
                                                admin = admin,
                                                user = user,
                                                groups = groups)
                    except ValueError:
                        flash('Rank Must Be An Integer')
                        return render_template('pool/admin.html',
                                                admin = admin,
                                                user = user,
                                                groups = groups)
            else:
                flash('You Must Enter A Value For Every Field')
                return render_template('pool/admin.html',
                                        admin = admin,
                                        user = user,
                                        groups = groups)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/deletegolfer', methods=['GET', 'POST'])
@app.route('/pool/deletegolfer/', methods=['GET', 'POST'])
def showPoolDeleteGolfer():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.startingRank.asc())
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/deletegolfer.html',
                                    admin=admin,
                                    user=user,
                                    golfers=golfers)
        elif request.method == 'POST':
            delete_golfer = request.form['deletegolfer']
            delete_golfer = int(delete_golfer)
            if delete_golfer:
                golferToDelete = session.query(
                    PoolGolfers).filter_by(id=delete_golfer).all()
                print delete_golfer
                if golferToDelete:
                    for golfer in golferToDelete:
                        session.delete(golfer)
                        session.commit()
                        DBSession.remove()
                        print "golfer deleted!"
                    flash ('Golfer Deleted Successfully!')
                    golfers = session.query(PoolGolfers)
                    golfers = golfers.order_by(PoolGolfers.startingRank.asc())
                    DBSession.remove()
                    return render_template('pool/deletegolfer.html',
                                            admin=admin,
                                            user=user,
                                            golfers=golfers)
                else:
                    flash('Golfer Not Found In Database')
                    return render_template('pool/deletegolfer.html',
                                            admin=admin,
                                            user=user,
                                            golfers=golfers)
            else:
                flash('You Must Select A Golfer To Delete')
                return render_template('pool/deletegolfer.html',
                                        admin=admin,
                                        user=user,
                                        golfers=golfers)

    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/editgroups', methods=['GET', 'POST'])
@app.route('/pool/editgroups/', methods=['GET', 'POST'])
def showPoolEditGroups():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.startingRank.asc())
        groups = session.query(PoolGroups)
        groups = groups.order_by(PoolGroups.id.asc())
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/editgroups.html',
                                    admin=admin,
                                    user=user,
                                    golfers=golfers,
                                    groups=groups)
        elif request.method == 'POST':
            for golfer in golfers:
                edit_golfer_rank = request.form['%s rank' % golfer.id]
                edit_golfer_name = request.form['%s name' % golfer.id]
                edit_golfer_country = request.form['%s country' % golfer.id]
                edit_golfer_group = request.form['%s group' % golfer.id]
                if edit_golfer_rank == str(golfer.startingRank) and edit_golfer_name == golfer.name and edit_golfer_country == golfer.country and edit_golfer_group == str(golfer.group.id):
                    continue
                if edit_golfer_name and edit_golfer_country and edit_golfer_rank and edit_golfer_group:
                    if poolGolferExists(edit_golfer_name) and edit_golfer_name != golfer.name:
                        flash('Golfer Name (%s) Already Exists' % edit_golfer_name)
                        return render_template('pool/editgroups.html',
                                                admin = admin,
                                                user = user,
                                                golfers=golfers,
                                                groups = groups)
                    elif poolRankExists(edit_golfer_rank) and edit_golfer_rank != str(golfer.startingRank):
                        flash('Golfer Rank (%s) Already Exists' % edit_golfer_rank)
                        return render_template('pool/editgroups.html',
                                                admin = admin,
                                                user = user,
                                                golfers=golfers,
                                                groups = groups)
                    else:
                        try:
                            rank = int(edit_golfer_rank)
                            groups = session.query(PoolGroups)
                            editGolferGroup = groups.filter_by(id=edit_golfer_group).one()
                            golfer.name = edit_golfer_name
                            golfer.country = edit_golfer_country
                            golfer.startingRank = edit_golfer_rank
                            golfer.group = editGolferGroup
                            session.add(golfer)
                            session.commit()
                            DBSession.remove()

                        except ValueError:
                            flash('Rank Must Be An Integer')
                            return render_template('pool/editgroups.html',
                                                    admin = admin,
                                                    user = user,
                                                    golfers=golfers,
                                                    groups = groups)
                else:
                    flash('You Must Enter A Value For Every Field')
                    return render_template('pool/editgroups.html',
                                            admin = admin,
                                            user = user,
                                            golfers=golfers,
                                            groups = groups)
            flash('Golfer Editted Seccessfully!')
            session = DBSession()
            users = session.query(PoolUsers)
            users = users.order_by(PoolUsers.username.asc())
            user = users.filter_by(username=login_session['username']).one()
            golfers = session.query(PoolGolfers)
            golfers = golfers.order_by(PoolGolfers.startingRank.asc())
            groups = session.query(PoolGroups)
            groups = groups.order_by(PoolGroups.id.asc())
            DBSession.remove()
            return render_template('pool/editgroups.html',
                                    admin = admin,
                                    user = user,
                                    golfers=golfers,
                                    groups = groups)

    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/addresults', methods=['GET', 'POST'])
@app.route('/pool/addresults/', methods=['GET', 'POST'])
def showPoolAddResults():
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.name.asc())
        tournaments = session.query(PoolTournaments)
        tournaments = tournaments.order_by(PoolTournaments.id.asc())
        results = session.query(PoolResults)
        DBSession.remove()
        available_tournaments_id = []
        available_tournaments_name = []
        for tournament in tournaments:
            available_tournaments_id.append(tournament.id)
            available_tournaments_name.append(tournament.name)
        for i in range(0,len(available_tournaments_id)):
            for result in results:
                if available_tournaments_id[i] == result.tournament_id:
                    available_tournaments_id[i] = -available_tournaments_id[i]
                    available_tournaments_name[i] += " (RESULTS EXIST)"
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/addresults.html',
                                    admin=admin,
                                    user=user,
                                    golfers=golfers,
                                    tournaments=tournaments,
                                    results=results,
                                    available_tournaments_id=available_tournaments_id,
                                    available_tournaments_name=available_tournaments_name)
        elif request.method == 'POST':
            results = session.query(PoolResults)
            tournament_id = request.form['tournament']
            tournaments = session.query(PoolTournaments)
            tournament_id = int(tournament_id)
            if tournament_id < 0:
                flash('Results already exist for this tournament')
                return render_template('pool/addresults.html',
                                        admin = admin,
                                        user = user,
                                        golfers=golfers,
                                        tournaments=tournaments,
                                        available_tournaments_id=available_tournaments_id,
                                        available_tournaments_name=available_tournaments_name)
            tournament = tournaments.filter_by(id=tournament_id).one()
            for golfer in golfers:
                golfer_result = request.form['%s result' % golfer.id]
                if golfer_result != '':
                    for result in results:
                        if tournament_id == str(result.tournament.id) and golfer.name == result.golfer.name:
                            flash('Tournament Results For %s Already Exist' % golfer.name)
                            return render_template('pool/addresults.html',
                                                    admin = admin,
                                                    user = user,
                                                    golfers=golfers,
                                                    tournaments=tournaments,
                                                    available_tournaments_id=available_tournaments_id,
                                                    available_tournaments_name=available_tournaments_name)
                    try:
                        golfer_result_int = int(golfer_result)
                        newGolferResult = PoolResults(
                            golfer = golfer,
                            tournament = tournament,
                            position = 0,
                            overall = golfer_result_int)
                        session.add(newGolferResult)
                        session.commit()
                        DBSession.remove()
                    except ValueError:
                        flash('Rank Must Be An Integer')
                        return render_template('pool/addresults.html',
                                                admin = admin,
                                                user = user,
                                                golfers=golfers,
                                                tournaments=tournaments,
                                                available_tournaments_id=available_tournaments_id,
                                                available_tournaments_name=available_tournaments_name)
            flash('Ranks Added Seccessfully!')
            session = DBSession()
            users = session.query(PoolUsers)
            users = users.order_by(PoolUsers.username.asc())
            user = users.filter_by(username=login_session['username']).one()
            golfers = session.query(PoolGolfers)
            golfers = golfers.order_by(PoolGolfers.startingRank.asc())
            tournaments = session.query(PoolTournaments)
            tournaments = tournaments.order_by(PoolTournaments.id.asc())
            DBSession.remove()
            available_tournaments_id = []
            available_tournaments_name = []
            for tournament in tournaments:
                available_tournaments_id.append(tournament.id)
                available_tournaments_name.append(tournament.name)
            for i in range(0,len(available_tournaments_id)):
                for result in results:
                    if available_tournaments_id[i] == result.tournament_id:
                        available_tournaments_id[i] = -available_tournaments_id[i]
                        available_tournaments_name[i] += " (RESULTS EXIST)"
            return render_template('pool/addresults.html',
                                    admin = admin,
                                    user = user,
                                    golfers=golfers,
                                    tournaments=tournaments,
                                    available_tournaments_id=available_tournaments_id,
                                    available_tournaments_name=available_tournaments_name)

    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/viewresults', methods=['GET', 'POST'])
@app.route('/pool/viewresults/', methods=['GET', 'POST'])
def showPoolViewResults():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.name.asc())
        tournaments = session.query(PoolTournaments)
        tournaments = tournaments.order_by(PoolTournaments.id.asc())
        results = session.query(PoolResults)
        DBSession.remove()
        available_tournaments_id = []
        available_tournaments_name = []
        for tournament in tournaments:
            available_tournaments_id.append(tournament.id)
            available_tournaments_name.append(tournament.name)
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/viewresults.html',
                                    admin=admin,
                                    user=user,
                                    golfers=golfers,
                                    tournaments=tournaments,
                                    available_tournaments_id=available_tournaments_id,
                                    available_tournaments_name=available_tournaments_name)
        else:
            tournament_id = request.form['tournament']
            tournaments = session.query(PoolTournaments)
            tournament_id = int(tournament_id)
            if tournament_id < 0 or tournament_id not in available_tournaments_id:
                flash('Tournament does not exist')
                return render_template('pool/viewresults.html',
                                        admin = admin,
                                        user = user,
                                        golfers=golfers,
                                        tournaments=tournaments,
                                        available_tournaments_id=available_tournaments_id,
                                        available_tournaments_name=available_tournaments_name)
            else:
                return redirect(url_for('showPoolViewResult', tournament_id=tournament_id))
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/viewresult_<int:tournament_id>/', methods=['GET', 'POST'])
def showPoolViewResult(tournament_id):
    ##here josh josh
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        tournaments = session.query(PoolTournaments)
        tournament = tournaments.filter_by(id=tournament_id).one()
        results = session.query(PoolResults)
        results = results.filter_by(tournament=tournament).all()
        golfers = golfers.order_by(PoolGolfers.name.asc())
        golfer_dict = {}
        for golfer in golfers:
            golfer_dict[golfer.id] = ""
        print golfer_dict
        for result in results:
            golfer_dict[int(result.golfer.id)] = int(result.overall)
        print golfer_dict
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/viewresult.html',
                                    admin=admin,
                                    user=user,
                                    golfers=golfers,
                                    tournament=tournament,
                                    golfer_dict=golfer_dict)
        elif request.method == 'POST':
            for golfer in golfers:
                golfer_result = request.form['%s result' % golfer.id]
                if golfer_result != '':
                    try:
                        golfer_result_int = int(golfer_result)
                        newGolferResult = PoolResults(
                            golfer = golfer,
                            tournament = tournament,
                            position = 0,
                            overall = golfer_result_int)
                        session.add(newGolferResult)
                        session.commit()
                        DBSession.remove()
                    except ValueError:
                        flash('Rank Must Be An Integer')
                        return redirect(url_for('showPoolViewResult', tournament_id=tournament_id))
            flash('Ranks Added Seccessfully!')
            session = DBSession()
            users = session.query(PoolUsers)
            users = users.order_by(PoolUsers.username.asc())
            user = users.filter_by(username=login_session['username']).one()
            golfers = session.query(PoolGolfers)
            golfers = golfers.order_by(PoolGolfers.startingRank.asc())
            tournaments = session.query(PoolTournaments)
            tournaments = tournaments.order_by(PoolTournaments.id.asc())
            DBSession.remove()
            return redirect(url_for('showPoolViewResult', tournament_id=tournament_id))

@app.route('/pool/viewgroups', methods=['GET', 'POST'])
@app.route('/pool/viewgroups/', methods=['GET', 'POST'])
def showPoolViewGroups():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.startingRank.asc())
        groups = session.query(PoolGroups)
        groups = groups.order_by(PoolGroups.id.asc())
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/viewgroups.html',
                                    admin=admin,
                                    user=user,
                                    golfers=golfers,
                                    groups=groups)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/adduser', methods=['GET', 'POST'])
@app.route('/pool/adduser/', methods=['GET', 'POST'])
def showPoolAddUser():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/adduser.html',
                                    admin = admin,
                                    user = user)
        elif request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']
            confirm_password = request.form['verify']
            new_email = request.form['email']
            new_hashed_password = make_secure_val(new_password)
            session = DBSession()
            if new_username:
                if poolUserExists(new_username):
                    flash('Username Already Exists')
                    return render_template('pool/adduser.html',
                                            admin=admin,
                                            user=user)
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('pool/adduser.html',
                                            admin=admin,
                                            user=user)
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('pool/adduser.html',
                                                    admin=admin,
                                                    user=user)
                        else:
                            newUser = PoolUsers(username=new_username,
                                            password=new_hashed_password,
                                            email=new_email)
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
                            print "user added!!!"
                            flash('User Added Succesfully!')
                            return render_template('pool/adduser.html',
                                                    admin=admin,
                                                    user=user)
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('pool/adduser.html',
                                                admin=admin,
                                                user=user)
            else:
                flash('No Username Entered')
                return render_template('pool/adduser.html',
                                        admin=admin,
                                        user=user)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))

@app.route('/pool/deleteuser', methods=['GET', 'POST'])
@app.route('/pool/deleteuser/', methods=['GET', 'POST'])
def showPoolDeleteUser():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('poolLogin'))
        if request.method == 'GET':
            return render_template('pool/deleteuser.html',
                                    admin=admin,
                                    user=user,
                                    users=users)
        elif request.method == 'POST':
            delete_user = request.form['deleteuser']
            delete_user = int(delete_user)
            session = DBSession()
            if delete_user:
                choicesToDelete = session.query(
                    PoolChoices).filter_by(user_id=delete_user).all()
                if choicesToDelete:
                    for delChoice in choicesToDelete:
                        session.delete(delChoice)
                        session.commit()
                        DBSession.remove()
                        print "choice deleted!"
                userToDelete = session.query(
                    PoolUsers).filter_by(id=delete_user).all()
                if userToDelete:
                    for delUser in userToDelete:
                        session.delete(delUser)
                        session.commit()
                        DBSession.remove()
                        print "user deleted!"
                    flash ('User Deleted Successfully!')
                    users = session.query(PoolUsers)
                    users = users.order_by(PoolUsers.id.asc())
                    DBSession.remove()
                    return render_template('pool/deleteuser.html',
                                            admin=admin,
                                            user=user,
                                            users=users)
                else:
                    flash('User Not Found In Database')
                    return render_template('pool/deleteuser.html',
                                            admin=admin,
                                            user=user,
                                            users=users)
            else:
                flash('You Must Select A Question To Delete')
                return render_template('pool/deleteuser.html',
                                        admin=admin,
                                        user=user,
                                        users=users)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('poolLogin'))


@app.route('/pool/standings/', methods=['GET', 'POST'])
def poolStandings():
    if request.method == 'GET':
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.startingRank.asc())
        tournaments = session.query(PoolTournaments)
        tournaments = tournaments.order_by(PoolTournaments.id.asc())
        choices = session.query(PoolChoices)
        results = session.query(PoolResults)
        DBSession.remove()
        #needs work
        points =[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        #
        tier1 = [500, 300, 250, 225, 200, 180, 160, 140, 120, 100, 80, 80, 80, 80, 80, 50, 50, 50, 50, 50, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15]
        tier2 = [350, 250, 200, 175, 150, 125, 100, 90, 80, 70, 50, 50, 50, 50, 50, 40, 40, 40, 40, 40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10]
        tier3 = [250, 150, 125, 100, 90, 80, 70, 60, 50, 40, 30, 30, 30, 30, 30, 25, 25, 25, 25, 25, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5]
        totals = [0] * users.count()
        for choice in choices:
            golferResults = results.filter_by(golfer=choice.golfer).all()
            for golferResult in golferResults:
                if golferResult.tournament.tier == 1:
                    points[golferResult.tournament.id - 1][choice.user.id - 1] += tier1[golferResult.overall - 1]
                    totals[choice.user.id - 1] += tier1[golferResult.overall - 1]
                elif golferResult.tournament.tier == 2:
                    points[golferResult.tournament.id - 1][choice.user.id - 1] += tier2[golferResult.overall - 1]
                    totals[choice.user.id - 1] += tier2[golferResult.overall - 1]
                elif golferResult.tournament.tier == 3:
                    points[golferResult.tournament.id - 1][choice.user.id - 1] += tier3[golferResult.overall - 1]
                    totals[choice.user.id - 1] += tier3[golferResult.overall - 1]
        ranks = calculate_rank(totals)
        return render_template('pool/standings.html',
                                user=user.username,
                                users=users,
                                golfers=golfers,
                                tournaments=tournaments,
                                results=results,
                                points=points,
                                totals=totals,
                                ranks=ranks)


@app.route('/pool/<username>', methods=['GET', 'POST'])
def poolTeam(username):
    if request.method == 'GET':
        session = DBSession()
        users = session.query(PoolUsers)
        users = users.order_by(PoolUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        page_user = users.filter_by(username=username).one()
        golfers = session.query(PoolGolfers)
        golfers = golfers.order_by(PoolGolfers.startingRank.asc())
        tournaments = session.query(PoolTournaments)
        tournaments = tournaments.order_by(PoolTournaments.id.asc())
        choices = session.query(PoolChoices)
        results = session.query(PoolResults)
        DBSession.remove()
        #needs work
        tier1 = [500, 300, 250, 225, 200, 180, 160, 140, 120, 100, 80, 80, 80, 80, 80, 50, 50, 50, 50, 50, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15]
        tier2 = [350, 250, 200, 175, 150, 125, 100, 90, 80, 70, 50, 50, 50, 50, 50, 40, 40, 40, 40, 40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10]
        tier3 = [250, 150, 125, 100, 90, 80, 70, 60, 50, 40, 30, 30, 30, 30, 30, 25, 25, 25, 25, 25, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5]
        points = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        totals = [0] * users.count()
        for golfer in golfers:
            golferResults = results.filter_by(golfer=golfer).all()
            for golferResult in golferResults:
                if golferResult.tournament.tier == 1:
                    points[golferResult.tournament.id - 1][golfer.id - 1] += tier1[golferResult.overall - 1]
                elif golferResult.tournament.tier == 2:
                    points[golferResult.tournament.id - 1][golfer.id - 1] += tier2[golferResult.overall - 1]
                elif golferResult.tournament.tier == 3:
                    points[golferResult.tournament.id - 1][golfer.id - 1] += tier3[golferResult.overall - 1]
        golfer_ranks = calculate_golfer_rank(points)
        golfer_points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for tournament in points:
            for x in range(0, len(tournament)):
                golfer_points[x] += tournament[x]

        user_choices = choices.filter_by(user=page_user).all()
        return render_template('pool/team.html',
                                user=user.username,
                                users=users,
                                golfers=golfers,
                                tournaments=tournaments,
                                results=results,
                                points=points,
                                totals=totals,
                                choices=user_choices,
                                ranks=golfer_ranks,
                                golfer_points=golfer_points,
                                page_user=page_user.username)

#end pool

@app.route('/survey', methods=['GET', 'POST'])
@app.route('/survey/', methods=['GET', 'POST'])
@app.route('/survey/login', methods=['GET', 'POST'])
@app.route('/survey/login/', methods=['GET', 'POST'])
def surveyLogin():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('survey/login.html')
    elif request.method == 'POST':
        if request.form['login'] == "Log In":
            login_username = request.form['username']
            login_password = request.form['password']
            if login_username:
                if login_password:
                    session = DBSession()
                    survey_users = session.query(SurveyUsers).all()
                    DBSession.remove()
                    for user in survey_users:
                        if user.username == login_username:
                            survey_user = user
                            print "success"
                            break
                    if surveyUserExists(login_username):
                        if survey_user.username == 'admin':
                            login_hashed_password = login_password
                        else:
                            login_hashed_password = make_secure_val(login_password)
                        if survey_user.username == login_password:
                            login_session['username'] = login_username
                            return redirect(url_for('changeSurveyPassword'))
                        elif survey_user.password == login_hashed_password:
                            login_session['username'] = login_username
                            if login_username == 'admin':
                                print "successful admin log in"
                                return redirect(url_for('surveyAdmin'))
                            else:
                                print "successful log in"
                                return redirect(url_for('surveyResults'))
                        else:
                            flash('Incorrect Password')
                            return render_template('survey/login.html')
                    else:
                        flash('Username Not Found')
                        return render_template('survey/login.html')
                else:
                    flash('No Password Entered')
                    return render_template('survey/login.html')
            elif login_password:
                flash('No Username Entered')
                return render_template('survey/login.html')
        elif request.form['login'] == "Create User":
            session = DBSession()
            new_username = request.form['newUsername']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            new_hashed_password = make_secure_val(new_password)
            if new_username:
                if surveyUserExists(new_username):
                    flash('Username Already Exists')
                    return render_template('survey/login.html')
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('survey/login.html')
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('survey/login.html')
                        else:
                            newUser = SurveyUsers(username=new_username,
                                            password=new_hashed_password)
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
                            print "new user added"
                            login_session['username'] = new_username
                            return redirect(url_for('surveyResults'))
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('survey/login.html')
            else:
                flash('No Username Entered')
                return render_template('survey/login.html')

@app.route('/survey/logout/', methods=['GET'])
def surveyLogout():
    login_session.pop('username', None)
    return redirect(url_for('surveyLogin'))

@app.route('/survey/changepassword/', methods=['GET', 'POST'])
def changeSurveyPassword():
    if 'username' in login_session:
        print login_session['username']
        session = DBSession()
        users = session.query(SurveyUsers)
        users = users.order_by(SurveyUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            admin = False
        if request.method == 'GET':
            flash('Please Change Your Password')
            return render_template('survey/changepassword.html',
                                    admin = admin,
                                    user = user.username)
        elif request.method == 'POST':
            current_password = user.password
            new_password = request.form['password']
            confirm_password = request.form['verify']
            new_secure_password = make_secure_val(new_password)
            if new_secure_password != current_password:
                if new_password == confirm_password:
                    user.password = new_secure_password
                    session.add(user)
                    session.commit()
                    DBSession.remove()
                    flash('Password Succesfully Changed!')
                    return redirect(url_for('surveyResults'))
                else:
                    flash('Password Do Not Match!')
                    return render_template(url_for('showSurveyChangePassword'))
            else:
                flash('New Password Must Be Different Than Current Password')
                return render_template(url_for('showSurveyChangePassword'))
    else:
        flash('Please Log In')
        return render_template(url_for('surveyLogin'))

@app.route('/survey/addquestion/', methods=['GET', 'POST'])
@app.route('/survey/addquestion', methods=['GET', 'POST'])
def surveyAdmin():
    if 'username' in login_session:
        session = DBSession()
        users = session.query(SurveyUsers)
        users = users.order_by(SurveyUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('surveyLogin'))
        if request.method == 'GET':
            return render_template('survey/admin.html',
                                    admin = admin,
                                    user = user)
        elif request.method == 'POST':
            new_question = request.form['question']
            new_answer_1 = request.form['answer1']
            new_answer_2 = request.form['answer2']
            new_answer_3 = request.form['answer3']
            new_answer_4 = request.form['answer4']
            new_answer_5 = request.form['answer5']
            if new_question:
                if new_answer_1 or new_answer_2 or new_answer_3 or new_answer_4 or new_answer_5:
                    newQuestion = SurveyQuestions(question=new_question,
                                                    option1=new_answer_1,
                                                    option2=new_answer_2,
                                                    option3=new_answer_3,
                                                    option4=new_answer_4,
                                                    option5=new_answer_5)
                    session.add(newQuestion)
                    session.commit()
                    DBSession.remove()
                    print "new question added"
                    flash('Question Added Seccessfully!')
                    return render_template('survey/admin.html',
                                            admin = admin,
                                            user = user)
                else:
                    flash('You Must Enter An Answer')
                    return render_template('survey/admin.html',
                                            admin = admin,
                                            user = user)
            else:
                flash('You Must Enter A Question')
                return render_template('survey/admin.html',
                                        admin = admin,
                                        user = user)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('surveyLogin'))

@app.route('/survey/deletequestion', methods=['GET', 'POST'])
@app.route('/survey/deletequestion/', methods=['GET', 'POST'])
def showSurveyDeleteQuestion():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(SurveyUsers)
        users = users.order_by(SurveyUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        questions = session.query(SurveyQuestions)
        questions = questions.order_by(SurveyQuestions.id.asc())
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')

            return redirect(url_for('surveyLogin'))
        if request.method == 'GET':
            return render_template('survey/deletequestion.html',
                                    admin=admin,
                                    user=user,
                                    questions=questions)
        elif request.method == 'POST':
            delete_question = request.form['deletequestion']
            delete_question = int(delete_question)
            if delete_question:
                questionToDelete = session.query(
                    SurveyQuestions).filter_by(id=delete_question).all()
                print delete_question
                if questionToDelete:
                    for question in questionToDelete:
                        session.delete(question)
                        session.commit()
                        DBSession.remove()
                        print "question deleted!"
                    flash ('Question Deleted Successfully!')
                    questions = session.query(SurveyQuestions)
                    questions = questions.order_by(SurveyQuestions.id.asc())
                    DBSession.remove()
                    return render_template('survey/deletequestion.html',
                                            admin=admin,
                                            user=user,
                                            questions=questions)
                else:
                    flash('Question Not Found In Database')
                    return render_template('survey/deletequestion.html',
                                            admin=admin,
                                            user=user,
                                            questions=questions)
            else:
                flash('You Must Select A Question To Delete')
                return render_template('survey/deletequestion.html',
                                        admin=admin,
                                        user=user,
                                        questions=questions)

    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('surveyLogin'))

@app.route('/survey/adduser', methods=['GET', 'POST'])
@app.route('/survey/adduser/', methods=['GET', 'POST'])
def showSurveyAddUser():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(SurveyUsers)
        users = users.order_by(SurveyUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('surveyLogin'))
        if request.method == 'GET':
            return render_template('survey/adduser.html',
                                    admin = admin,
                                    user = user)
        elif request.method == 'POST':
            new_username = request.form['username']
            new_password = request.form['password']
            confirm_password = request.form['verify']
            new_hashed_password = make_secure_val(new_password)
            session = DBSession()
            if new_username:
                if surveyUserExists(new_username):
                    flash('Username Already Exists')
                    return render_template('survey/adduser.html',
                                            admin=admin,
                                            user=user)
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('survey/adduser.html',
                                            admin=admin,
                                            user=user)
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('survey/adduser.html',
                                                    admin=admin,
                                                    user=user)
                        else:
                            newUser = SurveyUsers(username=new_username,
                                            password=new_hashed_password)
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
                            print "user added!!!"
                            flash('User Added Succesfully!')
                            return render_template('survey/adduser.html',
                                                    admin=admin,
                                                    user=user)
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('survey/adduser.html',
                                                admin=admin,
                                                user=user)
            else:
                flash('No Username Entered')
                return render_template('survey/adduser.html',
                                        admin=admin,
                                        user=user)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('surveyLogin'))

@app.route('/survey/deleteuser', methods=['GET', 'POST'])
@app.route('/survey/deleteuser/', methods=['GET', 'POST'])
def showSurveyDeleteUser():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        session = DBSession()
        users = session.query(SurveyUsers)
        users = users.order_by(SurveyUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        DBSession.remove()
        if user.username == 'admin':
            admin = True
        else:
            flash('Access Restricted to Admin User Only')
            return redirect(url_for('surveyLogin'))
        if request.method == 'GET':
            return render_template('survey/deleteuser.html',
                                    admin=admin,
                                    user=user,
                                    users=users)
        elif request.method == 'POST':
            delete_user = request.form['deleteuser']
            delete_user = int(delete_user)
            session = DBSession()
            if delete_user:
                resultsToDelete = session.query(
                    SurveyResults).filter_by(user_id=delete_user).all()
                if resultsToDelete:
                    for delResult in resultsToDelete:
                        session.delete(delResult)
                        session.commit()
                        DBSession.remove()
                        print "result deleted!"
                userToDelete = session.query(
                    SurveyUsers).filter_by(id=delete_user).all()
                if userToDelete:
                    for delUser in userToDelete:
                        session.delete(delUser)
                        session.commit()
                        DBSession.remove()
                        print "user deleted!"
                    flash ('User Deleted Successfully!')
                    users = session.query(SurveyUsers)
                    users = users.order_by(SurveyUsers.id.asc())
                    DBSession.remove()
                    return render_template('survey/deleteuser.html',
                                            admin=admin,
                                            user=user,
                                            users=users)
                else:
                    flash('User Not Found In Database')
                    return render_template('survey/deleteuser.html',
                                            admin=admin,
                                            user=user,
                                            users=users)
            else:
                flash('You Must Select A Question To Delete')
                return render_template('survey/deleteuser.html',
                                        admin=admin,
                                        user=user,
                                        users=users)
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('surveyLogin'))

@app.route('/survey/takepoll', methods=['GET', 'POST'])
@app.route('/survey/takepoll/', methods=['GET', 'POST'])
def showSurveyPoll():
    '''Handler for landing page of website.'''
    if 'username' in login_session:
        if login_session['username'] == 'admin':
            flash('You Must Be Logged In As A User')
            return redirect(url_for('surveyLogin'))
        else:
            if request.method == 'GET':
                session = DBSession()
                users = session.query(SurveyUsers)
                users = users.order_by(SurveyUsers.username.asc())
                user = users.filter_by(username=login_session['username']).one()
                questions = session.query(SurveyQuestions)
                questions = questions.order_by(SurveyQuestions.id.asc())
                results = session.query(SurveyResults)
                print "all results"
                print results
                user_results = results.filter_by(user_id=user.id)
                print "user results"
                print user_results
                first = user_results.first()
                print "first?"
                print first
                DBSession.remove()
                return render_template('survey/takepoll.html',
                                        user=user.username,
                                        questions=questions,
                                        results=user_results,
                                        first=first)
            elif request.method == 'POST':
                session = DBSession()
                users = session.query(SurveyUsers)
                users = users.order_by(SurveyUsers.username.asc())
                user  = users.filter_by(username=login_session['username']).one()
                questions = session.query(SurveyQuestions)
                for question in questions:
                    option_selected = request.form.get(str(question.id))
                    if option_selected:
                        results = session.query(SurveyResults)
                        user_results = results.filter_by(user_id=user.id)
                        for user_result in user_results:
                            if user_result.question.id == question.id:
                                session.delete(user_result)
                                session.commit()
                                print "result deleted!"
                        newResult = SurveyResults(choice = option_selected,
                                                question_id = question.id,
                                                user_id = user.id)
                        session.add(newResult)
                        session.commit()
                        print "result added!"
                DBSession.remove()
                flash('Thanks For Taking The Survey!')
                return redirect(url_for('surveyResults'))
    else:
        flash('You Must Be Logged In To Access This Page')
        return redirect(url_for('surveyLogin'))


@app.route('/survey/results/', methods=['GET', 'POST'])
def surveyResults():
    if request.method == 'GET':
        session = DBSession()
        users = session.query(SurveyUsers)
        users = users.order_by(SurveyUsers.username.asc())
        user = users.filter_by(username=login_session['username']).one()
        results = session.query(SurveyResults)
        results = results.order_by(SurveyResults.question_id.asc())
        questions = session.query(SurveyQuestions)
        questions = questions.order_by(SurveyQuestions.id.asc())
        DBSession.remove()
        resultsToHTML = []
        for question in questions:
            voters = [question,[],[],[],[],[]]
            for result in results:
                if result.question.id == question.id:
                    if result.choice == question.option1:
                        voters[1].append(result.user.username)
                    elif result.choice == question.option2:
                        voters[2].append(result.user.username)
                    elif result.choice == question.option3:
                        voters[3].append(result.user.username)
                    elif result.choice == question.option4:
                        voters[4].append(result.user.username)
                    elif result.choice == question.option5:
                        voters[5].append(result.user.username)
            resultsToHTML.append(voters)
        print resultsToHTML
        return render_template('survey/results.html',
                                user=user.username,
                                results=resultsToHTML)

@app.route('/recipes/login', methods=['GET', 'POST'])
@app.route('/recipes/login/', methods=['GET', 'POST'])
def recipeConnect():
    '''Handler for landing page of website.'''
    if request.method == 'GET':
        return render_template('recipes/login.html')
    elif request.method == 'POST':
        if request.form['login'] == "Log In":
            login_username = request.form['username']
            login_password = request.form['password']
            if login_username:
                if login_password:
                    session = DBSession()
                    recipe_users = session.query(RecipeUsers).all()
                    DBSession.remove()
                    for user in recipe_users:
                        if user.name == login_username:
                            recipe_user = user
                            print "success"
                            break
                    if recipeUserExists(login_username):
                        if recipe_user.name == 'admin':
                            login_hashed_password = login_password
                        else:
                            login_hashed_password = make_secure_val(login_password)
                        if recipe_user.name == login_password:
                            login_session['recipes_username'] = login_username
                            login_session['recipes_user_id'] = recipe_user.id
                            return redirect(url_for('changeRecipePassword'))
                        elif recipe_user.password == login_hashed_password:
                            login_session['recipes_username'] = login_username
                            login_session['recipes_user_id'] = recipe_user.id
                            if login_username == 'admin':
                                print "successful admin log in"
                                return redirect(url_for('recipeAdmin'))
                            else:
                                print "successful log in"
                                return redirect(url_for('showRecipes'))
                        else:
                            flash('Incorrect Password')
                            return render_template('recipes/login.html')
                    else:
                        flash('Username Not Found')
                        return render_template('recipes/login.html')
                else:
                    flash('No Password Entered')
                    return render_template('recipes/login.html')
            elif login_password:
                flash('No Username Entered')
                return render_template('recipes/login.html')
        elif request.form['login'] == "Create User":
            session = DBSession()
            new_username = request.form['newUsername']
            new_password = request.form['newPassword']
            confirm_password = request.form['confirmPassword']
            new_hashed_password = make_secure_val(new_password)
            if new_username:
                if recipeUserExists(new_username):
                    flash('Username Already Exists')
                    return render_template('recipes/login.html')
                elif validate(new_username, USER_RE) is None:
                    flash('That is Not a Valid Username')
                    return render_template('recipes/login.html')
                else:
                    if new_password == confirm_password:
                        if validate(new_password, PASSWORD_RE) is None:
                            flash('That is Not a Valid Password')
                            return render_template('recipes/login.html')
                        else:
                            newUser = RecipeUsers(name=new_username,
                                            password=new_hashed_password)
                            session.add(newUser)
                            session.commit()
                            DBSession.remove()
                            print "new user added"
                            login_session['recipes_username'] = new_username
                            login_session['recipes_user_id'] = recipe_user.id
                            return redirect(url_for('showRecipes'))
                    else:
                        flash('Passwords Do Not Match')
                        return render_template('recipes/login.html')
            else:
                flash('No Username Entered')
                return render_template('recipes/login.html')

@app.route('/recipes/changepassword/', methods=['GET', 'POST'])
def changeRecipePassword():
    if 'recipes_username' in login_session:
        print login_session['recipes_username']
        session = DBSession()
        users = session.query(RecipeUsers)
        users = users.order_by(RecipeUsers.name.asc())
        user = users.filter_by(name=login_session['recipes_username']).one()
        DBSession.remove()
        if user.name == 'admin':
            admin = True
        else:
            admin = False
        if request.method == 'GET':
            flash('Please Change Your Password')
            return render_template('recipes/changepassword.html',
                                    admin = admin,
                                    user = user.name)
        elif request.method == 'POST':
            current_password = user.password
            new_password = request.form['password']
            confirm_password = request.form['verify']
            new_secure_password = make_secure_val(new_password)
            if new_secure_password != current_password:
                if new_password == confirm_password:
                    user.password = new_secure_password
                    session.add(user)
                    session.commit()
                    DBSession.remove()
                    flash('Password Succesfully Changed!')
                    return redirect(url_for('showRecipes'))
                else:
                    flash('Password Do Not Match!')
                    return render_template(url_for('changeRecipePassword'))
            else:
                flash('New Password Must Be Different Than Current Password')
                return render_template(url_for('changeRecipePassword'))
    else:
        flash('Please Log In')
        return render_template(url_for('recipeConnect'))


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
    users = session.query(RecipeUsers).order_by(RecipeUsers.id)
    DBSession.remove()
    if request.method == 'POST':
        # query all recipes
        session = DBSession()
        recipes = session.query(Recipes)
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
            recipes = recipes.order_by(Recipes.date.desc())
        elif order == "Oldest":
            # sort from oldest to newest
            recipes = recipes.order_by(Recipes.date.asc())
        elif order == "Alphabetically by Name":
            # sort alphabetically by recipe name
            recipes = recipes.order_by(Recipes.name.asc())
        elif order == "Popular":
            # sort by most popular recipe first
            likeOrder = getOrderedLikes()
        DBSession.remove()
        return render_template(
            'recipes/recipes.html',
            user=login_session['recipes_username'],
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
        for user_login in login_session:
            print user_login
        if user_id == "":
            # render if user selects All Recipes or goes to '/recipes'
            # query all recipes to display on webpage
            session = DBSession()
            recipes = session.query(Recipes).order_by(Recipes.date.desc())
            DBSession.remove()
            return render_template(
                'recipes/recipes.html',
                user=login_session['recipes_username'],
                recipes=recipes,
                users=users,
                meals=meals,
                cuisines=cuisines,
                likeOrder=likeOrder)
        else:
            # webpage if user selects My Recipes
            session = DBSession()
            recipes = session.query(Recipes).filter_by(
                user_id=user_id).order_by(
                Recipes.date.desc())
            DBSession.remove()
            return render_template(
                'recipes/recipes.html',
                user=login_session['recipes_username'],
                recipes=recipes,
                users=users,
                userSelect=user_id,
                meals=meals,
                cuisines=cuisines,
                likeOrder=likeOrder)

@app.route('/recipes/recipe<int:recipe_id>/')
def showRecipe(recipe_id):
    '''handler for displaying webpage of an individual recipe'''
    if recipeExists(recipe_id):
        # check to see if recipe id exists
        # query recipe, method, ingredients, likes and comments
        session = DBSession()
        recipe = session.query(Recipes).filter_by(id=recipe_id).one()
        ingredients = session.query(RecipeIngredients).filter_by(
            recipe_id=recipe_id).all()
        processes = session.query(RecipeProcess).filter_by(recipe_id=recipe_id).all()
        likes = session.query(RecipeLikes).filter_by(recipe_id=recipe_id).all()
        comments = session.query(RecipeComments).filter_by(
            recipe_id=recipe_id).order_by(
            RecipeComments.id.desc()).all()
        liked = False
        if 'recipes_username' in login_session:
            # check to see if user is logged in
            if likes:
                # check to see if likes exist for this recipe
                '''check to see if user already likes to recipe (if so, the
                ability to like is changed to the ability to unlike when webpage
                is rendered)'''
                liked = userLiked(likes)
        #DBSession.remove()
        return render_template(
            'recipes/recipe.html',
            user=login_session['recipes_username'],
            recipe=recipe,
            ingredients=ingredients,
            processes=processes,
            likes=likes,
            liked=liked,
            meals=meals,
            cuisines=cuisines,
            comments=comments)
    # redirect to '/' and flash error message if recipe id does not exist
    flash('Recipe does not exist')
    return redirect('/recipes/')

@app.route('/recipes/addrecipe/', methods=['GET', 'POST'])
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
        user_id = login_session['recipes_user_id']
        date = datetime.now()
        if error != "":
            '''if there is an error, rerender webpage with prefilled out form and
            error message'''
            flash(error)
            return render_template(
                'recipes/addrecipe.html',
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
        newRecipe = Recipes(
            name=name,
            cuisine=cuisine,
            meal=meal,
            date=date,
            picture=picture,
            user_id=user_id)
        session.add(newRecipe)
        session.commit()
        recipe_id = session.query(Recipes).filter_by(name=name).one().id
        for ingredient in ingredientList:
            # commit individual ingredients to database
            newIngredient = RecipeIngredients(
                ingredient=ingredient, recipe_id=recipe_id)
            session.add(newIngredient)
            session.commit()
        for process in processList:
            # commit individual method steps to database
            newProcess = RecipeProcess(process=process, recipe_id=recipe_id)
            session.add(newProcess)
            session.commit()
        # redirect user to newly created recipe webpage and success message
        flash('New Recipe %s Successfully Created' % newRecipe.name)
        DBSession.remove()
        return redirect(url_for('showRecipe', recipe_id=recipe_id))
        # return to recipe (no s!)
    else:
        if 'recipes_username' not in login_session:
            # redirect to '/' if user not logged in, error message
            flash('User not logged in')
            return redirect('/recipes/')
        else:
            return render_template(
                'recipes/addrecipe.html',
                meals=meals,
                cuisines=cuisines)

@app.route('/recipes/<int:recipe_id>/edit/', methods=['GET', 'POST'])
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
        author = session.query(Recipes).filter_by(id=recipe_id).one().user
        recipeToEdit = session.query(Recipes).filter_by(id=recipe_id).one()
        oldIngredients = session.query(
            RecipeIngredients).filter_by(recipe_id=recipe_id).all()
        oldProcesses = session.query(RecipeProcess).filter_by(
            recipe_id=recipe_id).all()
        if 'recipes_username' in login_session:
            if author.id == login_session['recipes_user_id']:
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
                    user_id = login_session['recipes_user_id']
                    date = datetime.now()
                    if error != "":
                        flash(error)
                        DBSession.remove()
                        return render_template(
                            'recipes/editrecipe.html',
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
                        newIngredient = RecipeIngredients(
                            ingredient=ingredient, recipe_id=recipe_id)
                        session.add(newIngredient)
                        session.commit()
                    # delete old process from database
                    for process in oldProcesses:
                        session.delete(process)
                        session.commit()
                    # add new process to database
                    for process in processList:
                        newProcess = RecipeProcess(
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
                        'recipes/editrecipe.html',
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

@app.route('/recipes/<int:recipe_id>/delete/', methods=['GET', 'POST'])
def deleteRecipe(recipe_id):
    '''handler to delete existing recipe'''
    if recipeExists(recipe_id):
        # if recipe if exists in database
        '''query author, ingredients, process, comments, likes and recipe from
        database'''
        session = DBSession()
        author = session.query(Recipes).filter_by(id=recipe_id).one().user
        recipeToDelete = session.query(Recipes).filter_by(id=recipe_id).one()
        likesToDelete = session.query(RecipeLikes).filter_by(recipe_id=recipe_id)
        commentsToDelete = session.query(
            RecipeComments).filter_by(recipe_id=recipe_id)
        ingredientsToDelete = session.query(
            RecipeIngredients).filter_by(recipe_id=recipe_id).all()
        processesToDelete = session.query(RecipeProcess).filter_by(
            recipe_id=recipe_id).all()
        if 'recipes_username' in login_session:
            if author.id == login_session['recipes_user_id']:
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
                        return redirect('/recipes/', recipe_id=recipe_id)
                else:
                    return render_template(
                        'recipes/deleterecipe.html', recipe=recipeToDelete)
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

@app.route('/recipes/<int:recipe_id>/like/')
def likeRecipe(recipe_id):
    '''handler to like a recipe'''
    if recipeExists(recipe_id):
        # if recipe id exists in database
        if 'recipes_username' in login_session:
            # if user is logged in
            # query likes in database
            session = DBSession()
            likes = session.query(RecipeLikes).filter_by(recipe_id=recipe_id).all()
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
            newLike = RecipeLikes(
                user_id=login_session['recipes_user_id'],
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

@app.route('/recipes/<int:recipe_id>/unlike/')
def unlikeRecipe(recipe_id):
    '''handler for user to unlike a recipe'''
    if recipeExists(recipe_id):
        # if recipe id exists in database
        if 'recipes_username' in login_session:
            # if user is logged in
            # query likes from database
            session = DBSession()
            likes = session.query(RecipeLikes).filter_by(recipe_id=recipe_id).all()
            if likes:
                # if likes exist
                if userLiked(likes):
                    # if user likes recipe
                    # query user's like for recipe and delete
                    likeToDelete = session.query(RecipeLikes).filter_by(
                        user_id=login_session['recipes_user_id'], recipe_id=recipe_id).first()
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

@app.route('/recipes/<int:recipe_id>/addcomment/', methods=['GET', 'POST'])
def addComment(recipe_id):
    '''handler for user to add comment to recipe'''
    if recipeExists(recipe_id):
        # recipe exists in database
        if request.method == 'POST':
            if 'recipes_username' in login_session:
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
                    newComment = RecipeComments(
                        comment=comment,
                        recipe_id=recipe_id,
                        user_id=login_session['recipes_user_id'],
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
                return render_template('recipes/addcomment.html')
        else:
            return render_template('recipes/addcomment.html')
    else:
        # redirect and error message if recipe does not exist
        flash('Recipe does not exist')
        return redirect('/recipes/')

@app.route(
    '/recipes/<int:recipe_id>/editcomment/<int:comment_id>/',
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
                RecipeComments).filter_by(id=comment_id).one()
            DBSession.remove()
            if request.method == 'POST':
                # query author id
                session = DBSession()
                author = session.query(RecipeComments).filter_by(
                    id=comment_id).one().user
                if 'recipes_username' in login_session:
                    # user is logged in
                    editComment = request.form['comment']
                    if author.id == login_session['recipes_user_id']:
                        # user id is the same as author id
                        if editComment == "":
                            # redirect and error message if comment is empty
                            flash('You must enter a comment in order to submit one')
                            DBSession.remove()
                            return render_template(
                                'recipes/editcomment.html', comment=commentToEdit)
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
                    return render_template('recipes/addcomment.html')
            else:
                return render_template(
                    'recipes/editcomment.html', comment=commentToEdit)
        else:
            # error message and redirect if comment does not exist
            flash('Comment does not exist')
            return render_template('recipes/addcomment.html')
    else:
        # redirect and error message if recipe does not exist
        flash('Recipe does not exist')
        return redirect('/recipes/')

@app.route(
    '/recipes/<int:recipe_id>/deletecomment/<int:comment_id>/',
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
            author = session.query(RecipeComments).filter_by(
                id=comment_id).one().user
            commentToDelete = session.query(
                RecipeComments).filter_by(id=comment_id).one()
            DBSession.remove()
            if 'recipes_username' in login_session:
                # user is logged in
                if author.id == login_session['recipes_user_id']:
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
                        return render_template('recipes/deletecomment.html')
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

@app.route('/recipes/logout/', methods=['GET'])
def recipeDisconnect():
    login_session.pop('recipes_username', None)
    login_session.pop('recipes_user_id', None)
    return redirect(url_for('recipeConnect'))

if __name__ == '__main__':
    app.secret_key = "Don't panic!"
    app.debug = True
    '''app.run()'''
    app.run("0.0.0.0", debug=True)
