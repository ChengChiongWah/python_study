from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from model import User


user = Blueprint('user', __name__)



@user.route('/register', methods=['POST'])
def register():
    form = request.form
    user = User(form)
    user.add()
    return redirect(url_for('index'))

@user.route('/login', methods=['POST'])
def login():
    if request.form('username') and request.form('password'):
        username = request.form('username')
        password_register = request.form('password')
        user = User.query.filter_by(username=username)
        if password_register == user.password:
