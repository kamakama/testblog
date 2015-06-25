from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, validators
from wtforms.fields.html5 import EmailField
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from app import avatars

class LoginForm(Form):
    username = TextField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
    username = TextField('Username', [validators.InputRequired(), validators.Length(min=4, max=20)])
    email = EmailField('Email')
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=4),
        validators.EqualTo('confirm', message='Passwords don\'t match')
    ])
    confirm = PasswordField('Password', [validators.InputRequired()])
    
class AvatarForm(Form):
    avatar = FileField('Avatar', [
        FileRequired(),
        FileAllowed(avatars, 'Images only!')
    ])

class EditForm(Form):
    about_me = TextAreaField('about_me', [validators.Length(min=0, max=140)])