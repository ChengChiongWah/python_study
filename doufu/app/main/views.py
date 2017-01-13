from flask import render_template, request
from flask_login import current_user
from . import main
from ..models import Recipe
from ..log import Log


@main.route('/', methods=['GET'])
def index():
    res = Recipe.query.all()
    if request.args.get('page') is None:
        page = 1
        pagination = Recipe.query.paginate(page, 10, False)
        pageitems = pagination.items
    else:
        page = int(request.args.get('page'))
        pagination = Recipe.query.paginate(page, 10, False)
        pageitems = pagination.items
    return render_template('index.html', pageitems=pageitems, pagination=pagination, page=page, res=res)
