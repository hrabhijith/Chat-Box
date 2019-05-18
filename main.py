from flask import Flask, render_template
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import exc
from database_setup import Users, Base, Messages
from flask import request
import sys
import logging
from flask import redirect
from flask import url_for
from flask import session as login_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


# Creates sqlite DB connection and return session object
def dbConnection():
    try:
        engine = create_engine('sqlite:///users.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
    except exc.SQLAlchemyError:
        logging.error('error in db connection')
        sys.exit(1)
    return session


# Home page route, registration or login
@app.route('/', methods=['GET', 'POST'])
def signup():
    # Checking whether the user is already connected or not
    if login_session.get('username') is not None:
        return redirect(url_for('sessions'))

    # Creating DB connection
    session = dbConnection()

    # fetching users data from database to compare usernames
    try:
        users = session.query(Users).all()
    except AttributeError:
        logging.error('No users data')

    # POST method functionality
    if request.method == 'POST':
        uniqueNameFlag = 0
        uniqueEmailFlag = 0

        for i in users:
            if request.form['username'] == i.username:
                uniqueNameFlag = 1
            if request.form['email'] == i.email:
                uniqueEmailFlag = 1

        # Checking whether username and email already exists or not
        if uniqueNameFlag == 1 and uniqueEmailFlag == 1:
            return render_template('signup.html', emailValid=False, nameValid=False)

        # Checking whether username already exists or not
        elif uniqueNameFlag == 1:
            return render_template('signup.html', nameValid=False)
        
        # Checking whether email already exists or not
        elif uniqueEmailFlag == 1:
            return render_template('signup.html', emailValid=False)
        
        # Creating new user
        newUser = Users(name=request.form['name'], username=request.form['username'], email=request.form['email'], online=0)
        newUser.hash_password(request.form['password'])
        session.add(newUser)
        session.commit()
        session.close()

        # on successful registration, redirecting to login 
        return redirect(url_for('login'))

    session.close()
    return render_template('signup.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Checking whether the user is already connected or not
    if login_session.get('username') is not None:
        return redirect(url_for('sessions'))

    # Creating DB connection
    session = dbConnection()

    if request.method == 'POST':
        try:
            user = session.query(Users).filter_by(email=request.form['email']).one_or_none()
        except exc.SQLAlchemyError:
            logging.error('No users data for the give email')
        
        if user is None:
            return render_template('login.html', emailValid = False)
        
        if user.verify_password(request.form['password']):
            login_session['id'] = user.id
            login_session['name'] = user.name
            login_session['username'] = user.username

            # Making the user online
            user.online = 1
            session.add(user)
            session.commit()
            session.close()

            return redirect(url_for('sessions'))
        else:
            return render_template('login.html', passwordValid = False)

    session.close()
    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    # Creating DB connection
    session = dbConnection()
    user = session.query(Users).filter_by(id=login_session['id']).one()
    user.online = 0
    session.add(user)
    session.commit()
    session.close()

    del login_session['name']
    del login_session['username']
    del login_session['id']

    return redirect(url_for('signup'))


# Session page where users can chat
@app.route('/session')
def sessions():
    # Checking whether the user is already connected or not
    if login_session.get('username') is None:
        return redirect(url_for('login'))

    # Creating DB connection
    session = dbConnection()

    # Fetching users who are online, messages
    users = session.query(Users).filter_by(online=1).all()
    
    messagesList = []
    try:
        messages = session.query(Messages).all()
    except:
        messages = None

    if messages is not None:
        for i in messages:
            messagesDict = {'message': '', 'username': ''}
            messageUser = session.query(Users).filter_by(id=i.user_id).one()
            messagesDict['message'] = i.message
            messagesDict['username'] = messageUser.username
            messagesList.append(messagesDict)
    else:
        messagesList = None
    
    session.close()
    return render_template('session.html', users=users, messages=messagesList)



def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    json['username'] = login_session['username']

    # Creating DB connection
    session = dbConnection()

    # Storing user messages
    user = session.query(Users).filter_by(id=login_session['id']).one_or_none()

    newMessage = Messages(message=json['message'], user=user)
    session.add(newMessage)
    session.commit()
    session.close()
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=1111)