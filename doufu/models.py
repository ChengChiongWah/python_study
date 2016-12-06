from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.security_key = 'The Python Language 3.5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

# formate_time = time.strftime('%Y-%m-%d %h:%M:%S', time.localtime(int(time.time())))
# formate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
# time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))


class Doufu(db.Model):
    __tablename__ = 'doufu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text) #名称
    introduce = db.Column(db.Text) #简介
    material = db.Column(db.Text) #用料
    methods = db.Column(db.Text) #做法
    pictures = db.Column(db.String) #保留图片路径
    create_time = db.Column(db.String)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    create_time = db.Column(db.String)

    def __init__(self, form):
        self.name = form.get('username', '')
        self.password = form.get('password', '')
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

    def add(self):
        db.session.add(self)
        db.session.commit()



if __name__ == '__main__':
    db.drop_all()
    db.create_all()


