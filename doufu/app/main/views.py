from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from functools import wraps
from . import main
from ..models import User, Recipe


@main.route('/', methods=['GET'])
def index():
     res = Recipe.query.limit(10).all()
     length = len(res)
     return render_template('index.html',res=res, length=length )