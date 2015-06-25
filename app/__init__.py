import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

avatars = UploadSet(name='avatars', extensions=IMAGES)
configure_uploads(app, [avatars])
#patch_request_class(app, 1 * 1024 * 1024)
    

from app import views, models

"""
@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    u = models.User(username='pascal', email='pascal@pascal.com', password='pw')
    db.session.add(u)
    db.session.commit()
"""
