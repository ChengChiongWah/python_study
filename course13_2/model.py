from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time

app = Flask(__name__)
app.secret_key = 'very easy guest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    register_time = db.Column(db.String)

    def __init__(self, form):
        self.name = form.get('username', '')
        self.password = form.get('password', '')
        self.register_time = time.strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return '{}'.format(self.name)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
