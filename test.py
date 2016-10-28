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