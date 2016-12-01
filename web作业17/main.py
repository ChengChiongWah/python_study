from flask import Flask
from flask import render_template
from user import user
from model import Weibo
from model import Comments

"""
作业  微博功能类似blog 新增一个用户注册 多用户发表微博的功能
"""


app = Flask(__name__)
app.secret_key = 'just check once'
app.register_blueprint(user, url_prefix='/user')


@app.route('/')
def index():
    weibos = Weibo.query.limit(20).all()
    comments = Comments.query.limit(20).all()
    return render_template('index.html', weibos=weibos, comments=comments)


if __name__ == '__main__':
    app.run()
