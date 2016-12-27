from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_login import login_user, logout_user, login_required
from functools import wraps
from . import auth
from ..models import User


def current_user():
    username = session.get('username', '')
    u = User.query.filter_by(name=username).first()
    return u


def login_require(f):
    @wraps(f)
    def functions(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('main.index'))
        else:
            f(*args, **kwargs)
    return functions


@auth.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')


@auth.route('/register/add', methods=['POST'])
def register_add():
    form = request.form
    user = User(form)
    user.add()
    return redirect(url_for('auth.login_view'))


@auth.route('/login_view', methods=['GET'])
def login_view():
    return render_template('login.html')

@auth.route('/login', methods=['post'])
def login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    user = User.query.filter_by(name=username).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        return redirect(url_for('auth.login_view'))

@auth.route('/login')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))