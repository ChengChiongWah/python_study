# encoding: utf-8

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
    string = ""
    for k, v in headers.items():
        string = string + str(k) +";"+ str(v) + r"/r/n"
    return string
def main():
    headers =    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    print(header_from_dict(headers))

# print(movie(url))
#   print(type(movie(url)))
#   status_code, headers, body = get(url)
#    print(status_code, headers, body)

if __name__ == '__main__':
    main()



