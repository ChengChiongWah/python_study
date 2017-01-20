#!/usr/bin/env python3
# coding:utf-8
from flask import current_app
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
from . import login_manager
import time
import os

uploads_dir = 'app/static/images/'


def formatetime():  # 给出时间格式
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))


class Recipe(db.Model):  # 菜谱
    __tablename__ = 'recipes'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.Text(20))  # 名称
    introduce = db.Column(db.Text(100))  # 简介
    pictures = db.Column(db.String(50))  # 保留图片路径
    author = db.Column(db.Text(20))  # 菜谱发布者
    tips = db.Column(db.Text(100))  # 小贴士
    materials = db.relationship('Material', backref='recipe', foreign_keys='Material.recipe_id', lazy='dynamic')
    steps = db.relationship('Step', backref='recipe', foreign_keys='Step.recipe_id', lazy='dynamic')
    questions = db.relationship('Questions', backref='recipe', foreign_keys='Questions.recipe_id', lazy='dynamic')
    create_time = db.Column(db.String(20))

    def __init__(self, form, filename, tips):
        self.name = form.get('name')
        self.introduce = form.get('introduce')
        self.pictures = filename
        self.tips = tips
        self.author = current_user.name
        self.create_time = formatetime()

    def add(self):
        db.session.add(self)
        db.session.commit()  # 先commit获得recipe对应id
        oldname = self.pictures
        os.rename(uploads_dir + oldname, uploads_dir + 'recipe_' + str(self.id) + '_' + oldname)  # 对上传的文件更改文件名
        self.pictures = 'static/images/recipe_' + str(self.id) + '_' + oldname  # 转成路径格式
        db.session.commit()

    def update(self, form, filename):
        self.name = form.get('name') or self.name
        self.introduce = form.get('introduce') or self.introduce
        self.pictures = filename or self.pictures
        self.tips = form.get('tips') or self.tips
        db.session.commit()

    def delete_element(self):
        if self.pictures:  # 删除文件
            os.remove('app/' + self.pictures)
        db.session.delete(self)
        db.session.commit()


class Material(db.Model):  # 用料
    __tablename__ = 'materials'
    id = db.Column(db.INT, primary_key=True)
    material_number = db.Column(db.INT)
    name = db.Column(db.Text(20))
    amount = db.Column(db.String(20))  # 数量
    recipe_id = db.Column(db.INT, db.ForeignKey('recipes.id'))

    def __init__(self, material_number, material_name, amount, recipe_id):
        self.material_number = int(material_number)
        self.name = material_name
        self.amount = amount
        self.recipe_id = recipe_id

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, material_name, amount_value):
        self.name = material_name or self.name
        self.amount = amount_value or self.amount
        db.session.commit()

    def delete_element(self):
        db.session.delete(self)
        db.session.commit()


class Step(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.INT, primary_key=True)
    step_number = db.Column(db.INT)
    technique = db.Column(db.String(150))  # 步骤方法
    pictures = db.Column(db.String(100))  # 步骤图
    recipe_id = db.Column(db.INT, db.ForeignKey('recipes.id'))  # 对应的菜谱名

    def __init__(self, step_number, technique, filename, recipe_id):
        self.step_number = step_number
        self.technique = technique
        self.pictures = filename
        self.recipe_id = recipe_id

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, step_number, technique, pictures):
        self.step_number = step_number or self.step_number
        self.technique = technique or self.technique
        self.pictures = pictures or self.pictures
        db.session.commit()

    def delete_element(self):
        if self.pictures:
            os.remove('app/' + self.pictures)
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text(100))
    email = db.Column(db.String(30), unique=True)
    picture = db.Column(db.String(100))
    role_id = db.Column(db.INT)
    create_time = db.Column(db.String(30))

    def __init__(self, form):
        self.name = form.get('username', '')
        self.password = generate_password_hash(form.get('password', ''))
        self.email = form.get('email', '')
        self.picture = 'static/images/users_pictures/user_default.jpg'
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.Config['SECRIT_KEY'], expiration)
        return s.dumps({'email': self.email})

    def confirm(selfself, token):
        s = Serializer(current_app.Config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('email') != self.email:
            return False

    def pwd_update(self, pwd):
        self.password = generate_password_hash(pwd)
        db.session.commit()

    def picture_update(self, filename):
        self.picture = filename
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):  # flask-login扩展加载用户的回调函数
    return User.query.get(int(user_id))


class Questions(db.Model):
    '''
    菜谱的留言信息
    '''
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(100))  # 留言内容
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))  # 留言的菜谱id
    author = db.Column(db.String(30))  # 留言作者
    create_time = db.Column(db.String(20))  # 留言时间

    def __init__(self, content, recipe_id, author):
        self.content = content
        self.recipe_id = recipe_id
        self.author = author
        self.create_time = formatetime()

    def add(self):
        db.session.add(self)
        db.session.commit()


class Debug(db.Model):
   __tablename__ = 'debug'
   id = db.Column(db.Integer, primary_key=True)
   debug_content = db.Column(db.Text(150))
   confirmed = db.Column(db.Boolean, default=False)
   create_time = db.Column(db.String(20))

   def __init__(self, debug_content):
       self.debug_content = debug_content
       self.create_time = formatetime()

   def add(self):
       db.session.add(self)
       db.session.commit()

   def debug_confirmed_update(self, signal):
       self.confirmed = signal
       db.session.commit()

   def debug_delete(self):
       db.session.delete(self)
       db.session.commit()
 
