from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from models import User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')


@main.route('/register/add', methods=['POST'])
def register_add():
    form = request.form
    user = User(form)
    user.add()
    return redirect(url_for('main.login_view'))


@main.route('/login_view', methods=['GET'])
def login_view():
    return render_template('login.html')

@main.route('/login', methods=['GET'])
def login():
    form = request.form()
    username = form.get('username', '')
    password = form.get('password', '')
    if username:
        user = User.query.filter_by(name=username).first()
        if password == user.password:
            session[user.id] = user.id
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.login_view'))

