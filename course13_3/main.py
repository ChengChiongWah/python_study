"""
实现一个用户管理界面
步骤如下
1, 往用户表中随机灌 50 条记录
2, 创一个 /admin/user 路由, 显示用户列表
3, 每页显示 10 条数据, 通过 /admin/user?page=1 这个参数来控制当前页
4, 如果没有 page 参数, 则默认 page 为 1
5, 页面中要有上一页/下一页和所有你能点击的页码(本例中是这样的  上一页 1 2 3 4 5 下一页)
6, 第一页中 上一页不是超链接是文本, 最后一页中, 下一页不是超链接是文本

"""

from flask import Flask
from admin import admin

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    app.run()