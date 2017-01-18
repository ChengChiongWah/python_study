#!/usr/bin/env python3
# coding:utf-8
from flask import render_template, request
from flask_login import current_user
from . import main
from ..models import Recipe
from ..log import Log


@main.route('/', methods=['GET'])
def index():
    res = Recipe.query.all()
    page_number = len(res) // 5
    if len(res) /5 is not int: #不是5的整数倍的话加多1
        page_number += 1
    if request.args.get('page') is None:
        page = 1
        pagination = Recipe.query.paginate(page, 5, False)
        pageitems = pagination.items
    else:
        page = int(request.args.get('page'))
        pagination = Recipe.query.paginate(page, 5, False)
        pageitems = pagination.items
    return render_template('index.html', pageitems=pageitems, pagination=pagination, page=page, res=res,
                           page_number=page_number)


@main.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template('contact_us.html')
