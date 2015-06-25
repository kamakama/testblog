from flask import render_template, flash, redirect, url_for, request, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
import imghdr
import os
from datetime import datetime
from functools import wraps
from app import app, db, lm, avatars
from .forms import LoginForm, RegisterForm, AvatarForm, EditForm
from .models import User


@app.route('/test')
def testroute():
    u1 = User.query.filter_by(username='pascasl').first()
    u2 = User.query.get(int('17'))
    print(u1)
    return "abc"


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'nickname': 'test1'},
            'body': 'abc!'
        },
        {
            'author': {'nickname': 'test2'},
            'body': 'def!'
        }
    ]
    return render_template("index.html", title='Home', user=current_user, posts=posts)


@lm.user_loader
def load_user(id):
    user = User.query.get(int(id))
    return user

@app.route('/register' , methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', title='Register', form=form)
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('User already exists')
            return render_template('register.html', title='Register', form=form)
        user = User(form.username.data, form.password.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))
    flash('Invalid password. Try again')
    return render_template('register.html', title='Register', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if not user.check_password(password):
                flash('Wrong password')
                return render_template('login.html', title='Sign In', form=form)
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            return redirect(next or url_for('user', name=username))
        flash('Invalid username. Try again')
    return render_template('login.html', title='Sign In', form=form)
    

@app.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(username=name).first()
    if user is None:
        flash('User %s not found.' % name)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', title=name, user=user, posts=posts)
    
    
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = AvatarForm()
    if request.method == 'GET':
        return render_template('upload.html', form=form)
    if form.validate_on_submit():
        if request.content_length > (1 * 1024 * 1024):
            flash('File too big (max 1 MB)')
            return render_template('upload.html', form=form)
        filename = avatars.save(form.avatar.data)
        if imghdr.what(avatars.path(filename)):
            user = User.query.filter_by(username=g.user.username).first()
            if user.avatar:
                os.remove(avatars.path(user.avatar))
            user.avatar = filename
            db.session.commit()
            flash('Avatar saved.')
            return redirect(url_for('index'))
        else:
            os.remove(avatars.path(filename))
    flash('Invalid file.')
    return render_template('upload.html', form=form)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)
    
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
