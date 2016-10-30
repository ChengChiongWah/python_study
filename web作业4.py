# 2016/10/25
#
# ========
# 作业 4
# ========
#


# 1
#
# 写一个 HTML form, 它会发送如下的 HTTP 请求给服务器
'''
POST /login HTTP/1.1
Host: localhost

username=gua&password=123
'''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>web作业4</title>
    </head>
    <body>
         <form action="The Path of URL" method="post">
            <input type="text" name="name" />
            <input type="password" name="password" />
            <input type="Submit" value="Submit" />
        </form>
    </body>
</html>


# 2
# 根据上课用的 Request 类
# 写出下面这个请求的 method path query headers form()
'''
POST /register?id=1 HTTP/1.1
Host: localhost
Content-Type: x-www-form-urlencoded

username=gua&password=1%2023
'''
method ="POST"
path = "/register"
query = {username:gua,password:1}
headers ="POST /register?id=1 HTTP/1.1\r\n\r\nHost: localhost\r\n\r\nContent-Type: x-www-form-urlencoded\r\n\r\n\r\nusername=gua&password=1%2023"
form={username:gua,password:1}

# 3
# 熟读 Python 学习手册中关于 类 的章节
# 下节课开始要大量使用 类