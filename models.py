from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """ Connect Database """
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # relation to Feedback model
    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User username={self.username}, password={self.password}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}>"

    @classmethod
    def register_user(cls, username, pswrd):
        """ Register User w/hashing password """
        hashed_pswrd = bcrypt.generate_password_hash(pswrd)
        # turn to bytestring to normal unicode utf8 string
        hashed_pswrd_utf8 = hashed_pswrd.decode('utf8')
        # return instance of user with hashed pswrd
        return cls(username=username, password=hashed_pswrd_utf8)

    @classmethod
    def authenticate_user(cls, username, pswrd):
        """ Authenticate user """
        # check entered password against database passwrod
        try:
            user = User.query.filter_by(username=username).first()
            is_user_authenticated = bcrypt.check_password_hash(user.password, pswrd)
            # was password a match
            return is_user_authenticated
        except AttributeError as AtrErr:
            # username doesn't exist
            return False


class Feedback(db.Model):
    """ Feedback Model """

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username_key = db.Column(db.ForeignKey('users.username'))

    def __repr__(self):
        return f"<Feedback id={self.id}, title={self.title}, content={self.content}, username_key={self.username_key}>"