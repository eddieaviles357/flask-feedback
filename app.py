
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db
from registerform import RegisterForm

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI="postgresql:///feedback.sql",
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
# Show a form that when submitted will register/create a user. 
# This form should accept a username, password, email, first_name, and last_name.
# Make sure you are using WTForms and that your password input hides the characters that the user is typing!
    
# POST /register
# Process the registration form by adding a new user. Then redirect to /secret
@app.route('/register', methods=["GET", "POST"])
def register_user():
    """ Register route ( register a new user ) """
    form = RegisterForm()
    if form.validate_on_submit():
        user = {k: form.data[k] for k in form.data if k != 'csrf_token'}

        for k in form.data: print(k,form.data[k])
        flash("Successfully Register", "success")
        redirect('/secret')
    return render_template('register.html', form=form)

# GET /login
# Show a form that when submitted will login a user. This form should accept a username and a password.

# Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# POST /login
# Process the login form, ensuring the user is authenticated and going to /secret if so.

# GET /secret
# Return the text “You made it!” (don’t worry, we’ll get rid of this soon)
@app.route('/secret')
def secret_route():
    """ Secret route """
    return "<h1>You made it!!</h1>"