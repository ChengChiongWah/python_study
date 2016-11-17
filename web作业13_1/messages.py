from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from model import message

messages = Blueprint('messages', __name__)

@messages.route('/', methods=['GET'])
def index():
    message_lists = message.query.all()
    return render_template('messages.html', message_lists=message_lists)


@messages.route('/add', methods=['POST'])
def add():
    form = request.form.get('message-contents')
    m = message(form)
    message.save(m)
    # return redirect(url_for('messages.index'))
    return form


# @messages.route('/edit', methods=['POST'])
# def edit():
#     id = form.get('id')

