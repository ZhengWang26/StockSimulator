from flaskServer import app
from flask import render_template, request, jsonify, redirect, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import db

app.config['SECRET_KEY'] = 'hahahhaha'

# need to do all the db functions

loginManager = LoginManager()
loginManager.init_app(app)

@loginManager.user_loader
def load_user(user_id):
    user = db.getFromId(user_id)
    if type(user) == str:
        return None
    return user
    
@loginManager.unauthorized_handler
def unauthorized():
    return redirect('/')




@app.errorhandler(404)
def page_not_found(e):
    print(str(e))
    return (render_template('404.html'), 404)


@app.route('/checkStatus')
def checkStatus():
    if current_user.is_authenticated:
        return jsonify(status = True)
    else:
        return jsonify(status = False)






@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect('/userhome')
    return render_template('signUp.html')

@app.route('/newUser', methods = ['POST'])
def newUser():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    result = db.addUser(username, email, password)
    print(email, username, password)
    print('adding new user', result)
    return jsonify(result = result)



@app.route('/')
@app.route('/signin')
def signin():
    if current_user.is_authenticated:
        return redirect('/userhome')
    return (render_template('stocksimulator.html'))

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    result = db.authenticate(username, password)
    print(username, password)
    print('logging in', result)
    if type(result) == str:
        return jsonify(result = result)
    else:
        login_user(result)
        return jsonify(result = 'success')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')



@app.route('/userhome/<username>')
@login_required
def userhome(username):
    print('\n\n\n\n\n\n\n-----------------------------------------------------------------------', username, '\n\n\n\n\n\n\n\n\n')
    return render_template('homepage.html')

@app.route('/addWatchList', methods = ['POST'])
def addWatchList():
    username = request.form['username']
    symbol = request.form['symbol']
    result = db.addToWatchList(username, symbol)
    return jsonify(result = result)


@app.route('/getWatchList/<username>', methods = ['GET'])
def getWatchList(username):
    return jsonify(watchList = db.getWatchList(username))
