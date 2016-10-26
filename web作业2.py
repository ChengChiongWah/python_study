"""
2016/10/20

作业 2

请参考上课 1 板书内容
"""


# 1
# 补全函数 parsed_url
def parsed_url(url):
    '''
    url 可能的值如下
    g.cn
    g.cn/
    g.cn:3000
    g.cn:3000/search
    http://g.cn
    https://g.cn
    http://g.cn/

	NOTE:
    没有 protocol 时, 默认协议是 http

    在 http 下 默认端口是 80
    在 https 下 默认端口是 443
    :return : tuple, 内容如下 (protocol, host, port, path)
    '''
    if url[:8] == "https://":  # https://协议
        protocol = "https"
        url = url[8:]
    elif url[:7] == "http://":  # 标明是http
        protocol = "http"
        url = url[7:]
    else:  # 没有标明protocol时
        protocle = "http"

    if url[:].find(":") == -1:  # g.cn
        host = url[:]
        if protocol == "https":
            port = 443
        else:
            port = 80
        path = "/"
    else:  # g.cn:300
        host_end = url.find(":")
        host = url[:host_end]
        url = url[host_end + 1:]
        if url[:].find("/") == -1:   # g.cn:3000
            port = int(url[:])
            path = "/"
        else:  # g.cn:3000/abc
            port_end = url[:].find("/")
            port = int(url[:port_end])
            path = url[port_end + 1:]

    return (protocol, host, port, path)


# 2
# 给 1 写测试
def test_parsed_url(url):
    '''
    '''
    pass


# 3
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    string = ""
    for k, v in dic.items():
        if type(v) is int:
            v = str(v)
        if len(string) == 0:
            string = string + (k + "=" + v + "&")
        else:
            string = string +(k + "=" + v )
    print("/?" + string)


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 4
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    pass


# 5
#
# 为作业 4 写测试


# 6
def args_from_url(url):
    '''
    url 是一个字符串, 如下
    http://cocode.cc/test?a=1&b=2&c=3

    返回一个这样的字典
    {
        'a': '1',
        'b': '2',
        'c': '3',
    }
    '''
    url_bg = url.find("?") + 1
    url = url[url_bg:]
    url = url.splite("&")
    fdic = {}
    for elem in url:
        fdic = dic((elem.split("=")),)
    return fdic


