#!/usr/bin/env python3
# coding:utf-8
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from . import main
from ..models import Recipe, Debug
from ..log import Log


@main.route('/', methods=['GET'])
def index():
    res = Recipe.query.all()
    page_number = len(res) // 5
    if len(res)%5 != 0: #不是5的整数倍的话加多1
        page_number += 1
    if request.args.get('page') is None:
        page = 1
        pagination = Recipe.query.paginate(page, 5, False)
        pageitems = pagination.items
    else:
        page = int(request.args.get('page'))
        pagination = Recipe.query.paginate(page, 5, False)
        pageitems = pagination.items
    Log.log(page_number)
    return render_template('index.html', pageitems=pageitems, pagination=pagination, page=page, res=res,
                           page_number=page_number)


@main.route('/debgu_information', methods=['GET'])
def debugs():
    debugs = Debug.query.all()
    return render_template('debugs_information.html', debugs=debugs)


@main.route('/debug_add', methods=['POST'])
def debugs_add():
    form = request.form
    debug_content = form.get('debug_content')
    debug = Debug(debug_content)
    debug.add()
    return redirect(url_for('main.debugs'))


@main.route('/debug_confirm', methods=['GET'])
def debugs_confirm():
    id = request.args.get('id')
    debug = Debug.query.filter_by(id=int(id)).first()
    debug.debug_confirmed_update(True)
    return redirect(url_for('main.debugs'))

@main.route('/debug_delete', methods=['GET'])
def debugs_delete():
    id = request.args.get('id')
    debug = Debug.query.filter_by(id=int(id)).first()
    debug.debug_delete()
    return redirect(url_for('main.debugs'))


@main.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template('contact_us.html')
