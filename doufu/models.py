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
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True) #名称
    introduce = db.Column(db.Text) #简介
    pictures = db.Column(db.String) #保留图片路径
    tips = db.Column(db.Text) #小贴士
    author = db.Column(db.Text) #菜谱的发布者
    materials = db.relationship('Material', backref='recipe', foreign_keys='Material.recipe_id', lazy='dynamic')
    steps = db.relationship('Step', backref='recipe', foreign_keys='Step.recipe_id', lazy='dynamic')
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

    def update(self, form, path):
        self.name = form.get('name') or self.name
        self.introduce = form.get('introduce') or self.introduce
        self.pictures = path or self.pictures
        self.tips = form.get('tips') or self.tips
        db.session.commit()


    def delete_element(self):
        db.session.delete(self)
        db.session.commit()


class Material(db.Model): #用料
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Integer) #数量
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

    def __init__(self, material_name, amount, recipe_id):
        self.name = material_name
        self.amount = amount
        self.recipe_id = recipe_id


    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, material_name, amount_value):
        self.name = material_name
        self.amount = amount_value
        db.session.commit()

    def delete_element(self):
        db.session.delete(self)
        db.session.commit()


class Step(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, unique=True)
    technique = db.Column(db.Integer) #步骤方法
    pictures = db.Column(db.String) #步骤图
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id')) #对应的菜谱名

    def __init__(self, step_number, technique, pictuees, recipe_id):
        self.step_number = step_number
        self.technique = technique
        self.pictures = pictuees
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
        db.session.delete(self)
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
    r = Recipe.query.limit(10).all()
    for m in range(0, len(r)):
        print(r[m].name)
        for i in r[m].materials.all():
            print (''*10, i.name, i.amount)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    test()

