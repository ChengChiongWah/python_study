#!/usr/bin/env python3.5
# coding:utf-8
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import current_app
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import auth
from ..models import User, Recipe
from ..recipe.views import allowed_file, upload
import os


# def current_user():
#    username = session.get('username', '')
#    u = User.query.filter_by(name=username).first()
#    return u


# def login_require(f):
#    @wraps(f)
#    def functions(*args, **kwargs):
#        if current_user() is None:
#            return redirect(url_for('main.index'))
#        else:
#            f(*args, **kwargs)
#   return functions


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


@auth.route('/forget', methods=['GET'])
def forget_pwd():
    return render_template('forget.html')


@auth.route('/send_mail_view', methods=['POST'])
def send_mail_view():
    recive_mail = request.form.get('email')
    send_mail(recive_mail)
    return redirect(url_for('auth.login'))


@auth.route('/token_check', methods=['GET'])
def token_check():
    try:
        token = request.args.get('token')
        return redirect(url_for('auth.pwd_update_view', token=token))
    except:
        return redirect(url_for('main.index'))


@auth.route('/pwd_update_view', methods=['GET'])
def pwd_update_view():
    token = request.args.get('token')
    return render_template('pwd_update.html', token=token)


@auth.route('/pwd_update', methods=['POST'])
def pwd_update():
    form = request.form
    token = form.get('token')
    pwd = form.get('password')
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    token_data = s.loads(token)  # 对token解码成对应的值
    email = token_data['email']
    user = User.query.filter_by(email=email).first()
    if user and pwd:
        user.pwd_update(pwd)
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.index'))


@auth.route('/auth_user_information', methods=['GET'])
def user_information():
    username = request.args.get('username')
    user = User.query.filter_by(name=username).first()
    recipe = Recipe.query.filter_by(author=username).all()
    return render_template('user_information.html', user=user, recipe=recipe)


@auth.route('/auth_user_picture_update_view', methods=['GET'])
@login_required
def user_picture_update_view():
    return render_template('user_picture_update.html')


@auth.route('/auth_user_picture_update', methods=['POST'])
@login_required
def user_picture_update():
    form = request.form
    f = request.files.get('picture')
    username = current_user.name
    file_formate = username + '_picture_'
    uploads_dir = './app/static/images/users_pictures/'
    static_images_dir = 'static/images/users_pictures/'
    if f and file_formate:
        if current_user.picture.rsplit('/', 1)[1] == 'user_default.jpg':  # 判断用户的头像是否更改过
            filename = upload(f, file_formate, uploads_dir, static_images_dir)
            current_user.picture_update(filename)
        else:
            os.remove('app/' + current_user.picture)
            filename = upload(f, file_formate, uploads_dir, static_images_dir)
            current_user.picture_update(filename)
    return redirect(url_for('auth.user_information', username=current_user.name))


def send_mail(reciver_mail):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    token = s.dumps({'email': reciver_mail})

    sender = 'chengchiongwah@gmail.com'
    subject = '密码修改邮件'
    mail_content = '<html><body><a href="http://45.32.88.103//token_check?token={}">修改密码链接</a></body></html>'.format(token)
    smtpserver = 'smtp.gmail.com:587'
    username = 'chengtestmail@gmail.com'
    password = 'cttctt2013'

    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'zhengch<chengtestmail@gmail.com>'
    msg['To'] = reciver_mail
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(username, password)
    server.sendmail(sender, reciver_mail, msg.as_string())
    server.quit()
