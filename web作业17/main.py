from flask import Flask
from flask import render_template
from user import user

"""
作业  微博功能类似blog 新增一个用户注册 多用户发表微博的功能
"""

app = Flask(__name__)
app.register_blueprint(user, url_prefix='/user')

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
