from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from functools import wraps
from model import User
from model import Weibo
from model import Comments


user = Blueprint('user', __name__)


def current_user():
    user_id = session.get('user_id', '')
    u = User.query.filter_by(id=user_id).first()
    return u


def login_require(f):
    @wraps(f)
    def functions(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('index'))
        else:
            return f(*args, **kwargs)
    return functions


@user.route('/index', methods=['GET'])
def index():
    if request.cookies:
        username = request.args.get('username')
        weibos = Weibo.query.limit(20).all()
        return render_template('login/weibo.html', weibos=weibos, username=username)
    else:
        return redirect(url_for('index'))


@user.route('/register', methods=['POST'])
def register():
    form = request.form
    user = User(form)
    user.add()
    return redirect(url_for('index'))


@user.route('/login', methods=['POST'])
def login():
    if request.form.get('username'):
        username = request.form.get('username')
        password_register = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if password_register == user.password:
            session['user_id'] = user.id
    return redirect(url_for('user.index', username=username))



@user.route('/weibo/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@user.route('/weibo', methods=['POST'])
@login_require
def weibo():
    if request.form.get('weibo_contents'):
        form = request.form
        weibo = Weibo(form)
        weibo.add()
        username = request.args.get('username')
    else:
        username = request.args.get('username')
        flash('Please input weibo contents')
    return redirect(url_for('user.index', username=username))


@user.route('/comments', methods=['GET'])
@login_require
def comments():
    weibo_id = request.args.get('weibo_id')
    username = request.args.get('username')
    return render_template('login/comments.html', weibo_id=int(weibo_id), username=username)


@user.route('/comments/add', methods=['POST'])
def comments_add():
    if request.cookies:
        if request.form.get('comments_contents'):
            form = request.form
            comment = Comments(form)
            weibo_id = request.args.get('weibo_id')
            username = request.args.get('username')
            comment.add(int(weibo_id))
        else:
            username = request.args.get('username')
        return redirect(url_for('user.index', username=username))
    else:
        return redirect(url_for('index'))


