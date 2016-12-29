from flask import render_template
from . import main
from ..models import Recipe


@main.route('/', methods=['GET'])
def index():
     res = Recipe.query.limit(10).all()
     length = len(res)
     return render_template('index.html',res=res, length=length )