
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, Feedback, db
from form import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError, SAWarning
from markupsafe import escape
from utils import is_user_in_session, redirect_to_login_with_flash_message

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


@app.errorhandler(404)
def page_not_found(err):
    """ Custom 404 page when url not found"""
    return render_template('404.html'), 404

# GET / 
# Redirect to /register.

@app.route('/')
def home():
    """ Home route """
    try:
        user = User.query.get_or_404(session['username'])
        if is_user_in_session(user.username):
            return redirect(f'/users/{user.username}')
    except KeyError:
        return redirect('/register')
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
    if is_user_in_session(user.username):
        # access 
        feedbacks = Feedback.query.filter_by(username_key=user.username)
        return render_template('user-details.html', user=user, feedbacks=feedbacks)
    else:
        # user does not have access
        return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')


# POST /users/<username>/delete
# Remove the user from the database and make sure to also delete all of their feedback. 
# Clear any user information in the session and redirect to /. 
# Make sure that only the user who is logged in can successfully delete their account
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """ Delete user """
    user = User.query.get_or_404(username)
    if is_user_in_session(user.username):
        # access
        db.session.delete(user)
        db.session.commit()
        session.pop('username') # remove user from session
        flash('User Deleted', 'danger')
        return redirect('/login')
    else:
        # can't delete user redirect
        return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')

# *****************************************
# **************** FEEDBACK ***************
# *****************************************

# GET /users/<username>/feedback/add
# Displays a form to add feedback.
# Only the user who is logged in can see this form

# POST /users/<username>/feedback/add
# Adds a new piece of feedback and redirects to /users/<username> — 
@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """ Add feddback route """
    username = escape(username)
    user = User.query.get_or_404(username)

    if is_user_in_session(user.username):
        # User is in session
        form = FeedbackForm()
        # POST
        if form.validate_on_submit():
            fb = {k: form.data[k] for k in form.data if k != 'csrf_token'}
            feedback = Feedback(**fb, username_key=user.username)
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback added successfully', 'success')
            return redirect(f'/users/{user.username}')
        # GET
        return render_template('add-feedback.html', form=form)
    else:
        # User is not in session
        return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')


# GET /feedback/<feedback-id>/update
# Displays a form to edit feedback —
# POST /feedback/<feedback-id>/update
# Updates a specific piece of feedback and redirects to /users/<username> — 
@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """ Update feedback route """
    # Is the user in session match
    try:
        feedback = Feedback.query.filter_by(id=feedback_id).first()
        username = feedback.username_key
        if is_user_in_session(username):
            form = FeedbackForm()
            # POST
            if form.validate_on_submit():
                fb = {k: form.data[k] for k in form.data if k != 'csrf_token'}
                feedback.title = fb['title']
                feedback.content = fb['content']
                db.session.commit()
                flash('Feedback updated', 'success')
                return redirect(f'/users/{username}')
            # GET
            # prepopulate form with current feedback information
            form = FeedbackForm(obj=feedback)
            return render_template('edit-feedback.html', form=form, feedback=feedback)
    except AttributeError:
        return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')
    
    return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')

# POST /feedback/<feedback-id>/delete
# Delete a specific piece of feedback and redirect to /users/<username> — 
@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """ Deletes a feedback """
    try:
        feedback = Feedback.query.filter_by(id=feedback_id).first()
        username = feedback.username_key
        if is_user_in_session(username):
            # user has access
            db.session.delete(feedback)
            db.session.commit()
            flash('Deleted Feedback', 'danger')
            return redirect(f'/users/{username}')
    except AttributeError:
        return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')
    return redirect_to_login_with_flash_message('Can\'t do that please login', 'danger')