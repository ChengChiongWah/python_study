from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.security_key = 'just check once'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

db = SQLAlchemy(app)

formate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    register_time = db.Column(db.String)


    def __init__(self, form):
        self.username = form.get('username_register')
        self.password = form.get('password_register')
        self.register_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

    def add(self):
        db.session.add(self)
        db.session.commit()


class Weibo(db.Model):
    __tablename__ = 'weibo'
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text)
    create_time = db.Column(db.String)

    def __init__(self, form):
        self.contents = form.get('weibo_contents')
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def load_comment(self):
        self.comments = Comments.query.filter_by(weibo_id=self.id).all()
        return self.comments


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.Text)
    create_time = db.Column(db.String)
    # comments_author = db.Column(db.String)
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.contents = form.get('comments_contents', '')
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

    def add(self, weibo_id):
        self.weibo_id = weibo_id
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    # weibos = Weibo.query.limit(10).all()
    # for weibo in weibos:
    #     print(weibo.id, weibo.contents)
