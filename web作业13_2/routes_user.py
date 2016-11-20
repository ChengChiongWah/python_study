from flask import request
from flask import Blueprint
from flask import render_template

registers = Blueprint('registers', __name__)


@registers.route('/', methods=['GET'])
def login():
    form = request.form.register
    return render_template('register.html')

