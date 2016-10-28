"""
2016/10/23

作业 3

请参考上节课的作业
"""
import socket

# 1
# 利用上节课作业中的函数 parsed_url 改写 get 函数
# 让 get 函数支持自动根据协议/端口使用相应的端口
def get(url):
    """
    https://movie.douban.com/top250
    p = https
    u = movie.douban.com/top250
    """
    # p, u = url.split('://')
    if url[:8] == "https://":  # https://协议
        protocol = "https"
        url = url[8:]
    elif url[:7] == "http://":  # 标明是http
        protocol = "http"
        url = url[7:]
    else:  # 没有标明protocol时
        protocol = "http"

    if url[:].find(":") == -1:  # g.cn
        if protocol == "https":
            port = 443
        else:
            port = 80
        if url.find("/") == -1:
            host = url[:]
            path = "/"
        else:
            url_end = url[:].find("/")
            host = url[:url_end]
            path = url[url_end:]

    else:  # g.cn:300
        host_end = url.find(":")
        host = url[:host_end]
        url = url[host_end + 1:]
        if url[:].find("/") == -1:  # g.cn:3000
            port = int(url[:])
            path = "/"
        else:  # g.cn:3000/abc
            port_end = url[:].find("/")
            port = int(url[:port_end])
            path = url[port_end:]

    # port = 443
    # s = ssl.wrap_socket(socket.socket())
    s = socket.socket()

    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nGua: 好\r\n\r\nname=gua'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    return response.decode(encoding)



# 2
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""
# encoding: utf-8

import socket
import ssl
def get_url(url):
    """
    https://movie.douban.com/top250
    p = https
    u = movie.douban.com/top250
    """
    # p, u = url.split('://')
    if url[:8] == "https://":  # https://协议
        protocol = "https"
        url = url[8:]
    elif url[:7] == "http://":  # 标明是http
        protocol = "http"
        url = url[7:]
    else:  # 没有标明protocol时
        protocol = "http"

    if url[:].find(":") == -1:  # g.cn
        if protocol == "https":
            port = 443
        else:
            port = 80
        if url.find("/") == -1:
            host = url[:]
            path = "/"
        else:
            url_end = url[:].find("/")
            host = url[:url_end]
            path = url[url_end:]

    else:  # g.cn:300
        host_end = url.find(":")
        host = url[:host_end]
        url = url[host_end + 1:]
        if url[:].find("/") == -1:  # g.cn:3000
            port = int(url[:])
            path = "/"
        else:  # g.cn:3000/abc
            port_end = url[:].find("/")
            port = int(url[:port_end])
            path = url[port_end:]

    return protocol, host, path, port

def socket_connect(protocol):
    if protocol == "https":
        s = ssl.wrap_socket(socket.socket())
    else:
        s = socket.socket()
    return s

def movie(url):
    protocol, host, path, port = get_url(url)
    s = socket_connect(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nconnect:close\r\n\r\n'.format(path, host)
    s.send(request.encode("utf_8"))

    response = b""
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    result = response.decode("utf-8")
    return result


def movie_analyse(result):
    movie = result
    title = ""
    while True:
        if movie.rfind('<div class="item">') == -1:     #从结果的尾部开始分析，每分析完一部就截掉改部分信息。
            break
        else:
            movie_begin = movie.rfind('<div class="item">')
            movie_temp = movie[movie_begin:]
            movie = movie[:movie_begin]

            movie_title_begin = movie_temp.find('<div class="hd">')        #标题部分index
            movie_temp = movie_temp[movie_title_begin:]
            movie_title_end = movie_temp.find("</a>")
            movie_title = movie_temp[:movie_title_end]           #有title信息的部分
            while True:
                if movie_title.rfind("</span>") == -1:
                    break
                else:
                    title_inf_end = movie_title.rfind("</span>")
                    title_inf_begin = movie_title.rfind('">')
                    title += movie_title[title_inf_begin+2:title_inf_end]
                    movie_title = movie_title[ :title_inf_begin]

            movie_star_begin = movie_temp.find('average">')        #评分
            movie_temp = movie_temp[movie_star_begin:]
            movie_star_end = movie_temp.find('</span>')
            movie_star = movie_temp[9:movie_star_end]
            movie_temp = movie_temp[movie_star_end:]

            movie_judgement_begin = movie_temp.find("<span>")       #评价
            movie_judgement_end = movie_temp.find("</span>")
            movie_judgement = movie_temp[movie_judgement_begin+6:movie_judgement_end]
            movie_temp = movie_temp[movie_judgement_end:]

            if movie_temp.find("<span>") == -1:
                movie_eyes =""
            else:
                movie_eyes_begin = movie_temp.find('class="inq">')
                movie_eyes_end = movie_temp.find('</span>')
                movie_eyes = movie_temp[movie_eyes_begin+12:]

    title = title.replace("&nbsp;","")
    print(title, '\n', movie_star, '\n', movie_judgement, '\n', movie_eyes)



def main():
    url = 'https://movie.douban.com/top250'
    result = movie(url)
    movie_analyse(result)
#    print(movie(url))
 #   print(type(movie(url)))
 #   status_code, headers, body = get(url)
#    print(status_code, headers, body)

if __name__ == '__main__':
    main()


# 3
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好
"""



