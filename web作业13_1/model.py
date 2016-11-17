from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import os

app = Flask(__name__)
app.secret_key = 'hard guest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

db = SQLAlchemy(app)

class message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key = True)
    message_content = db.Column(db.Text)
    create_time = db.Column(db.String)

    def __init__(self):
        self.message_content = form.get('message_content')
        self.create_time = time.strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print(os.getcwd() +'\sqlite.db')