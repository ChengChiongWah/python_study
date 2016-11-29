from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from model import User
from model import Weibo
from model import Comments


user = Blueprint('user', __name__)



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
    weibos = Weibo.query.limit(20).all()
    comments = Comments.query.limit(20).all()
    return render_template('index.html', login_status=login_status, username=username,
                             weibos=weibos, comments=comments)

@user.route('/weibo', methods=['POST'])
def weibo():
    form = request.form
    weibo = Weibo(form)
    weibo.add()
    return redirect(url_for('index'))


@user.route('/comments/', methods=['GET'])
def comments():
    return render_template('comments.html')


@user.route('/comments/', methods=['POST'])
def comments_add():
    form = request.form
    comment = Comments(form)
    weibo_id = request.args.get('weibo_id')
    comment.add(int(weibo_id))
    return redirect(url_for('index'))
