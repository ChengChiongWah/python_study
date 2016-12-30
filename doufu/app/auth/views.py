from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_login import login_user, logout_user, login_required
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import Config
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


@auth.route('/forget', methods=['GET'])
def forget_pwd():
    return render_template('forget.html')


@auth.route('/send_mail_view', methods=['post'])
def send_mail_view():
    recive_mail = request.form.get('email')
    send_mail(recive_mail)
    return redirect(url_for('auth.login'))

@auth.route('/token_check')
def token_check():
    token = request.arges.get('token')
    s = Serializer(Config['SECRET_KEY'], expires_in=3600)
    token_data = s.load(token) #对token解码成对应的值
    if token_data:
        return redirect(url_for('auth.pwd_update_view', token_data=token_data['email'] ))
    else:
        return redirect(url_for('auth.send_mail_view'))


@auth.route('/pwd_update_view')
def pwd_update_view():
    return render_template('pwd_update.html')


@auth.route('/pwd_update')
def pwd_update():
    email = request.arg.get('token_data')
    user = User.query.filter_by(email=email).first()
    form = request.form
    pwd = form.get('password')
    if pwd:
        user.pwd_update(pwd)
    return redirect(url_for('auth.login'))



def send_mail(reciver_mail):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    s = Serializer(Config['SECRET_KEY'], expires_in = 3600)
    token = s.dumps({'email':reciver_mail})

    sender = 'sguzch@163.com'
    subject = '放假通知'
    mail_content = '<html><body><a href="' + url_for('auth.token_check', token=token, _external=True) + '">click here</a></body></html>'
    smtpserver = 'smtp.163.com'
    username = 'sguzch@163.com'
    password = 'wywywywy2013'

    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'zhengch<sguzch@163.com>'
    msg['To'] = reciver_mail
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, reciver_mail, msg.as_string())
    smtp.quit()