"""
实现一个用户登录注册的功能
不要求使用 session 和 cookie(下节课才学怎么在 flask 中用)

包含以下文件
models.py 是 model 文件, 包含 User 类
templates/login.html 是登录/注册页面模板文件
routes_user.py 是一个蓝图, 包含下面三个路由
	GET /login		返回登录界面, 这个界面包含两张表单分别用来登录或者注册
    POST /login		登录表单提交地址
    POST /register	注册表单提交地址

仿造上课用品豪华版的 todo.py 文件内容
"""

from flask import Flask
from routes_user import registers

app = Flask(__name__)


app.register_blueprint(registers, url_prefix='/registers')


@app.route('/')
def index():
    return "index page"

if __name__ == '__main__':
    app.run()