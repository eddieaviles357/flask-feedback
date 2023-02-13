
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, Feedback, db
from form import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from markupsafe import escape

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI="postgresql:///feedback",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # SQLALCHEMY_ECHO=True,
    SECRET_KEY="xxsecretxxkeyxxyesxx",
    DEBUG_TB_INTERCEPT_REDIRECTS=False
)

# connect db
connect_db(app)

debug = DebugToolbarExtension(app)
# GET / 
# Redirect to /register.

@app.route('/')
def home():
    """ Home route """
    return redirect('/register')

# GET /register
# POST /register
# Process the registration form by adding a new user. Then redirect to /users/<username>
@app.route('/register', methods=["GET", "POST"])
def register_user():
    """ Register route ( register a new user ) """
    form = RegisterForm()

    if form.validate_on_submit():
        # get user data from form exclude csrf_token key
        user_dict = {k: form.data[k] for k in form.data if k != 'csrf_token'}
        # register user and hash password
        user = User.register_user(user_dict['username'], user_dict['password'])
        # enter the rest of the data that was submitted
        user.email = user_dict['email']
        user.first_name = user_dict['first_name']
        user.last_name = user_dict['last_name']

        
        try: # try to enter username  or email if error render register page again
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            # failed so we rollback whatever data was in the session
            db.session.rollback()
            # add an error to be displayed via client form
            form.username.errors.append('Username taken, Please enter a different username')
            form.email.errors.append('Email taken, Please enter a different email')
            flash("Invalid credentials", "danger")
            # render client to try to register again
            return render_template('register.html', form=form)

        # add user to the client session
        session['username'] = user.username
        flash("Successfully Registered", "success")
        # redirect to protected route
        return redirect(f'/users/{user.username}')
    return render_template('register.html', form=form)

# GET /login
# Shows a form that when submitted will login a user. 
# This form accepts a username and a password.
# POST /login
# Processes the login form, ensuring the user is authenticated and going to /users/<username>.
@app.route('/login', methods=["GET", "POST"])
def get_login():
    """ Get login form route """
    form = LoginForm()

    # only true if it's a POST route
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # check credential for a match in the database
        if User.authenticate_user(username, password):
            flash(f'Welcome {username}', 'success')
            session['username'] = username
            return redirect(f'/users/{username}')
        else:
            # user did not enter valid credetials
            flash('Wrong credentials', 'danger')
            return render_template('login.html', form=form)

    # Get route
    return render_template('login.html', form=form)


# GET /logout
@app.route('/logout')
def logout_user():
    """ Logout user route """
    session.pop('username')
    flash('Signed out successful', 'success')
    return redirect('/')


# GET /users/<username>
@app.route('/users/<username>')
def user_details(username):
    # escape characters
    username = escape(username)
    """ User details ( protected route )"""
    user = User.query.get_or_404(username)
    if session.get('username') == user.username:
        # access 
        feedbacks = Feedback.query.filter_by(username_key=user.username)
        return render_template('user-details.html', user=user, feedbacks=feedbacks)
    else:
        # user does not have access
        form = LoginForm()
        flash('Please Login to access', 'warning')
        return render_template('login.html', form=form)


# POST /users/<username>/delete
# Remove the user from the database and make sure to also delete all of their feedback. 
# Clear any user information in the session and redirect to /. 
# Make sure that only the user who is logged in can successfully delete their account
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """ Delete user """
    user = User.query.get_or_404(username)
    if session.get('username') == user.username:
        # access
        db.session.delete(user)
        db.session.commit()
        session.pop('username') # remove user from session
        flash('User Deleted', 'danger')
        return redirect('/login')
    else:
        # can't delete user redirect
        flash('Can\'t do that please login')
        redirect('/login')

# GET /users/<username>/feedback/add
# Displays a form to add feedback.
# Only the user who is logged in can see this form
@app.route('/users/<username>/feedback/add')
def add_feedback(username):
    """ Add feddback route """
    username = escape(username)
    form = FeedbackForm()
    return render_template('add-feedback.html', form=form)

# POST /users/<username>/feedback/add
# Add a new piece of feedback and redirect to /users/<username> — 
# Make sure that only the user who is logged in can successfully add feedback


# GET /feedback/<feedback-id>/update
# Display a form to edit feedback — **Make sure that only the user who has written that feedback can see this form **


# POST /feedback/<feedback-id>/update
# Update a specific piece of feedback and redirect to /users/<username> — 
# Make sure that only the user who has written that feedback can update it


# POST /feedback/<feedback-id>/delete
# Delete a specific piece of feedback and redirect to /users/<username> — 
# Make sure that only the user who has written that feedback can delete it