from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.security_key = 'just check once'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    createtime = db.Column(db.String)

    def __init__(self):
        self.createtime = time.strftime('%Y-%m-%d %H:%M:%S')

    def add(self, name):
        self.name = name
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()