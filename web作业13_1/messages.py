from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
import time


log_config = {
    'file': 'logs.txt'
}


def set_log_path():
    fmt = '%Y%m%d%H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    log_config['file'] = 'logs/log.gua.{}.txt'.format(dt)


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    # 这样确保了每次运行都有一个独立的 path 存放 log
    path = log_config.get('file')
    if path is None:
        set_log_path()
        path = log_config['file']
    with open(path, 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)



from model import message

messages = Blueprint('messages', __name__)


@messages.route('/', methods=['GET'])
def index():
    message_lists = message.query.all()
    return render_template('messages.html', message_lists=message_lists)


@messages.route('/add', methods=['POST'])
def add():
    form = request.form
    m = message(form)
    message.save(m)
    return redirect(url_for('messages.index'))


@messages.route('/edit/<int:message_id>', methods=['POST'])
def edit(message_id):
    form = request.form
    m = message(form)
    message.save(m)
    return render_template('messages_edit.html')


@messages.route('/delete/<int:message_id>', methods=['POST'])
def delete(message_id):
    id = int(message_id)
    message.delete(message.id)
    return redirect(url_for('messages.index'))


