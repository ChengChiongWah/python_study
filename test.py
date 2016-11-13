def int10(bin_number):
    """
    bin 是一个 8 位二进制形式的字符串
    返回 bin 代表的数字
    例如 int10('00000111') 返回 7

    进制转换自行搜索或者论坛提问大家讨论吧
    """
    int_number = int(bin_number, 2)
    return int_number


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


s = 'TQ=='
a = base64Decode(s)
# a = test_base64Encode()
print(a)
