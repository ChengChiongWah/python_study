from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time

app = Flask(__name__)
app.secret_key = 'very easy guest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

db = SQLAlchemy(app)

class User(object):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    register_time = db.Column(db.String)

    def __init__(self):
        self.register_time = time.strftime('%Y-%m-%d %H:%M:%S')


    def __repr__(self):
        return '{}'.format(self.name)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
