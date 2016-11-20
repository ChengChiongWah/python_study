# coding=utf-8


"""web6作业：http各个头代表的意义
"""

'''
协议头的字段是以明文的字符串格式传输的，以冒号分割的键名 / 值对，最后以回车（CR）和换行（LF）符序列结尾。协议
头部分的结束时以一个空白的字段来标识的，结果是会传输两个连续的回车换行符对
Accetp：能接受的回应内容类型（content - types）如Accept：text / plain
Accept - Charset：能够接受的字符集 如Accep - Charset:utf - 8
Accept - Language：能够接受的回应内容的自然语言列表。 如Accept - Language：en - Us
Accept - Datetime：能够接受的按照时间来表示的版本 如Accept - Datetime:Thu, 31 May 2007 20:35:00 GMT
Authorization: 用于超文本传输协议的认证的认证信息 如Authorization：BasicQWdfj
cache - control：用来制定在这次的请求 / 回复链中的所有缓存机制都必须遵守的指令 如Cache -Contol:no - cache
connection： 浏览器想要优先使用的连接类型 如Connection：keep - alive
cookie：之前由服务器通过Set - Cookie发送的一个超文本传输协议Cookie 如：Cookie：$Version；Skin = new
Content_Length:以八位字节表示的请求体的长度 如Content - Length:348
Content - MD5：请求体的内容的二进制MD5散列值，以Base64编码的结果
Content - MD5：Qhdfdfdf234
Content - Type: 请求体的多媒体类型（用于POST和PUT请求中）Content - Type：application / x - www -form - urlencoded
Date： 发送该消息的日期和时间 如Date：Tue，15 Nov 1994 0 8:12:31 GMT
Expect: 表明客户端要求服务器做出特定的行为 如Expect：100 -continue
From： 发起此请求的用户的邮件地址 如From：user @ example.com
Host：服务器的域名（用于虚拟主机）以及服务器所监听的传输控制协议端口号，如果请求的端口号是对应得服务的标准端
      口，则端口号可被省略，自超文本传输协议版本1.1（http / 1.1）开始便是必需字段
      如Host：en.wikipedia.org:80 Host：en.wikipedia.org
If - Match：仅当客户端提供的实体与服务器上对应得实体相匹配时，才进行对应得操作。主要作用时，用作像PUT这样的方
            法中，仅当从用户上次更新某个资源以来，改资源未修改的情况下，才更新该资源。
            如 If - Match:“43434dfasdrfdf43”
If - Modified - Since：允许在对应得内容未被修改的情况下返回304未修改（304 Not Modified）
                       如：If - Modified - since：Sat，29，Oct 1994 19:43:31 GMT
IF - None - Match：允许在对应得内容未被修改的情况下返回304未修改（304 Not Modified）参考超文本传输协议的实
                   体标记 如If - None - Match:"73043dfdff3"
If - Range:如果该实体未被修改过，则向我发送所缺额哪一个或多个部分；否则，发送整个新实体
           如IF - Rang:“70070dfadfa3434”
If - Unmodified - Since：仅当该实体自某个特定时间以来未被修改的情况下，才发送回应
                         如If -Unmodified - Since:Sat, 29 Oct 1994 19:43:31 GMT
Max - Forwards： 限制该消息可被代理及网关转发的次数 如Max - Forwards:10
Origin：发起一个针对跨来源资源共享的请求（要求服务器在回应中加入一个‘方位控制允许来源’
       ('Access - Control - Allow - Origi')字段）如：Origin：http: // www.example - social - network.com
Pragma：与具体的实现相关，这些字段可能在请求 / 回应链中的任何时候产生多种效果 如 Pragmatic：no - cache
Proxy - Authorization:用了向代理进行人证的信息如：Proxy - Authorization：BasicQwer34fdff
Range：仅请求某个实体的一部分。字节偏移以0开始。参考字节服务如：Range：byte = 500 - 99
Refer而[sic]：表示浏览器所访问的前一个页面，正是那个页面上的某个链接将浏览器带到了当前请求的这个页面。
             (“引导者”（“referrer”)这个单词，在RFC中被拼错了，因此在大部分的软件实现中也拼错了，以至于
             错误的拼法成为了标准的用法） 如：Referer：http: // en.wikipedia.org / wiki / Main_page
TE：浏览器预期接受的传输编码方式，可使用回应协议头Transfer - Encoding字段中的那些值，另外还有一个值可用，
    "trailers"（与“分块”传输方式相关），用来表明浏览器希望在最后一个尺寸为0的块之后还接收到一些额外的字段。
    如：TE:trailers, deflate
User - Agent:浏览器的身份标识 如：User - Agent:Mozilla / 5.0(X11;Linux X86_64; rv：12.0) Gecko / 20100101 Firefox / 21.0
upgrade:要求服务器升级到另一个协议 如：Upgrade：HTTP / 2.0, SHTTP / 1.3, IRC / 6.9, RTA / X11
Via：向服务器告知，这个请求是由哪些代理发出 如：Via：1.0 fred，1.0 example.com (Apache / 1.1)
Warning:一个一般性的警告，告知，在实体内容中可能存在错误 如：Warning：199 Miscellaneous warning
'''

'''
要知道一个类有哪些属性，有两种方法。最简单的是使用dir（）内建函数，另外是通过访问类的字典属性__dict__,
这是所有类都具备的特殊属性之一。dir（Myclass）   Myclass.__dict__
'''

'''
多重继承中，如果类需要调用已经调用类的上一层类的方法，可以用如下的方法来调用：
P2.bar(gc)
'''

'''
新式类也有一个__mro__属性，告诉你查照的顺序：GC.__mro__
'''

'''
经典类使用深度优先算法。因为新式类继承自object，新的菱形继承结构出现，问题也就接着而来了。所以必须新建一个MRO
'''

'''
hasattr() getattr() setattr() delattr() *attr()
系列函数可以在各种对象下工作，不限于类和实例，
hasattr()
目的是为了决定一个对象是否有一个特定的属性，一般用于访问某属性前先做一下检查，
getattr()
取得对象的属性，试图读取一个不存在的属性时，引发AttributeError异常，除非那个可选的默认参数。
setattr()
赋值给对象的属性，要么加入一个新的属性，要么取代一个也存在的属性。
delattr()
从一个对象中删除属性。
'''

'''
super()
的主要用途是来查找父类的属性。比如：super(MyClass, self).__init__(), 如果没有执行这样的查找，
你可能不需要使用super（）。
'''

'''
如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，表示私有变量，只有内部访问，外部不能访问。
'''

'''
@property

把一个getter方法变成属性（加上 @ property），此时本身又创建另一个装饰器 @ score.setter，
负责把setter方法变成属性赋值

class Student（object）：
    @property
    def birth（self）：
        return self._birth

    @birth.setter  # birth是可读属性
    def birth（self，value):
        self._birth = value

    @ property
    def age（self）：  # age就是一个只读属性
        return 2015 - self._birth
'''

'''
各魔法方法:
__str__(self):
定义对类的实例调用str（）时的行为

__repr__(self):
定义对类的实例调用represent（）时的行为。str（）和repr（）最主要的区别在于目标用户，represent（）的作用是
产生极其可读的输出（大部分情况下其输出可作为python的有效代码）， 而str（）则产生人类可读的输出

__unicode__(self):
定义对类的实例调用Unicode（）时的行为，Unicode（）和str（）很像，只是它返回unicode字符串。注意，如果调用者
试图调用str（）而你只实现了__unicode__(), 那么类将来不能正常工作。所以你应该总是定义__str__(), 以防有些人
没有闲情逸致来使用unicode.

__format__(self):
定义当类的实例用于新式字符串格式化时的行为，例如:"Hello,0:abc!".format(a)会导致调用a.__format__("abc")当定
义你自己的数值类型或字符串类型时，你可能想提供某些特殊的格式化选项，这种情况下这个魔法方法非常有用

__hash__(self):
定义类的实例调用hash（）时的行为，他必须返回一个整数，其结果被用于字典中键的快速比较。同时注意一点，实现这个
魔法方法通常也需要实现__eq__，并且遵守如下的规则：a == b意味着hash（a） == hash（b）

__nonzero__（self）：
定义对类的实例调用bool（）时的行为，根据你自己对类的设计，针对不同的实例，这个魔法方法应该相应地返回True或Flase。

__dir__(self):
定义对类的实例调用dir（）时的行为，这个方法应该向调用者返回一个属性列表。一般来说没有必要自己实现__dir__.
但是如果你重定义了__getattr__或者__getattribute__, 乃至使用动态生成的属性，以实现类的交互式使用，那么
这个魔法方法必不可少。

__getattr__(self, name):
当用户试图访问一个根本不存在（或暂时不存在）的属性时，你可以通过这个魔法方法来定义类的行为，这个可以用于捕捉
错误的拼写并且给出指引，使用废弃属性时给出警告（如果你愿意，任然可以计算并且返回该属性），以及灵活地处理
AttributeError.只有当试图访问不存在的属性时它才会被调用。所以这不能算是真正的封装的办法。

__setattr__(self, name):
允许自定义某个属性的赋值行为，不管这个属性存在与否，也就是说你可以对任意属性的任何变化都定义自己的规则

__delattr__(self, name):
用于处理删除属性时的行为。和__setattr__一样，使用它时也需要多加小心，防止产生无限递归(在__delattr__的实现中
调用del self.name会导致无限递归）。

__getattribute__(self, name):
__getattribute__只能用于新式类，允许你自定义属性被访问时的行为，它也同样可能遇到无限递归问题
(通过调用基类的__getattribute__来避免)。__getattribute__基本可以替代__getattr__.只有当它被实现，并且显示
地被调用，或者产生AttributeError时它才被使用。这个魔法方法可以被使用，不推荐使用它，因为它的使用范围相对
有限（通常我们想要在赋值时进行特殊操作，而不是取值时），而且这个方法很容易出现Bug。

自定义这些控制属性访问的魔法方法很容易导致问题：
def __setattr__(self, name, value):
    self.name = value
    # 因为每次属性幅值都要调用 __setattr__(),所以这里的实现会导致递归，
    #这里的调用实际上是self.__setattr('name',value)。因为这个方法一直在
    #调用自己，因此递归将持续进行，直到程序崩溃
def __setattr__(self, name, value)
    self.__dict__[name] = value  # 使用__dict__并进行赋值，定义自定义行为。


class AccessCounter(object):
    """一个包含了一个值并且实现了访问计数器的类每次值的变化都会导致计数器自增"""

    def __init__(self, val):
        super(AcessCounter, self).__setattr__('counter', 0)
        super(AccessCount，self).__setattr__('value', val)

    def __setattr__(self, name, value):
        if name == 'value':
            super(AccessCounter, self).__setattr__('counter', self.counter + 1)
        # 使计数器自增变成不可避免
        # 如果你想阻止其他属性的赋值行为
        # 产生AttributerError（name）就可以了
        super（AccessCounter，self).__setattr__(name, value)

    def __delattr__(self, name):
        if name == "value":
            super(AccessCounter, self).__setattr('counter', self.counter + 1)
            super(AccessCounter，self).__delattr(name)

容器背后的魔法方法
__len__(self):
返回对容器中某一项使用self[key]的方式进行读取操作的行为。这也是可变和不变容器类行都要实现的一个方法，
他应该在键的类型错误式产生TypeError异常，同时在没有与键值相匹配的内容时产生KeyError异常
__setitem__(self, key)
定义对容器中某一项使用self[key]的方法进行赋值操作时的行为。他是可变容器类型必须实现的一个方法，同样应该在
合适的时候产生KeyError和TypeError异常
__iter__(self, key)
它应该返回当前容器的一个迭代器。迭代器以一连串内容的形式返回，最常用的是使用iteration（）函数调用，以及在类
似for x in container：的循环中被调用
__reversed__(self):
定义了对容器使用reverse的（）内建函数的行为，他应该返回一个反转的序列
__contains__(self, item)
定义了使用in 和 not in 进行成员测试时类的行为。
__missing__(self, key)
在字典的子类中使用，他定义了当试图访问一个字典中不存在的键时的行为
列子：
class FunCtionalList(object):
    """一个列表的封装类，实现了一些额外的函数式方法,例如head, tail, init, last, drop,和take"""
     def __init__(self, values=None):
        if values is None:
            self.value = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]   #如果键的类型或值不合法，列表会返回异常

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return reversed(self.values)

    def append(self, value):
        self.values.append(value)

    def head(self):
        return self.values[0]

    def tail(self):
        return self.values[1:]  #取得除第一个元素外的所有元素

    def init(self):
        return self.values[:-1]  #取得除最后一个元素外的所有元素

    def last(self):
        return self.values[:-1]  #取得最后一个元素

    def drop(self, n):
        return self.values[n:]  #取得除前n个元素外的所有元素

    def take(self, n):
        return self.values[:n]  #取得前那个元素


__call__(self, [args...])
允许类的一个实例像函数那样被调用，本质是这代表了x() 和x.__call__()是相同的，在某些需要经常改变状态的类
的实例中特别有用，"调用"这个实例来改变他的状态，是一种更加符合自觉优雅的方法
例：
class Entity(object):
    """表示一个实体的类，调用他的实例可以更新实体的位置"""
    def __init__(self, size, x, y)
        self.x, self.y = x, y
        self.size = size

    def __call__(self, x, y):
        self.x, self.y = x, y   #改变实体的位置




'''

'''
编码（encode）\解码（decode）
     string
      / \
 encode  decode
   ^      |
     \ /
     byte
s.encode(utf - 8) --> bytes
b.decode(utf - 8) --> str
'''

'''
web4:
行末尾  \代表是连接多行字符串
使用with可以保证程序中断的时候正确关闭
http头：connectiong：close表示服务器给客户端发送信息之后就断开，
html中不管有多少个空格只显示一个空格。
html的form中一定要有一个button（按钮）
如果请求用get会在url中直接显示用户的请求信息。
如果请求用post 他的请求内容放在body里面，在URL中不会显示。
一般来说都用post

form
    是html用来给服务器传递数据的 tag form中action属性是path method属性是http方法（get post）
    浏览器使用method属性的方法将表单中的数据传送给服务器处理，有POST 和 GET两种方法
    如果用POST方法，浏览器将会按照下面两步来发送，首先浏览器将与action属性中的指定的表单服务器取得联系，
    一旦取得联系之后，浏览器就会按分段传输的方法将数据发送给服务器

    在服务器端，一旦POST样式的应用程序开始执行时，就应该从一个标志位置读取参数，而一旦读到参数，在应用程序
    能够使用这些表单值以前，必须对这些参数进行解码，用户特定的服务器会明确指定应用程序应该如何接受这些参数

    另一种情况是采用GET方法，这时浏览器会与表单服务器建立连接，然后直接在一个传输步骤发送所有的表单数据；浏览器
    会将数据直接附在表单的action url之后。这两者之间用？号隔开

    一般浏览器通过上述任何一种方法都可以传输表单信息，而有些服务器只接受其中一种方法提供的数据，可以在<form>
    标签的method属性中指明表单处理服务器要用的方法来处理数据

'''

'''
web5:

'''

'''
web6:
web6作业：http各个头代表的意义
Set - Cokkie的内容很复杂，a = b的形式（变量跟值类似）
第一次发送cookie给浏览器 后面浏览器访问时会带上cookie服务器从cookie就可以识别哪一个用户。
session 把信息存在服务器，？？？？
代码在论坛上贴上后？？？（豪华储瓜间上面）
ORM：object relation mapping
'''

'''
web7:
setattr
root.xpath('//div[@class="item"]')
'''

'''
web9:
摘要算法是一种能产生特殊格式的算法，给定任意长度的数据生成定长的密文摘要结果是不可逆的，不能被还原为原数据
摘要算法不是压缩不是加密，正是生成签名。
import hashlib
pwd='gua'.encode('ascii')
m = hashlib.md5(pwd)   #md5
print (m.hexdigest())

s = hashlib.sha1(pwd) #sha1
prin他（m.hexdigest())

用MD5或者sha1保护用户的密码 用户的密码存在数据库中，有可能会被黑客盗取（拖库）

用salt防止黑客对密码进行碰撞，假如用户使用简单密码，破解者可以用提前生成的简单密码摘要表（彩虹表）来破解原文
所以我们会存储一个额外的信息，扰乱用户的简单密码
用函数可以生成一个带盐的密文
加盐的目的是极大增加被破解的难度
def salted_password(self, password， salt）：
    def md5hex(ascii_str):
        return hashlib.md5(ascii_str.encode('ascii')).hexdigest()
    hash1 = md5hex(password)
    hash2 = md5hex(hash1 + salt)
    return hash2

持久化session
什么是持久化 把一个东西存在硬盘中，不会因为掉电而丢失

作业：edit update  新增添加评论
'''

'''
socket
Socket 类型：
    socket（family, type[, protocal])  使用给定的地址族,套接字类型, 协议编号（默认为0）来创建
    socket.AF_UNIX        只能够用于单一的Unix系统间通信
    socket.AF_INET        服务器之间网络通讯
    socket.AF_INET6       IPv6
    socket.SOCKET_STREAM  流式socket for TCP
    socket.SOCK_DGRAM     数据报式socket， for UDP
    socket.SOCK_RAW       原始套接字，普通的套接字无法处理ICMP IGMP等网络报文，而SOCK_RAW可以，其次，
                          SOCK_RAW也可以处理特殊的IPv4报文，此外，利用原始套接字，可以通过IP_HDRINCL
                          套接字选项由用户构造IP头
    socket.SOCK_SEQPACKET 可靠的连续数据包服务
    创建TCP Scoket         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    创建UDP Socket         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Socket 函数
注意： TCP发送数据时，已建立好TCP连接，所以不需要指定地址。UDP是面向无连接的每次发送要指定发送给谁
      服务端与客户端不能直接发送列表，元祖 字典需要字符串化
socket函数
服务端socket函数
    s.bind(address)        将套接字绑定到地址，在AF_INET下以元祖（host, port)的形式表示地址
    s.listen(backlog)      开始监听TCP传入连接。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接量
                           ，该值至少为1，大部分应用程序设为5就可以了
    s.accept()             接受TCP连接并返回（conn, address),其中conn是新的套接字对象，可以用来接收和发送数据。
                           address是连接客户端的地址
客户端socket函数
    s.connect(address)     连接到address处的套接字。一般address的格式为元祖（host， port），如果
                           连接出错，返回socket.error错误
    s.connect_ex(address)  功能与connect（address）相同，但是成功返回0，失败返回errno的值
公共socket函数
    s.recv（bufsize[, flag]) 接受TCP套接字的数据。数据以字符串形式返回，bufsize指定要接受的最大数据量
                            flag提供有关消息的其他信息， 通常可以忽略
    s.send(string[, flag])  发送TCP数据。将string中的数据发送到连接的套接字。返回值是要发送的数据量
                            改数据量可能小于string的字节大小
    s.sendall(string[, flag]) 完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会
                             尝试发送所有数据，成功返回None，失败则抛出异常
    s.recvfrom(bufsize[,flag]) 接受UDP套接字的数据。与recv()类似，但返回值是（data, address).其中data是包含
                              接收数据的字符串，address是发送数据的套接字地址。
    s.sendto(string[,flag],address） 发送UDP数据。将数据发送到套接字，address是形式为（ipaddr, prot)的元祖
                              指定远程地址。返回值是发送的字节数
    s.close()                关闭套接字
    s.getpeername()          返回连接套接字的远程地址。返回值通常是元祖（ipaddr, port）
    s.getsockname()          返回套接字自己的地址，通常是一个元祖（ipaddr， port）
    s.setsockport(level, opename, value) 设置给定套接字选项的值
    s.getsockopt(level, optname[,buflen])   返回套接字选项的值
    s.settimeout(timeout)     设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期
                              一般超时期应该在刚创建套接字是设置，因为他们可能用于连接的操作如connect（）
    s.fileno()               返回套接字的文件描述符
    s.setblocking(flag)      如果flag为0，则将套接字设为非阻塞模式，否则将套接字设置为阻塞模式（默认值)非阻塞
                             模式下，如果调用recv（）没有发现任何数据，或者send（）调用无法立即发送数据，那么
                             将引起socket.error异常
    s.makefile（）           创建一个与该套接字相关连得文件
socket服务端：
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #创建套接字
s.bind()         #绑定套接字到本地IP与端口
s.listen(3)       #监听
s.accept()       #接收客户端的连接请求
s.recv()  s.send()     #接收传来的数据并发送给对方数据
s.close()     #传输完毕，关闭套接字

socket客户端：
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #创建套接字
s.connect()    #连接远端地址
s.sendall()    #发送数据
s.recv()  #接收数据
s.close() #关闭套接字

'''

'''
web10
1.用AES算法加密session以及这样做的好处：
每一个session id是一个令牌，存储在服务器上面 加密之后就可以不要持久化session
比如本来 cookie uid=1 加密之后是 uid=dfdadfdsf
python不自带AES的模块 要自己安装 pip3 install pycrypto

2.base64 编码以及用处
主要是把任意的数据转化为可显示的字符
如 10100101 10101100 10101010
   a-Z  0-9
    52   62  加上/+  共64  有等号=表示猜不出来的东西

3. 程序在服务器上运行的原理
服务器就是一台电脑，以前的服务器是机房托管模式（电信机房 网通机房）你把电脑给电信服务商，他帮你接上网线
现在是云服务形式

浏览器发送请求到服务器
服务器主机得到请求 （域名host 端口port）
转给http服务器  （主流是 Apache 和 Nginx）理由如下：
  1.更加健壮，不会一崩溃触动全身
  2.更安全，更少漏洞，因为Apache 这种程序应用最广最成熟
  3.更快速的响应（比如我们请求一个图片，static下面的内容全部对给Apache，比python的open file要快）更高的性能
http服务器转给我们的程序
http服务器响应给浏览器

4.买域名和买服务器
512M的内存 腾讯 淘宝或国外的云服务
godaddy 新网 万网
Linux版本选择

装一个虚拟机



作业：base64 装个Linux
'''

'''
web11

mkdir     创建目录
    -p 可以一次连环创建目录
    mkdir -p /a/b/c
rmdir     删除一个空目录
rm    删除文件或目录（很危险）
    -f 强制删除一个目录
    -r 删除目录
mv     移动文件或文件改名
    可以用mv xx /tmp的方式将文件放到临时文件夹（/tmp是操作系统提供的临时文件夹，
    重启后会删除里面的所有文件）
cat    显示文件内容
tac    反向显示文件内容
nl     显示文件内容，并显示行号
more   显示分屏分批看文件
les    比more更高级，可以前后退看文件
head   可以显示文件前面10行
tail   可以显示文件后10行
       head tail 有一个n参数，表示显示n行
touch  touch a.gua  如果a.gua存在，就更新修改时间
        如果不存在就创建a.gua文件
sudo   用管理员账户执行程序
        比如安装程序或修改一些系统配置都需要管理员权限
su      切换用户

chown   改变文件所属用户
        chown  gua c.gua
        chown  gua：gua  c.gua
chmod   改变文件权限
文件权限        文件类型   用户  用户组  文件大小     修改日期     文件名
drwxrwxr-x       1         gua   gua      4096    11/09 20:28    b.gua



'''
'''
web12

<<SQL 必知必会>>
<<MySQL 必知必会>>
规范SQL语句书写，比如：
INSERT INTO
    'USER'('id', 'username', 'password', 'email')
VALUES
    (NULL, NULL, NULl, NULL)
主键是方便能索引到表中的数据
创建约束 PRIMARY KEY,  AUTONICREMENT, NOT NULL, UNIQUE
外键是别人的主键
sql_insert= """
    INSERT INTO
        'users' ('username', 'password', 'email')
    VALUES
        (?, ?, ?);
    """
    conn.execute(sql_insert, (username, password, email))#注意里面的是tuple。

'''

'''
return
从函数返回值，并终止函数。
'''

'''
web13
ACCEPT-Encoding:gzip, deflate, sdch   #浏览器跟服务器说我支持的那些压缩格式
Accept-Language:en_US,en,q=0.8  #支持的语言
{#。。。。#}是jijia的注释
Conten-Type：告诉服务器body里的内容是什么type。

规定整个整个http头编码是ascii编码  body的编码随便（如果header里的Content-Type:text/html;charset=gbk指定就用指定的）

html5里面可以省略引号

app.config['SQlalCHEMY_DATABASE']='sqlite:///todo.DB'

sqlite save的时候
db.session.add（self）
db.session.commit（）

'''

'''
web14
服务器上面可以可以设置多个cookie
set-cookie:mark=foo
set-cookie:name=gua
上面的字段不能一起设置：set-cookie：mark=foo&name=gua

flask自定义错误页面：
@app.errorhandler(404)
def error404(e):
    return render_template('404.html')

@app.route('/error/<int:code>')
def error_code(code):
    import flask
    flask.abort(code)

数据库关联
class User（db.Model, ModelHelper）:
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    ...
    username=db.relationship('Todo',backref='user', lazy='dynamic')

class Todo(db.Model, ModelHelper):
    __talbename__ = 'tods'
    id = db.Column(db.Integer, primary_key=True)
    ...

Linux
file
     用来显示文件的类型（格式）不是百分之百正确

uname
    显示操作系统的名字，
    uname -r
    uname -A

which
     显示路径
     which pwd 显示pwd的路径

where
    whereis ls
    显示更全面的信息

whoami
    显示当前登录的用户

find
    find . -name 'a.txt'   在当前目录下找a.txt文件

奇怪的符号
    ~  表示家目录 ~会直接到当前用户的家目录
    >  重定向覆盖模式
    >> 重定向追加模式
    tee： cat c.gua|tee f.gua   既能在终端看到也能在f.gua这个文件看到
    |:管道 一个命令的输出是另外一个命令的输入
    grep: 在指定的文件查找gua  grep 'gua' f.gua   又如：cat f.gua | grep 'gua'
    .. 把输出结果替换掉
    & 让程序在后台运行，如firefox & 缺点是关掉终端后开着的程序也会关掉，
    () 让程序在独立子进程（shell）中运行 不会因shell关闭而关掉 (firefox &）
    history
    jobs 看到后台运行的程序
    fg  fg 加任务编号 把后台运行的程序放到前台来，如：fg 1

快捷键
    Ctrl-C 把正在运行的程序挂起放到后台
    Ctrl-Z 终端程序运行
    Ctrl-D 输入文件终止符
    Ctrl-t 交换光标前面的两个字符
    Ctrl-w 删除一个单词
    Ctrl-u 一次删除一行
    Ctrl-k 从光标删除到行尾
    Ctrl-d 删除后一个字符
    Ctrl-h 删除前一个字符
    Ctrl-f forward 往前就是右箭头
    Ctrl-b backward 往后就是左箭头
    Ctrl-p pres 往上 就是上箭头
    Ctrl-n next 往下 就是下箭头



'''










