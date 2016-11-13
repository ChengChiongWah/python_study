# 2016/11/08
#
# Web 10 作业

# 作业 1
"""
下载 VirtualBox 这款虚拟机软件并安装使用
下载地址如下(群文件也有)
https://www.virtualbox.org/wiki/Downloads
"""

# 作业 2
"""
下载 Ubuntu 16.04 LTS 版本的 iso 镜像文件
在虚拟机中安装使用
下载地址如下
32位
http://releases.ubuntu.com/16.04/ubuntu-16.04-desktop-i386.iso
64位
http://releases.ubuntu.com/16.04/ubuntu-16.04-desktop-amd64.iso
"""

"""
资料
两个 ascii 码转换函数

ord('a') # 97
chr(65)  # 'A'
"""


# 作业 3
#
def binary(n):
    """
    n 是一个不大于 255 的 int
    返回 n 的 8 位二进制形式的字符串
    例如 binary(7) 返回 '00000111'

    进制转换自行搜索或者论坛提问大家讨论吧
    """
    binary_number = bin(n)
    if len(binary_number) < 10:
        add_number = 10 - len(binary_number)
        binary_number = binary_number[:2] + '0' * add_number + binary_number[2:]
    binary_number = binary_number[2:]
    return binary_number


def test_binary():
    n = 120
    expect = ['01111000']
    assert binary(n) in expect


# 作业 4
#
def int10(bin_number):
    """
    bin 是一个 8 位二进制形式的字符串
    返回 bin 代表的数字
    例如 int10('00000111') 返回 7

    进制转换自行搜索或者论坛提问大家讨论吧
    """
    int_number = int(bin_number, 2)
    return int_number


def test_int10():
    n = '1111111'
    expected = [127]
    assert int10(n) in expected


# 作业 5
#
def binaryStream(s):
    """
    s 是一个 string
    返回 s 的二进制字符串
    例如 binaryStream('Man') 返回
    '010011010110000101101110'

    使用上面的函数
    """
    binary_number = ''
    for character in s:
        binary_number += binary(ord(character))
    return binary_number


def test_binaryStream():
    n = 'B'
    expected = ['01000010']
    assert binaryStream(n) in expected


# 作业 6
#
def stringFromBinary(bins):
    """
    bins 是一个二进制形式的字符串
    返回 bins 代表的原始字符串
    例如 stringFromBinary('010011010110000101101110') 返回 'Man'

    使用上面的函数
    """
    string_step = len(bins) / 8
    string = ''
    while string_step > 0:
        int_numbers = int10(bins[:8])
        string += chr(int_numbers)
        bins = bins[8:]
        string_step -= 1
    return string


def test_stringFromBinary():
    n = '01000010'
    expected = ['B']
    assert stringFromBinary(n) in expected


# 作业 7
#
def base64Encode(s):
    """
    s 是一个 string
    返回 s 的 base64 编码

Base64是一种基于 64 个可打印字符来表示数据的方法
它用每6个比特为一个单元，对应某个可打印字符
ASCII 码一个字符是 8 比特, 也就是一字节
3 个字节就有 24 个比特, 对应了 4 个 base64 单元

如下所示
原始信息        M        a        n
ASCII         77       7        110
二进制         01001101 01100001 01101110
4 个单元       010011 010110 000101 101110
每个单元转换后  19  22  5  46

转换后每个 base64 单元都是一个 0-63 的数字
因为 6 比特表示的范围就是这么大
然后数字到字符串的转换是下面这段字符串取下标所得
'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

那么 Base64 编码结果就是    T   W   F  u

所以 base64Encode('Man') 返回 'TWFu'


既然 3 个字节转换为 4 个 base64 单元
那么 1 个字节怎么办呢?
答案是用 0 补出 3 字节, 如下所示
原始信息    M
ASCII     77       0        0
二进制     01001101 00000000 00000000
4 个单元   010011 010000 000000 000000
单元转换后  19 16 0 0
因为末尾是强行补上的, 所以给他用 '=' 凑出字符(这是一个例外)
所以 base64Encode('M') 返回 'TQ=='
    """
    base64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'  # base64对照表
    base64_string = ''
    string_binary = binaryStream(s)  # 先把字符串转换成2进制
    string_binary_length = len(string_binary)  # 所得2进制的长度
    mod_number = divmod(string_binary_length, 24)  # 对所得2进制长度除取模
    if mod_number[1] != 0:  # 不是24字节的整数倍
        string_binary += '0' * (24 - mod_number[1])  # 添加成24的整数倍
    while len(string_binary) > 0:
        base64_number = int10(string_binary[:6])  # 每6个字节对应的数值
        if base64_number == 0:
            base64_string += '='
        else:
            base64_string += base64_table[base64_number]  # 在base64_table对照表找找到对应的字符
        string_binary = string_binary[6:]  # 以6个字节为单位截断
    return base64_string


def test_base64Encode():
    n = 'M'
    expect = ['Qg==', 'TQ==']
    assert base64Encode(n) in expect


# 作业 8
#
'''
def base64Decode(s):
    """
    s 是一个 base64 编码后的字符串
    解码 s 并返回
    例如 base64Decode('TWFu') 返回 'Man'
 def int10(bin_number):
    """
    bin 是一个 8 位二进制形式的字符串
    返回 bin 代表的数字
    例如 int10('00000111') 返回 7

    进制转换自行搜索或者论坛提问大家讨论吧
    """
    int_number = int(bin_number, 2)
    return int_number
'''


def binary(n):
    """
    返回 n 的 6 位二进制形式的字符串
    例如 binary(7) 返回 '000111'

    进制转换自行搜索或者论坛提问大家讨论吧
    """
    binary_number = bin(n)
    if len(binary_number) < 8:
        add_number = 8 - len(binary_number)
        binary_number = binary_number[:2] + '0' * add_number + binary_number[2:]
    binary_number = binary_number[2:]
    return binary_number


def stringFromBinary(bins):
    """
    bins 是一个二进制形式的字符串
    返回 bins 代表的原始字符串
    例如 stringFromBinary('010011010110000101101110') 返回 'Man'

    使用上面的函数
    """
    string_step = len(bins) / 8
    string = ''
    while string_step > 0:
        int_numbers = int10(bins[:8])
        string += chr(int_numbers)
        bins = bins[8:]
        string_step -= 1
    return string


def base64Decode(s):
    """
    s 是一个 base64 编码后的字符串
    解码 s 并返回
    例如 base64Decode('TWFu') 返回 'Man'
    原始信息    M
    ASCII     77       0        0
    二进制     01001101 00000000 00000000
    4 个单元   010011 010000 000000 000000
    单元转换后  19 16 0 0
    TQ==
    """
    base64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'  # base64对照表
    string = ''
    binary_number = ''
    for character in s:
        if character == '=':  # = 字符表示0
            binary_number += '000000'
        else:
            character_index = base64_table.index(character)    # 按照base64对照表找到每一个字母的
            binary_number += binary(character_index)  # 返回6位的二进制数
    while len(binary_number) > 0:
        string += stringFromBinary(binary_number[:8])
        binary_number = binary_number[8:]
    return string


def test_base64Decode():
    n = 'TQ=='
    expect = ['Qg==', 'TQ==', 'M']
    assert base64Decode(n) in expect
   """

