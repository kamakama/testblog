from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(80))
    email = db.Column('email', db.String(50), index=True)
    avatar = db.Column('avatar', db.String(255))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    registered_on = db.Column('registered_on' , db.DateTime)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, password, email=None):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self, pw):
        self.password = generate_password_hash(pw, method='sha256')

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
