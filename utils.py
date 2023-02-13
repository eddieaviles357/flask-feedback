from flask import session
def is_user_in_session(username):
    """ Checks if user is in session """
    return True if session['username'] == username else False