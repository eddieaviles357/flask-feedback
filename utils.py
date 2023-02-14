from flask import session, flash, redirect
from form import LoginForm

def is_user_in_session(username):
    """ Checks if user is in session """
    return True if session['username'] == username else False

def redirect_to_login_with_flash_message(msg, category):
    """ Redirect to Login form route w/ flash messages and category """
    flash(msg, category)
    return redirect('/login')