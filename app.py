
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db
from registerform import RegisterForm
from sqlalchemy.exc import IntegrityError

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
        # get user data from form exclude csrf_token key
        user_dict = {k: form.data[k] for k in form.data if k != 'csrf_token'}
        # user_dict = {
        #     'username':     form['username'].data,
        #     'password':     form['password'].data,
        #     'email':        form['email'].data,
        #     'first_name':   form['first_name'].data,
        #     'last_name':    form['last_name'].data
        #     }
        # register user and hash password
        user = User.register_user(user_dict['username'], user_dict['password'])
        # enter the rest of the data that was submitted
        user.email = user_dict['email']
        user.first_name = user_dict['first_name']
        user.last_name = user_dict['last_name']

        db.session.add(user)
        
        try: # try to enter username  or email if error render register page again
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
        return redirect('/secret')
    return render_template('register.html', form=form)

# GET /login
# Show a form that when submitted will login a user. This form should accept a username and a password.

# Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# POST /login
# Process the login form, ensuring the user is authenticated and going to /secret if so.
@app.route('/login')
def login_user():
    """ Login user route """
    return "<h1>Login route</h1>"

# GET /secret
# Return the text “You made it!” (don’t worry, we’ll get rid of this soon)
@app.route('/secret')
def secret_route():
    """ Secret route """
    return "<h1>You made it!!</h1>"