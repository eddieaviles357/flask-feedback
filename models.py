from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

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

    def __repr__(self):
        return f"<User username={self.username}, pswrd={self.password}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}" >

    @classmethod
    def register_user(cls, username, pswrd):
        """ Register User w/hashing password """
        hashed_pswrd = bcrypt.generate_password_hash(pswrd)
        # turn to bytestring to normal unicode utf8 string
        hashed_pswrd_utf8 = hashed_pswrd.decode('utf8')
        # return instance of user with hashed pswrd
        return cls(username=username, password=hashed_pswrd_utf8)
