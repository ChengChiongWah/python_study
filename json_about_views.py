#!/usr/bin/env python3.5
# coding:utf-8

from . import admin
from .. import db, csrf
from .log import Log
from ..models import Bjf_admin_user, Bjf_invest_project, Bjf_users
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
import json

@admin.route('/admin_login_view', methods=['GET'])
def admin_login_view():
    return render_template('admin_login.html')


@admin.route('/admin_login', methods=['POST'])
def admin_login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    user = Bjf_admin_user.query.filter_by(name=username).first()
    if user and user.verify_password(password):
        login_user(user)
        print(current_user.name)
        return redirect(url_for('admin.admin_information'))
    else:
        return redirect(url_for('admin.admin_login_view'))


@admin.route('/admin_information', methods=['GET', 'POST'])
@login_required
def admin_information():
    return render_template('admin_information.html')



@admin.route('/admin_add_user', methods=['GET'])
# @login_required
def admin_add_user():
    return render_template('admin_user_add.html')

@admin.route('/admin_user_add', methods=['GET','POST'])
@login_required
def admin_user_add():
    try:
        strf = request.form
        dictvl = dict(strf)
        user = dictvl['user'][0]
        password = dictvl['pwd'][0]
        admin_user_email = dictvl['email'][0]
        admin_user = Bjf_admin_user(user, password, admin_user_email)
        Bjf_admin_user.save(admin_user)
        return ('200')
    except:
        return ('error')


@admin.route('/admin_logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin.admin_login_view'))


@admin.route('/admin_user_query_conditions')
@login_required
def admin_user_query_conditions():
    pass


@admin.route('/admin_user_query_all', methods=['GET', 'POST'])
@login_required
def admin_user_query_all():
    if request.method == 'POST':
        admin_user_all = Bjf_admin_user.query.with_entities(Bjf_admin_user.name, Bjf_admin_user.email).all()
        admin_user_all_list = []
        for a in admin_user_all:
            tmp = {}
            tmp['username'] = a.name
            tmp['email'] = a.email
            admin_user_all_list.append(tmp)
        admin_user_all_json = json.dumps({'data': admin_user_all_list}) # 封装成json格式
        return admin_user_all_json
    else:
        return render_template('admin_user_list.html')


@admin.route('/front_user_query_conditions')
@login_required
def admin_front_user_query_conditions():
    pass


@admin.route('/front_user_query_all', methods=['GET', 'POST'])
# @login_required
def admin_front_user_query_all():
    if request.method == 'POST':
        print(request.method)
        front_user_all = Bjf_users.query.with_entities(Bjf_users.username, Bjf_users.gender, Bjf_users.phone,
                                                       Bjf_users.email, Bjf_users.remark, Bjf_users.created_time).all()
        front_user_all_list = []
        for f in front_user_all:
            tmp = {}
            tmp['username'] = f.username
            tmp['gender'] = f.gender
            tmp['phone'] = f.phone
            tmp['email'] = f.email
            tmp['remark'] = f.remark
            tmp['created_time'] = f.created_time
            front_user_all_list.append(tmp)
        front_user_all_json = json.dumps({'data': front_user_all_list}) # 封装成json格式
        return front_user_all_json
    else:
        return render_template('front_user_list.html')


@admin.route('/project_query_conditions')
@login_required
def admin_project_query_conditions():
    pass


@admin.route('/project_query_all', methods=['GET', 'POST'])
@login_required
def admin_project_query_all():
    if request.method == 'POST':
        project_all = Bjf_invest_project.query.with_entities(Bjf_invest_project.prj_name, Bjf_invest_project.founder, Bjf_invest_project.prj_amount,
                                                       Bjf_invest_project.status, Bjf_invest_project.remark).all()
        project_all_list = []
        for p in project_all:
            tmp = {}
            tmp['name'] = p.prj_name
            tmp['founder'] = p.founder
            tmp['prj_amount'] = p.prj_amount
            tmp['status'] = p.status
            tmp['remark'] = p.remark
            project_all_list.append(tmp)
        project_all_json = json.dumps({'data':project_all_list}) # 封装成json格式
        return project_all_json
    else:
        return render_template('***.html')