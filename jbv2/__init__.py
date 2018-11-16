from flask import (Flask, render_template, request, redirect, jsonify, url_for, flash)
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database_setup import (Base, RecipeUsers, Recipes, RecipeComments, RecipeLikes, RecipeProcess, RecipeIngredients, ghostUser, ghostGame, ghostComplete, SurveyUsers, SurveyResults, SurveyQuestions)
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
    q = session.query(ghostUser).filter_by(name=name)
    return session.query(q.exists()).scalar()

def surveyUserExists(name):
    session = DBSession()
    z = session.query(SurveyUsers).filter_by(username=name)
    print session.query(z.exists()).scalar()
    DBSession.remove()
    return session.query(z.exists()).scalar()

def recipeUserExists(name):
    session = DBSession()
    z = session.query(RecipeUsers).filter_by(username=name)
    print session.query(z.exists()).scalar()
    DBSession.remove()
    return session.query(z.exists()).scalar()


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

@app.route('/merch', methods=['GET'])
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
    DBSession.remove()
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
            recipes = session.query(Recipes).order_by(Recipes.date.desc())
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
            recipes = session.query(Recipes).filter_by(
                user_id=user_id).order_by(
                Recipes.date.desc())
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


def recipeExists(recipe_id):
    '''function to check if recipe exists in database'''
    q = session.query(Recipes).filter_by(id=recipe_id)
    return session.query(q.exists()).scalar()


def commentExists(comment_id):
    '''function to check if comment exists in database'''
    q = session.query(RecipeComments).filter_by(id=comment_id)
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
    recipes = session.query(Recipes)
    for recipe in recipes:
        likeDict[recipe.id] = 0
    likes = session.query(RecipeLikes)
    for like in likes:
        likeDict[recipeLikes.recipe_id] += 1
    likeList = sorted(likeDict, key=lambda k: likeDict[k], reverse=True)
    return likeList

def getUserID(email):
    '''function to look up and return user id from database'''
    try:
        user = session.query(RecipeUsers).filter_by(email=email).first()
        return user.id
    except BaseException:
        return None

if __name__ == '__main__':
    app.secret_key = "Don't panic!"
    app.debug = True
    '''app.run()'''
    app.run("0.0.0.0", debug=True)
