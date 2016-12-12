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
    tips = db.Column(db.Text) #小贴士
    author = db.Column(db.Text) #菜谱的发布者
    materials = db.relationship('Material', backref='recipe', lazy='dynamic')
    setps = db.relationship('Step', backref='recipe', lazy='dynamic')
    create_time = db.Column(db.String)


    def __init__(self, form, path, tips):
        self.name = form.get('name')
        self.introduce = form.get('introduce')
        self.pictures = path
        self.tips = tips
        self.create_time = formatetime()

    def add(self):
        db.session.add(self)
        db.session.commit()


class Material(db.Model): #用料
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Integer) #数量
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __init__(self, material_name, amount, recipe_name):
        self.name = material_name
        self.amount = amount
        self.recipe_name = recipe_name

    def add(self):
        db.session.add(self)
        db.session.commit()


class Step(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, unique=True)
    technique = db.Column(db.Integer) #步骤方法
    pictures = db.Column(db.String) #步骤图
    recipe_id = db.Column(db.Text, db.ForeignKey('recipe.id')) #对应的菜谱名

    def __init__(self, step_number, technique, pictuees, recipe_name):
        self.step_number = step_number
        self.technique = technique
        self.pictures = pictuees
        self.recipe_name = recipe_name

    def add(self):
        db.session.add(self)
        db.session.commit()


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

def test():
    recipe = Recipe.query.with_entities(Recipe.name).all()
    for i in recipe:
        print (i)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    test()

