from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request
import time

from model import User

admin = Blueprint('admin', __name__)


@admin.route('/user', methods=['GET'])
def users():
    userall = User.query.all()
    if request.args.get('page') is None:  # 没有提供page值的时候默认为1
        page = 1
        pagination = User.query.paginate(page, 10, False)
        pageitems = pagination.items
    else:
        page = int(request.args.get('page'))
        pagination = User.query.paginate(page, 10, False)  # page 为当前的页码，10是每一页显示的信息条数，True是当没有数据时显示400
        pageitems = pagination.items  # 当前页的所有信息
    return render_template('user.html', pageitems=pageitems, pagination=pagination, page=page, useraall=userall)
