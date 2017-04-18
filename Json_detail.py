接受json数据：

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


2.
发送接送数据


@admin.route('/front_user_query_all', methods=['GET', 'POST'])
@login_required
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
