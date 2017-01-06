from flask import current_app
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
from . import login_manager
import time
import os

uploads_dir = 'static/images/'

def formatetime(): #给出时间格式
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))


class Recipe(db.Model): #菜谱
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text) #名称
    introduce = db.Column(db.Text) #简介
    pictures = db.Column(db.String) #保留图片路径
    tips = db.Column(db.Text) #小贴士
    author = db.Column(db.Text) #菜谱的发布者
    materials = db.relationship('Material', backref='recipe', foreign_keys='Material.recipe_id', lazy='dynamic')
    steps = db.relationship('Step', backref='recipe', foreign_keys='Step.recipe_id', lazy='dynamic')
    create_time = db.Column(db.String)


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
        os.rename(uploads_dir+oldname, uploads_dir+'recipe_'+str(self.id)+'_'+oldname) # 对上传的文件更改文件名
        self.pictures = 'static/images/recipe_' + str(self.id) + '_' + oldname #转成路径格式
        db.session.commit()

    def update(self, form, filename):
        self.name = form.get('name') or self.name
        self.introduce = form.get('introduce') or self.introduce
        self.pictures = filename or self.pictures
        self.tips = form.get('tips') or self.tips
        db.session.commit()

    def delete_element(self):
        if self.pictures: #删除文件
            os.remove(self.pictures)
        db.session.delete(self)
        db.session.commit()


class Material(db.Model): #用料
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    material_number = db.Column(db.Integer)
    name = db.Column(db.Text)
    amount = db.Column(db.Integer) #数量
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))

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
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer)
    technique = db.Column(db.Integer) # 步骤方法
    pictures = db.Column(db.String) # 步骤图
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id')) # 对应的菜谱名

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
            os.remove(self.pictures)
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    email = db.Column(db.String, unique=True)
    role_id = db.Column(db.Integer)
    create_time = db.Column(db.String)

    def __init__(self, form):
        self.name = form.get('username', '')
        self.password = generate_password_hash(form.get('password', ''))
        self.email = form.get('email', '')
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))

    def add(self):
        db.session.add(self)
        db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.Config['SECRIT_KEY'], expiration)
        return s.dumps({'email':self.email})

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

@login_manager.user_loader
def load_user(user_id):  #flask-login扩展加载用户的回调函数
    return User.query.get(user_id)

def test():
    steps = Step.query.with_entities(Step.step_number).filter_by(recipe_id='1').all()
    print (steps)
    step_numbers = [s[0] for s in steps]
    # for s in steps:
    #     step_numbers.append(s[0])
    #     print(s)
    print(step_numbers)



