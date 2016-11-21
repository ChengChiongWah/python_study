from flask import request
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from model import User

registers = Blueprint('registers', __name__)


@registers.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@registers.route('/login', methods=['GET', 'POST'])
def login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    user = User.query.filter_by(name=username).first()
    if user:
        if user.name == username and user.password == password:
            return "login Sucessful!"
    else:
        return redirect(url_for('registers.index'))


@registers.route('/register/', methods=['POST'])
def register():
    form = request.form
    user = User(form)
    user.save()
    return redirect(url_for('registers.index'))
