"""
2016/11/03


web 8 作业
以上课板书为基础



1, 补全 edit 和 update 两个路由函数
加上权限控制功能, 如果权限不足, 重定向到 /todo/index



2, 给 Todo 类增加一个 created_time 属性
它保存的是创建数据的 unix 时间, int 类型
简单说来就是 int(time.time())



3, 给 Todo 类增加一个 updated_time 属性
它保存的是修改数据的时间



4, 在 /todo/index 界面上显示创建和修改事件, 格式如下(24小时制)
11/02 10:31



5, 增加一个路由 /admin/users
只有 id 为 1 的用户可以访问这个页面, 其他用户访问会定向到 /login
这个页面显示了所有的用户 包括 id username password



6, 在 /admin/users 页面中新增一个表单
表单包括 id password 两个 input
管理员可以在这个表单中输入 id 和 新密码 来修改相应用户的密码
这个表单发送 POST 请求到 /admin/user/update
所以你要增加一个新的路由函数



7, 给用户增加一个 role 属性, int 类型, 默认是 10
把管理页面的权限验证换成 role 为 1 的人是管理员

"""