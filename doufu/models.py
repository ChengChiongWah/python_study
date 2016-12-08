from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.security_key = 'The Python Language 3.5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

def formatetime(): #给出时间格式
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

class Recipe(db.Model): #菜谱
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True) #名称
    introduce = db.Column(db.Text) #简介
    pictures = db.Column(db.String) #保留图片路径
    author = db.Column(db.Text) #菜谱的发布者
    create_time = db.Column(db.String)


    def __init__(self, form, path):
        self.name = form.get('name')
        self.introduce = form.get('introduce')
        self.pictures = path
        self.create_time = formatetime()

    def add(self):
        db.session.add(self)
        db.session.commit()


class Material(db.Model): #用料
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    amount = db.Column(db.Integer) #数量
    recipe_id = db.Column(db.Integer)


class Steps(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, unique=True)
    technique = db.Column(db.Integer) #方法
    tips = db.Column(db.Text) #小贴士
    recipe_number = db.Column(db.Integer) #对应的菜谱ID


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
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


